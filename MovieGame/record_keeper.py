from MovieGame import app, db
from MovieGame.models import *

class Processor(object):

    def __init__(self):
        db.create_all()

    def add_user(self, name, strikes, chain):

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
        scores = db.session.query(User.name, User.score).\
            order_by(desc(User.score)).group_by(User.name).all()


        return scores


"""

def do_it():
    p = Processor()

    p.add_user('Alice', 5, ["Good Will Hunting", "Matt Damon", "The Departed", "mark whalberg", "ted"])   
    p.add_user('Bob', 4, ["Good Will", "Matt Damon", "Good Will", "Ben Affleck"])
    p.add_user('Casey', 5, ["Trading Places", "Eddie Murphy", "The Departed", "Matt Damon", "The Martian"])
    p.add_user('David', 1, ["Hercules", "Ben Affleck"])
    x  = db.session.query(Movie.name, User.name).filter(User.movies).filter(User.name == 'Bob').all()
    print(x)
    x  = db.session.query(Movie.name, func.count(Movie.name)).distinct().filter(User.movies).distinct().order_by(desc(func.count(Movie.name))).group_by(Movie.name).all()
    print(x)
    x  = db.session.query(Movie.name, User.name).filter(User.movies).distinct().all()
    print(x)
    y = db.session.query(Movie.name, func.count(distinct(User.id))).filter(User.movies).distinct().order_by(desc(func.count(distinct(User.id)))).group_by(Movie.name).all()
    print(y)

    print()
"""
