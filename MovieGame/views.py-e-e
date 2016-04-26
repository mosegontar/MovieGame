import os
import string

from flask import g, render_template, session, url_for, request, redirect, flash
from MovieGame import app, db
import MovieGame.movie_info as MovieAPI

import MovieGame.viewmodel as VM

def update_game_state(user_id, game):

    game = VM.get_game(user_id)
    current = VM.get_current(game)
    chain = VM.get_chain(game)

    return (game, current, chain)

def check_guess(user_id, current, game, guess):
    
    guess = guess.lower()
    user = VM.get_user_data(user_id)

    if current.choice_type == "movie":
        current_list = MovieAPI.get_cast(current.moviedb_id)
    else:
        current_list = MovieAPI.get_films(current.moviedb_id)

    if guess in current_list.keys():

        new_strike = False

        connection = VM.check_connection(guess, game)

        if connection:  return False

        chain = VM.get_chain(game)
        round_number = (len(chain) / 2) + 1

        parent = current.id

        guess_entry = VM.get_choice_data(guess)
        if not guess_entry:

            name = guess
            moviedb_id = current_list.get(name)
            choice_type = ['actor', 'movie'][['actor', 'movie'].index(current.choice_type) - 1]
            choice = VM.add_choice(name, moviedb_id, choice_type)
            child = choice.id

        else:
            child = guess_entry.id

        VM.add_round(user_id, user.game_number, round_number, parent, child)        

    else:
        new_strike = True

    VM.update_user(user_id, new_strike)
    db.session.commit()
    return True


@app.route('/test')
def test():
    """ """
    scores = VM.get_high_scores()
    print(scores)
    return 'hi'

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')    
   
@app.route('/', methods=['GET', 'POST'])
def start():
    """On GET request, displays various genres from which user can choose to begin game,
    On POST request, generates list of top 100 movies from each chosen genre
    """

    genres_list = MovieAPI.get_genres()

    if request.method == 'POST':

        choices = [int(index) for index in request.form.getlist('genres')]
        
        if not choices or request.form['name'].strip() == '':
            flash("Remember to select at least one category and to enter your name!")
            return render_template('start.html', all_genres=genres_list)
        
        starting_genre_ids = []
        for num in choices:
            starting_genre_ids.append(num)

        random_movie = MovieAPI.get_random_movie(starting_genre_ids)
        session['starting_movie'] = random_movie

        username = request.form['name'].strip()
        session['user_id'] = VM.add_user(username)

        return redirect(url_for('game'))

    else:

        session.clear()
        return render_template('start.html', all_genres=genres_list)

def prepare_game():
    """Updates game state before each request"""

    if 'user_id' in session.keys():
    
        user = VM.get_user_data(session['user_id'])
        game = VM.get_game(user.id)

        if not game:
            movie = session['starting_movie']
            current = VM.add_choice(movie['title'], movie['id'], "movie")
            chain = []
        else:
            chain = VM.get_chain(game)
            current = VM.get_current(game)

        return (user, game, current, chain)

    else:
        return redirect(url_for('start'))

@app.route('/play', methods=['GET', 'POST'])
def game():
    """Runs game play"""

    user, game, current, chain = prepare_game()

    if request.method == 'POST':

        guess = request.form['answer'].strip()

        valid_guess = check_guess(user.id, current, game, guess)
        if not valid_guess:
            flash("You've already made a connection between {} and {}".format(string.capwords(guess), string.capwords(current.name)))

        game, current, chain = update_game_state(user.id, game)

    if user.strikes < 3:
        game_url = 'game_play.html'
    else:
        game_url = 'game_over.html'

    current = string.capwords(current.name)
    chain = [string.capwords(item) for item in chain]

    return render_template(game_url, 
                           current = current,
                           chain = chain[::-1], 
                           score = user.score, 
                           strikes = user.strikes,
                           name = user.username)



@app.route('/high-scores')
def high_scores():
    """Lists all high scores"""

    scores = VM.get_high_scores()

    return render_template('high_scores.html', scores=scores)

@app.route('/high-scores/user/<user_id>')
def user_high_score(user_id):
    """List chain and score for specific user"""

    movies = VM.get_user_movies(user_id)
    actors = VM.get_user_actors(user_id)

    chain = VM.make_complete_chain(movies, actors)

    username = movies[0][1]
    score = len(movies) + len(actors)

    return render_template('user_reel.html', username=username, chain=chain, score=score)
