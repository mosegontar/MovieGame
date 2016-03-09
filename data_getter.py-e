import random
import re

import requests
from bs4 import BeautifulSoup

def get_title(page):
    page = BeautifulSoup(page.text, 'lxml')
    title = page.find("meta", attrs={'name': 'movieTitle'})
    return title['content']

def get_films(actor_url):
    print('get_films function', actor_url)
    page = requests.get(actor_url)
    films_div = BeautifulSoup(page.text, 'lxml').find('div', id='filmography_box')
    film_links = films_div.find_all('a', href=re.compile("/m/.*"))
    
    films = {}
    for link in film_links:
        films[link.text.strip()] = link['href']
    
    return films
        
def fix_link(link):
    print(link, "fixing!")
    if link.startswith('http://www.rottentomatoes.com/'):
        fixed_link = link
    else:
        fixed_link = 'http://www.rottentomatoes.com' + link

    return fixed_link

def get_cast(movie_url):
    page = requests.get(movie_url)
    cast_div = BeautifulSoup(page.text, 'lxml').find('div', class_='castSection')
    cast_links = cast_div.find_all('a', href=re.compile("/celebrity/.*"))

    cast = {}
    for c in cast_links:
        cast[c.text.strip()] = c['href']

    return cast

def start_at_top():

    top_movies = requests.get('http://www.rottentomatoes.com/top')
    soupy_links = BeautifulSoup(top_movies.text, 'lxml').find_all('a', href=re.compile("/m/.*"))
    random_movie_link = random.choice(soupy_links)['href']
    
    random_movie_link = fix_link(random_movie_link)

    movie_page = requests.get(random_movie_link)

    title = get_title(movie_page)
    cast = get_cast(random_movie_link)

    return (random_movie_link, title)



def check_filmography(lst, query):

    sanit_q = query.lower().strip()

    try:
        return films.get(query)
    except:
        return False
        

def main():

    start = start_at_top()
    print(start[1])
    start = start[0]

    count = 0
    while True:
        print(start, "start")
        names = get_cast(start)
        a = ''
        for c in names.keys():
            if len(c) > 3:
                a = c
                print(c)
                name_link = fix_link(names.get(c))
                break

        films = get_films(name_link)

        b = ''
        film_link = None
        for f in films.keys():
            if (len(f) > 3 and f != c):
                b = f
                print(f)
                print(f, names.keys())
                film_link = fix_link(names.get(f.lower))
                print(film_link, "film link")
                break

        if film_link:
             names = get_cast(film_link)
        else:
            return
        
        a = ''
        for c in names.keys():
            if len(c) > 3 and c != b:
                a = c
                print(c)
                name_link = fix_link(names.get(c))
                break

        films = get_films(name_link)

        for f in films.keys():
            if len(f) > 3 and f != a:
                print(f,a)
                b = f
                print(f)
                film_link = fix_link(names.get(c))
                break

        break
        count += 1

main()





