from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum

from MovieGame import app, db

movies_actors = db.Table('movies_actors',
    db.Column('parent_choice_id', db.Integer, db.ForeignKey('choices.id')),
    db.Column('child_choice_id', db.Integer, db.ForeignKey('choices.id'))
) 


class Users(db.Model):
    """Users model."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    score = db.Column(db.Integer, default=1)
    strikes =db.Column(db.Integer, default=0)


class Choices(db.Model):
    """Choices model. Either actor or movie."""
    __tablename__ = 'choices'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    moviedb_id = db.Column(db.Integer)
    choice_type = db.Column(Enum('actor', 'movie', name='choice_type'))
    relations = db.relationship('Choices',
                                  secondary=movies_actors,
                                  primaryjoin=(movies_actors.c.parent_choice_id == id),
                                  secondaryjoin=(movies_actors.c.child_choice_id == id),
                                  backref=db.backref('movies_actors', lazy='dynamic'),
                                  lazy='dynamic')

class Games(db.Model):
    """Games model. Creates entry for every round of a user's game."""
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    round_number = db.Column(db.Integer, default=0)
    parent_id = db.Column(db.Integer, db.ForeignKey('choices.id'))
    child_id = db.Column(db.Integer, db.ForeignKey('choices.id'))



