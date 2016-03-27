
from MovieGame import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, asc, distinct, select, func

actor_chain = db.Table('actor_chain', 
    db.Column('actor_id', db.Integer, db.ForeignKey('Actors.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('Users.id'))
)

movie_chain = db.Table('movie_chain',
    db.Column('movie_id', db.Integer, db.ForeignKey('Movies.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('Users.id'))
)

class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    score = db.Column(db.Integer)
    movies = db.relationship('Movie', secondary=movie_chain,
        backref=db.backref('users', lazy='dynamic'))
    actors = db.relationship('Actor', secondary=actor_chain,
        backref=db.backref('actors', lazy='dynamic'))

    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __repr__(self):
        return '{}'.format(self.name)

class Actor(db.Model):
    __tablename__ = 'Actors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Actor: {}>'.format(self.name)

class Movie(db.Model):
    __tablename__ = 'Movies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '{}'.format(self.name)

def process(name, strikes, *args):

    user = User(name, strikes)

    for arg in args:

        movie = Movie.query.filter_by(name=arg).first()
        if not movie:
             movie = Movie(arg)
             print(movie) 
        db.session.add(movie)
        user.movies.append(movie)
        
    db.session.add(user) 
    db.session.commit()
    
if __name__ == '__main__':
    pass

