import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('/Users/Alexander/Codine/Projects/MovieGame/instance/config.py')
db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    game_number = db.Column(db.Integer)


class Choices(db.Model):
    __tablename__ = 'choices'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    url = db.Column(db.String(140), unique=True)
    type = db.Column(Enum('actor', 'movie', name='choice_type'))

class Games(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_game_number = db.Column(db.Integer, db.ForeignKey('users.game_number'),default=1)
    round_number = db.Column(db.Integer, default=0)
    parent_id = db.Column(db.Integer, db.ForeignKey('choices.id'))
    child_id = db.Column(db.Integer, db.ForeignKey('choices.id'))

db.create_all()

movie1 = Choices(name="Movie1", url="http://Movie1", type="movie")
movie2 = Choices(name="Movie2", url="http://Movie2", type="movie")
movie3 = Choices(name="Movie3", url="http://Movie3", type="movie")

actor1 = Choices(name="Actor1", url="http://Actor1", type="actor")
actor2 = Choices(name="Actor2", url="http://Actor2", type="actor")
actor3 = Choices(name="Actor3", url="http://Actor3", type="actor")

db.session.add(movie1)
db.session.add(movie2)
db.session.add(movie3)
db.session.add(actor1)
db.session.add(actor2)
db.session.add(actor3)
db.session.commit()


username1 = "Alex"
chain = ["Movie1", "Actor1", "Movie2", "Actor2", "Movie3", "Actor3", "Movie2", "Actor2"]

username2 = 'Casey'
chain2 = ["Movie2", "Actor1", "Movie3", "Actor2", "Movie1"]

def play(user, chain):
    user = Users(username=user)
    db.session.add(user)
    round = Games(user_id=user.id)
    for index in range(1, len(chain)):

        parent = chain[index-1]
        child = chain[index]

        parent_entry = Choices.query.filter_by(name=parent).first()
        child_entry = Choices.query.filter_by(name=child).first()

        round_entry = Games(user_id=user.id, round_number=index, parent_id=parent_entry.id, child_id=child_entry.id)

        db.session.add(round_entry)

    db.session.commit()


play(username1, chain)
play(username2, chain2)
# List of rounds for user
q = db.session.query(Games.round_number, Games.parent_id, Games.child_id).filter(Games.user_id == 1).all()
for r in q:
    par = Choices.query.get(r[1])
    chi = Choices.query.get(r[2])

    print("Round: {}, Parent: {}, Child: {}".format(r[0], par.name, chi.name))

print()
q2 = db.session.query(Games.round_number, Games.parent_id, Games.child_id).filter(Games.user_id == 2).all()
for r in q2:
    par = Choices.query.get(r[1])
    chi = Choices.query.get(r[2])

    print("Round: {}, Parent: {}, Child: {}".format(r[0], par.name, chi.name))
