from MovieGame import app, db
from MovieGame.models import *


def do_it():
    db.create_all()
    process('Alice', 2, 'Good Will', "Movie")   
    process('Bob', 3, "Good Will", "Movie", "Good Will", "J Park")
    process('Casey', 4, "Good Will", "J Park", "Alfredo", "Alfredo", "Alfredo")
    process('David', 1, "Good Will", "J Park", "Alfredo")
    x  = db.session.query(Movie.name, User.name).filter(User.movies).filter(User.name == 'Bob').all()
    print(x)
    x  = db.session.query(Movie.name, func.count(Movie.name)).distinct().filter(User.movies).distinct().order_by(desc(func.count(Movie.name))).group_by(Movie.name).all()
    print(x)
    x  = db.session.query(Movie.name, User.name).filter(User.movies).distinct().all()
    print(x)
    y = db.session.query(Movie.name, func.count(distinct(User.id))).filter(User.movies).distinct().order_by(desc(func.count(distinct(User.id)))).group_by(Movie.name).all()
    print(y)

    print(db.session.query(User.name, User.score).order_by(desc(User.score)).group_by(User.name).all())
