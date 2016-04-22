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
    game_number = db.Column(db.Integer, default=1)
    score = db.Column(db.Integer, default=1)
    strikes =db.Column(db.Integer, default=0)


class Choices(db.Model):
    __tablename__ = 'choices'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    choice_type = db.Column(Enum('actor', 'movie', name='choice_type'))

class Games(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_game_number = db.Column(db.Integer, db.ForeignKey('users.game_number'))
    round_number = db.Column(db.Integer, default=0)
    parent_id = db.Column(db.Integer, db.ForeignKey('choices.id'))
    child_id = db.Column(db.Integer, db.ForeignKey('choices.id'))

db.create_all()

movie1 = Choices(name="Movie1", choice_type="movie")
movie2 = Choices(name="Movie2", choice_type="movie")
movie3 = Choices(name="Movie3", choice_type="movie")

actor1 = Choices(name="Actor1", choice_type="actor")
actor2 = Choices(name="Actor2", choice_type="actor")
actor3 = Choices(name="Actor3", choice_type="actor")

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
    for index in range(1, len(chain)):

        parent = chain[index-1]
        child = chain[index]

        parent_entry = Choices.query.filter_by(name=parent).first()
        child_entry = Choices.query.filter_by(name=child).first()

        round_entry = Games(user_id=user.id, user_game_number=user.game_number, round_number=index, parent_id=parent_entry.id, child_id=child_entry.id)

        db.session.add(round_entry)

    db.session.commit()

def get_current(game):

    chain_head = game[-1][-1]
    current = Choices.query.get(chain_head)
    return current.name

def get_connection(game):
    connections = {}
    for round_num in game:
        parent = Choices.query.get(round_num[1])
        child = Choices.query.get(round_num[2])

        connections.setdefault(parent.name.lower(), []).append(child.name.lower())
        connections.setdefault(child.name.lower(), []).append(parent.name.lower())

    # Let's remove any duplicate relationships
    unique_connections = dict([(key, list(set(value))) for key, value in connections.items()])

    return unique_connections

def check_connection(guess, game):

    current = get_current(game).lower()
    connections = get_connection(game)

    if guess.lower() in connections[current]:
        return True
    else:
        return False

def get_chain(game):

    first_item = Choices.query.get(game[0][1]).name
    following_items = [Choices.query.get(round_num[2]).name for round_num in game]
    following_items.insert(0, first_item)

    return following_items

def get_user_data(user_id):

    user_entry = Users.query.filter(Users.id == user_id).first()

    return user_entry

def get_game(user_id):

    game = db.session.query(Games.round_number, Games.parent_id, Games.child_id).\
        filter(Games.user_id == user_id).all()

    return game

def update_user(user_id, new_strike=False):

    user = get_user_data(user_id)
    
    game = get_game(user_id)
    chain_length = len(get_chain(game))

    user.score = chain_length

    if new_strike:
        user.strikes += 1

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

print('before:')
u = get_user_data(1)
print(u.username)
print(u.score)
print(u.strikes)

update_user(1)

print('after:')
u = get_user_data(1)
print(u.username)
print(u.score)
print(u.strikes)

update_user(1, True)


print('after again:')
u = get_user_data(1)
print(u.username)
print(u.score)
print(u.strikes)




