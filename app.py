from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

#Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLACLHEMY_TRACK_MODIFICATIONS'] = False

#Init db
db = SQLAlchemy(app)

#Init ma
ma = Marshmallow(app)

#User Class/Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), unique=False, nullable=False)
    last_name = db.Column(db.String(100), unique=False, nullable=False)
    card_qty = db.Column(db.Integer, unique=False, nullable=False)
    debit_card = db.Column(db.Integer, unique=False, nullable=False)
    credit_card = db.Column(db.Integer, unique=False, nullable=False)

    def __init__(self, first_name, last_name, card_qty, debit_card, credit_card):
        self.first_name = first_name
        self.last_name = last_name
        self.card_qty = card_qty
        self.debit_card = debit_card
        self.credit_card = credit_card

#User Schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name','card_qty', 'debit_card','credit_card')

#Init Shema
user_schema = UserSchema()
users_schema = UserSchema(many=True)

#Create a User (POST)
@app.route('/user', methods=['POST'])
def add_user():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    card_qty = request.json['card_qty']
    debit_card = request.json['debit_card']
    credit_card = request.json['credit_card']

    new_user = User(first_name, last_name, card_qty, debit_card, credit_card)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

#GET All Users
@app.route('/users', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    # dump() - возвращает отформатированный результат
    return jsonify(result)

#GET Single User
@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)

#Update a User
@app.route('/user/<id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)

    first_name = request.json['first_name']
    last_name = request.json['last_name']
    card_qty = request.json['card_qty']
    debit_card = request.json['debit_card']
    credit_card = request.json['credit_card']

    user.first_name = first_name
    user.last_name = last_name
    user.card_qty = card_qty
    user.debit_card = debit_card
    user.credit_card = credit_card

    db.session.commit()

    return user_schema.jsonify(user)

#Delete User
@app.route('/user/<id>', methods=['DELETE'])
def delete_product(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    
    return user_schema.jsonify(user)

#Run Server
if __name__ == '__main__':
    app.run(debug=True)