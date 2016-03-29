from MovieGame import app, db
from MovieGame.models import *

class Processor(object):

    def __init__(self):
        db.create_all()

    def add_user(self, name, strikes, chain):
        """Add current user and data to database"""

        user = User(name, strikes)

        for index, item in enumerate(chain):

            if index % 2 == 0:
                movie = Movie.query.filter_by(name=item).first()

                if not movie:
                     movie = Movie(item)
                
                db.session.add(movie)
                user.movies.append(movie)

            else:
                actor = Actor.query.filter_by(name=item).first()

                if not actor:
                    actor = Actor(item)

                db.session.add(actor)
                user.actors.append(actor)
            
        db.session.add(user) 
        db.session.commit()

    def get_high_scores(self):
        """Get high scores"""

        scores = db.session.query(User.id, User.name, User.score).\
            order_by(desc(User.score)).all()

        return scores

    def get_user_movies(self, username):
        """Get all movies in user chain"""

        movie_chain = db.session.query(Movie.name, User.name).\
            filter(User.movies).filter(User.name == username).all()
        
        return movie_chain

    def get_user_actors(self, username):
        """Get all actors in user chain"""

        actor_chain = db.session.query(Actor.name, User.name).\
            filter(User.actors).filter(User.name == username).all()

    def get_top_movies(self):
        """Get the most well-known movies"""

        top_movies = db.session.query(Movie.name, func.count(distinct(User.id))).\
            filter(User.movies).distinct().order_by(desc(func.count(distinct(User.id)))).\
            group_by(Movie.name).all()
        
        return top_movies

    def get_top_actors(self):
        """Get the most well-known actors"""

        top_actors = db.session.query(Actor.name, func.count(distinct(User.id))).\
            filter(User.actors).distinct().order_by(desc(func.count(distinct(User.id)))).\
            group_by(Actor.name).all()

        return top_actors
