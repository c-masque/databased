from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Spice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False)
    notes = db.Column(db.String(20), unique=False)
    secondary_notes = db.Column(db.String(20), unique=False)
    description = db.Column(db.String(200), unique=False)

    def __init__(self, name, notes, secondary_notes, description):
        self.name = name
        self.notes = notes
        self.secondary_notes = secondary_notes
        self.description = description


class SpiceSchema(ma.Schema):
    class Meta:
        fields = ('name', 'notes', 'secondary_notes', 'description')


spice_schema = SpiceSchema()
spices_schema = SpiceSchema(many=True)

# please work gods help me
@app.route('/')
def hello():
    return "please work"


# post one new spice
@app.route('/spice', methods=['POST'])
def add_spice():
    name = request.json['name']
    notes = request.json['notes']
    secondary_notes = request.json['secondary_notes']
    description = request.json['description']

    new_spice = Spice(name, notes, secondary_notes, description)

    db.session.add(new_spice)
    db.session.commit()

    spice = Spice.query.get(new_spice.id)

    return spice_schema.jsonify(spice)


# get all spices
@app.route('/all-spices', methods=['GET'])
def get_all_spices():
    all_spices = Spice.query.all()
    result = spices_schema.dump(all_spices)
    return jsonify(result)


# look at one spice # why can't I use name and only can use ID??? is it because it is not unique?
@app.route('/spice/<id>', methods=['GET'])
def get_spice(id):
    spice = Spice.query.get(id)
    return spice_schema.jsonify(spice)


# update spice with put not patch...? # nevermind that's hard
@app.route('/spice/<id>', methods=['PUT'])
def replace_spice(id):
    spice = Spice.query.get(id)
    name = request.json['name']
    notes = request.json['notes']
    secondary_notes = request.json['secondary_notes']
    description = request.json['description']

    spice.name = name
    spice.notes = notes
    spice.secondary_notes = secondary_notes
    spice.description = description

    db.session.commit()
    return spice_schema.jsonify(spice)


# deleting a spice
@app.route('/spice/<id>', methods=['DELETE'])
def spice_deletion(id):
    spice =Spice.query.get(id)
    db.session.delete(spice)
    db.session.commit()

    return f"The {spice} entry was deleted."


if __name__ == '__main__':
    app.run(debug=True)