from flask import Flask, render_template # important it is case sensitive # framework for these web routes
from flask_sqlalchemy import SQLAlchemy # easy queries - makes sql less painful
from flask_marshmallow import Marshmallow # nice way to model data - schemas and models structured nicely
import os

#ORM - object relational mapper

app = Flask(__name__) # Flask is acting as a class

# a route is simple an end point to go into an app
# flask uses a decorator

@app.route('/') # route belongs to flask - / is the root route
def hello():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)