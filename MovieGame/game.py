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

def get_current_relations(current):
    """Return the list of associated relations for the current item (head of chain)"""
    current_relations = dict([(c.name.lower(), c.moviedb_id) for c in current.relations])

    if len(list(current_relations)) == 0:
        if current.choice_type == "movie":
            temp_list = MovieAPI.get_cast(current.moviedb_id)
        else:
            temp_list = MovieAPI.get_films(current.moviedb_id)

        ViewModel.add_relation(current, temp_list)
        current_relations = dict([(c.name.lower(), c.moviedb_id) for c in current.relations])
    else:
        pass

    return current_relations

def check_guess(user_id, current, game, guess):
    """Check whether a guess is correct or not; return with or w/o strike."""
    user = ViewModel.get_user_data(user_id)
    
    current_relations = get_current_relations(current)
    
    guess = guess.lower()
    if guess == current.name.lower():
        return False

    if guess in current_relations:

        new_strike = False

        connection = ViewModel.check_connection(guess, game)

        if connection:  return False

        chain = ViewModel.get_chain(game)
        round_number = len(game) + 1

        parent = current
        child  = ViewModel.get_choice_data(guess)

        ViewModel.add_round(user.id, round_number, parent.id, child.id)        

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
        
