import random
import re

import requests
from bs4 import BeautifulSoup


class Retreiver(object):

    def __init__(self):
        
        self.chain = []
        self.score = len(self.chain)

        self.strikes = 0

        self.name = None
        self.name_dict = None
        self.url = None


    def get_title(self, page):
        page = BeautifulSoup(page.text, 'lxml')
        title = page.find("meta", attrs={'name': 'movieTitle'})
        try:
            return title['content']
        except:
            return False

    def get_films(self, actor_url):
        print(actor_url)
        page = requests.get(actor_url)
        films_div = BeautifulSoup(page.text, 'lxml').find('div', id='filmography_box')
        film_links = films_div.find_all('a', href=re.compile("/m/.*"))
        
        films = {}
        for link in film_links:
            films[link.text.lower().strip()] = link['href']
        
        return films
            
    def fix_link(self, link):
        if link.startswith('http://www.rottentomatoes.com/'):
            fixed_link = link
        else:
            fixed_link = 'http://www.rottentomatoes.com' + link

        return fixed_link

    def get_cast(self, movie_url):
        page = requests.get(movie_url)
        cast_div = BeautifulSoup(page.text, 'lxml').find('div', class_='castSection')
        if not cast_div:
            return False
        cast_links = cast_div.find_all('a', href=re.compile("/celebrity/.*"))

        cast = {}
        for c in cast_links:
            cast[c.text.lower().strip()] = c['href']

        return cast

    def start_at_top(self):

        top_movies = requests.get('http://www.rottentomatoes.com/top')
        soupy_links = BeautifulSoup(top_movies.text, 'lxml').find_all('a', href=re.compile("/m/.*"))
        random_movie_link = random.choice(soupy_links)['href']
        
        random_movie_link = self.fix_link(random_movie_link)

        movie_page = requests.get(random_movie_link)


        title = self.get_title(movie_page)
        cast = self.get_cast(random_movie_link)
        
        if not title or not cast:
            self.start_at_top()
        else:
            self.name = title
            self.name_dict = cast

        

r = Retreiver()
r.start_at_top()
while r.strikes <= 3:

    print(r.name)
    choice = input("> ").strip()
    if choice.lower() in r.name_dict.keys():
        print(True)
        r.name = choice.title()
        name_link = r.name_dict.get(choice.lower())
        name_link = r.fix_link(name_link)
        r.chain.append(r.name)

        if len(r.chain) % 2 == 0:
            r.name_dict = r.get_cast(name_link)
        else:
            r.name_dict = r.get_films(name_link)
    else:
        print("SORRY :(")
        r.strikes += 1

    r.score += 1





""""
# Movie name | cast list
> actor guess
if actor in cast list, return 
# Actor name | filmography
> film guess
if film in filmography, return
# Movie name | cast list
> actor guess
if ....
"""





