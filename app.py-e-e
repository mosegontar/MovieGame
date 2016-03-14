import os
import string

import tomatopicker as Picker
from engine import Game
import genres
from flask import Flask, g, render_template, session, url_for, request, redirect, flash

app = Flask(__name__)

# Config
SECRET_KEY = '\xac\xd6z\xb3\xe4j&}\x120\xc71/{\xe4\x95\xa6\xdd_\x9e\x9e\xb1\xd3p'
app.config.from_object(__name__)

def update_session(connections, chain, current, current_list, strikes):
    """Update session keys with current game state"""

    session['connections'] = connections
    session['chain'] = chain
    session['current'] = current
    session['current_list'] = current_list
    session['strikes'] = strikes
    session['score'] = len(session['chain']) - 1

@app.before_request
def before_request():
    """Updates game state before each request"""
    
    if request.endpoint == 'game':

        # If page is accessed after game is lost, clear session cookies for new game
        if 'gameover' in session.keys(): session.clear()

        # Before each request, initialize a new Game object and store on g 
        g.game = Game()

        # If a game is not already in progress or game reset, 
        # set session variables to game object's initial values
        if 'current' not in session.keys() or 'restart' in session.keys():
            
            if 'restart' in session.keys(): del session['restart']                 

            g.game.current, g.game.current_list = Picker.begin(session['starting_genres'])
            
            g.game.connections.setdefault(g.game.current.lower(), [])
            g.game.chain.append(g.game.current)
            update_session(g.game.connections, 
                           g.game.chain, 
                           g.game.current, 
                           g.game.current_list,
                           g.game.strikes)

        # If a game IS in progress, update the game object to the values stored in the session variables
        else:
            g.game.connections = session['connections']
            g.game.chain = session['chain']
            g.game.current = session['current']
            g.game.strikes = session['strikes']
            g.game.score = session['score']
            g.game.current_list = session['current_list']

    else:
        pass


@app.route('/restart', methods=['POST'])
def restart():
    """Restart game with random movie from previously chosen pool""" 

    session['restart'] = True
    return redirect(url_for('game'))
    
@app.route('/', methods=['GET', 'POST'])
def start():
    """On GET request, displays various genres from which user can choose to begin game,
    On POST request, generates list of top 100 movies from each chosen genre
    """

    if request.method == 'POST':

        choices = [int(index) for index in request.form.getlist('genres')]
        starting_genre_links = []

        for num in choices:
            starting_genre_links.append(genres.genres[num][1])

        session['starting_genres'] = starting_genre_links

        return redirect(url_for('game'))

    else:

        session.clear()
        return render_template('start.html', all_genres=genres.genres)


@app.route('/play', methods=['GET', 'POST'])
def game():
    """Runs game play"""
    
    # At each POST request, run game play
    if request.method == 'POST':

        guess = request.form['answer'].strip()
        valid_guess = g.game.check_guess(guess)

        if not valid_guess:
            flash("You've already made a connection between {} and {}".format(string.capwords(guess), g.game.current))

        # Now update the session variables with the latest game state 
        update_session(g.game.connections, 
                       g.game.chain, 
                       g.game.current, 
                       g.game.current_list,
                       g.game.strikes)

    if session['strikes'] < 3:
        game_url = 'game_play.html'

    else:
        session['gameover'] = True
        game_url = 'gameover.html'

    return render_template(game_url, 
                           current=session['current'],
                           chain = session['chain'][::-1], 
                           score=session['score'], 
                           strikes=session['strikes'])


if __name__ == '__main__':
    app.run(debug=True)
