import random
from datetime import date

#from MovieGame import app
import tmdbsimple as tmdb

tmdb.API_KEY = 'app.config[API_KEY]' #app.config['API_KEY']

def format_date(year, month, day):
    """format date"""

    year = str(year)
    month = str(month)
    day = str(month)

    formatted_date = year + '-' + month + '-' + day
    
    return formatted_date

def get_genres():
    """Get genres from themoviedb.org api"""

    genres = sorted(tmdb.Genres().list()['genres'], key=lambda genre: genre['name'])

    return genres

def get_random_movie(min_year=None, max_year=None, genres=None):
    """Get a random movie based on user input"""

    if not min_year:
        min_year = format_date(date.today().year-50, 1, 1) 
    else:
        min_year = format_date(min_year, 12, 31)

    if not max_year:
        max_year = format_date(date.today().year, date.today().month, date.today().day)
    else:
        max_year = format_date(max_year, 12, 31)

    discover = tmdb.Discover()
    search_results = []
    
    for i in range(1,6):
        
        search_parameters = {'sort_by': 'popularity.desc', 'release_date.gte': min_year, 'release_date.lte': max_year, 'page': i, 'with_genres': genres}
        response = discover.movie(**search_parameters)
        results = response['results']

        for movie in results:
            search_results.append(movie)

    return random.choice(search_results)

def get_cast(movie_id):

    movie = tmdb.Movies(movie_id)
    cast = movie.credits()['cast']
    
    return cast

def get_films(actor_id):
    
    actor = tmdb.People(actor_id)
    films = actor.movie_credits()['cast']

    return films









    


