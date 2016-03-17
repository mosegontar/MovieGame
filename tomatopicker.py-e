import random
import re

import requests
from bs4 import BeautifulSoup

def get_title(page):
    """Given a movie's RT page, get the movie title"""

    page = BeautifulSoup(page.text, 'lxml')

    # this is where the movie title is located on a movie's RT page:
    title = page.find("meta", attrs={'name': 'movieTitle'})
    try:
        return title['content']
    except:
        return False

def get_films(actor_url):
    """Given an actor's RT page, get filmography"""

    page = requests.get(actor_url)
    films_div = BeautifulSoup(page.text, 'lxml').find('div', id='filmography_box')

    # Movie page URLs on RT begin with /m/. Use regex to find all such URLs.
    film_links = films_div.find_all('a', href=re.compile("/m/.*"))
    
    # Create a dictionary for all films, with the film name as the key
    # and the film's URL as the value
    films = {}
    for link in film_links:
        films[link.text.lower().strip()] = link['href']
    
    return films
        
def fix_link(link):
    """Check if link format is correct; if not, fix"""

    if link.startswith('http://www.rottentomatoes.com/'):
        fixed_link = link
    else:
        fixed_link = 'http://www.rottentomatoes.com' + link

    return fixed_link

def get_cast(movie_url):
    """Given a movie's RT page, get cast list"""

    page = requests.get(movie_url)
    
    cast_div = BeautifulSoup(page.text, 'lxml').find('div', class_='castSection')
    
    # if the castSection div is not found, return False
    if not cast_div:
        return False

    # Actor page URLs on RT begin with /celebrity/. Use regex to find all such URLs.
    cast_links = cast_div.find_all('a', href=re.compile("/celebrity/.*"))

    # Create a dictionary for all cast members, with each actor name as the keys
    # and the actor's URL as the value
    cast = {}
    for c in cast_links:
        if c.span:
            name = c.span['title']
            cast[name.lower().strip()] = c['href']

    return cast

def begin(urls=["http://www.rottentomatoes.com/top"]):
    """Find a random movie and its cast to begin game"""

    movie_links = [] 
    for url in urls:
        fixed_url = fix_link(url)
        top_movies = requests.get(fixed_url)
        soupy_links = BeautifulSoup(top_movies.text, 'lxml').find('table', class_='table').find_all('a', href=re.compile("/m/.*"))
        movie_links = movie_links + list(soupy_links)


    random_movie_link = random.choice(list(set(movie_links)))['href'].split('/news/')[0]
    
    link = fix_link(random_movie_link)

    movie_page = requests.get(link)

    title = get_title(movie_page)
    cast = get_cast(link)

    # if a title or cast is not found, try again
    if not title or not cast:
        begin()
    else:
        return (title, cast)





