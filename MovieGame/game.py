from flask import session, redirect, url_for

from MovieGame import app, db
import MovieGame.movie_info as MovieAPI
import MovieGame.viewmodel as ViewModel 

def get_random_movie(starting_genres):
    random_movie = MovieAPI.get_random_movie(starting_genres)
    session['starting_movie'] = random_movie

def update_game_state(user_id, game):
    """Update Game object data."""
    game = ViewModel.get_game(user_id)
    current = ViewModel.get_current(game)
    chain = ViewModel.get_chain(game)

    if not game:
        movie = session['starting_movie']
        current =  ViewModel.get_choice_data(movie['title'].lower())
    else:
        pass

    return (game, current, chain)

def check_guess(user_id, current, game, guess):
    """Check whether a guess is correct or not; return with or w/o strike."""
    user = ViewModel.get_user_data(user_id)

    if current.choice_type == "movie":
        current_list = MovieAPI.get_cast(current.moviedb_id)
    else:
        current_list = MovieAPI.get_films(current.moviedb_id)
    
    guess = guess.lower()
    if guess == current.name.lower():
        return False

    if guess in current_list.keys():

        new_strike = False

        connection = ViewModel.check_connection(guess, game)

        if connection:  return False

        chain = ViewModel.get_chain(game)
        round_number = (len(game) / 2) + 1

        parent = current.id

        guess_entry = ViewModel.get_choice_data(guess)
        if not guess_entry:

            moviedb_id = current_list.get(guess)
            choice_type = ['actor', 'movie'][['actor', 'movie'].index(current.choice_type) - 1] 
            choice = ViewModel.add_choice(guess, moviedb_id, choice_type)
            child = choice.id

        else:
            child = guess_entry.id

        ViewModel.add_round(user.id, round_number, parent, child)        

    else:
        new_strike = True

    ViewModel.update_user(user.id, new_strike)
    db.session.commit()
    return True


def prepare_game(restart):
    """Update game state before each request."""
    if 'user_id' in session.keys():

        user = ViewModel.get_user_data(session['user_id'])
        game = ViewModel.get_game(user.id)

        if not game or restart:
            movie = session['starting_movie']
            current = ViewModel.add_choice(movie['title'], movie['id'], "movie")
            chain = []
        else:
            chain = ViewModel.get_chain(game)
            current = ViewModel.get_current(game)

        return (user, game, current, chain)

    else:
        return redirect(url_for('start'))
        
