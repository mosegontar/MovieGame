import random
import re

import requests
from bs4 import BeautifulSoup


class Retriever(object):
    """Retriever object gets data from Rottentomatoes.com and updates game stats"""

    def __init__(self):
        """Retriever object is initialized""" 

        self.chain = []
        self.score = len(self.chain)

        self.strikes = 0

        self.name = None
        self.name_dict = None


    def get_title(self, page):
        """Given a movie's RT page, get the movie title"""

        page = BeautifulSoup(page.text, 'lxml')

        # this is where the movie title is located on a movie's RT page:
        title = page.find("meta", attrs={'name': 'movieTitle'})
        try:
            return title['content']
        except:
            return False

    def get_films(self, actor_url):
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
            
    def fix_link(self, link):
        """Check if link format is correct; if not, fix"""

        if link.startswith('http://www.rottentomatoes.com/'):
            fixed_link = link
        else:
            fixed_link = 'http://www.rottentomatoes.com' + link

        return fixed_link

    def get_cast(self, movie_url):
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
            cast[c.text.lower().strip()] = c['href']

        return cast

    def start_at_top(self, urls):
        """Find a random movie and its cast to begin game"""

        movie_links = [] 
        for url in urls:
            top_movies = requests.get(url)
            soupy_links = BeautifulSoup(top_movies.text, 'lxml').find_all('a', href=re.compile("/m/.*"))
            movie_links = movie_links + list(soupy_links)


        random_movie_link = random.choice(list(set(movie_links)))['href'].split('/news/')[0]
        
        link = self.fix_link(random_movie_link)

        movie_page = requests.get(link)


        title = self.get_title(movie_page)
        cast = self.get_cast(link)

        # if a title or cast is not found, try again
        if not title or not cast:
            self.start_at_top()
        else:
            self.name = title
            self.name_dict = cast






