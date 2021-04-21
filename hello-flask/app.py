from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# create the flask object vvv
app = Flask(__name__)

# part of building the db #
basedir = os.path.abspath(os.path.dirname(__file__)) # dynamic way to map to file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# ^^^ this is adding to this Flask instance's env config the path using the 'SQLALCHEMY DATABASE URI' variable - giving it a name

# DB Connection String example
# sqlite://<username>:<password>@aw.servers.co/mydb:port3928

db = SQLAlchemy(app)
ma = Marshmallow(app)

# THIS MODEL DEFINES OUR BASIC DATABASE STRUCTURE #

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True) # this will be set automatically, allegedly
    title = db.Column(db.String(50), unique=False)
    content = db.Column(db.String(1000), unique=True)

    def __init__(self, title, content):
        self.title = title
        self.content = content

# THIS SCHEMA BELOW IS WHAT IT ACTUALLY LOOKS LIKE - kind of like a filter for what is needed #

class BlogSchema(ma.Schema):
    class Meta:
        fields = ('title', 'content')

# WE ARE INSTANTIATING TWO DIFFERENT BLOG POST OBJECTS 
# HAVING A MULTI SCHEMA HELPS TO NOT SEND AN ARRAY OF SINGLE OBJECTS
blog_post_schema = BlogSchema()
blog_posts_schema = BlogSchema(many=True)

# in repl we did 'from app import db' and 'db.create_all()' and it generated a sql lite db...

############ Endpoint to create a new guide ############

@app.route('/blog_post', methods=['POST'])
def add_blog_post():

    ## We are taking the json title and content key value
    # pairs from the request and setting them to a variable to use here
    title = request.json['title']
    content = request.json['content']

    # creating new ID in database and that new blog post
    new_blog_post = Blog(title, content)

    # this is where the db is actually being interacted with
    # adding this blog post to the new db session and commits
    db.session.add(new_blog_post)
    db.session.commit()

    # this adds certainty by querying the database
    # and confirming the data in the database
    blog_post = Blog.query.get(new_blog_post.id)

    # this jsonify helps structure the data back into json string data
    return blog_post_schema.jsonify(blog_post)

############ Endpoint to query all guides ############

@app.route('/blog_posts', methods=['GET'])
def get_blog_posts():

    all_blog_posts = Blog.query.all()
    result = blog_posts_schema.dump(all_blog_posts)
    return jsonify(result)


############ Endpoint to query single guide ############

@app.route('/blog_post/<id>', methods=['GET']) # the url parameter <id> will help bring up individual post
def get_blog_post(id):
    blog_post = Blog.query.get(id)
    return blog_post_schema.jsonify(blog_post)

############ Endpoint to updating single guide ############

@app.route('/blog_post/<id>', methods=['PUT']) # PUT is important to use uniquely here
def update_blog_post(id):
    blog_post = Blog.query.get(id)
    title = request.json['title']
    content = request.json['content']

    blog_post.title = title
    blog_post.content = content

    db.session.commit()
    return blog_post_schema.jsonify(blog_post)

############ Endpoint for deleting records ############

@app.route('/blog_post/<id>', methods=['DELETE'])
def delete_blog_post(id):
    blog_post = Blog.query.get(id)
    db.session.delete(blog_post)
    db.session.commit()

    return "Blog post was successfully deleted."


## TO RUN THE APP ##
if __name__ == '__main__':
    app.run(debug=True)

# GET
# POST
# PUT/PATCH
# DELETE