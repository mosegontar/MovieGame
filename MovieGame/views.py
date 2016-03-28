import os
import string

from flask import g, render_template, session, url_for, request, redirect, flash
from MovieGame import app
import MovieGame.tomatopicker as Picker
from MovieGame.game import Game
import MovieGame.genres as genres

from MovieGame.record_keeper import Processor 


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
        if 'gameover' in session.keys(): 
            session.clear()

        # Before each request, initialize a new Game object and store on g 
        g.game = Game()

        # Begin game with random movie selected from 'starting_genres'
        if 'current' not in session.keys() or 'restart' in session.keys():
            
            if 'restart' in session.keys(): 
                del session['restart']                 

            try:
                g.game.current, g.game.current_list = Picker.begin(session['starting_genres'])
            except KeyError:
                return redirect(url_for('start'))
            
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
        
        if not choices or request.form['name'].strip() == '':
            session.clear()
            flash("Remember to select at least one category and to enter your name!")
            return render_template('start.html', all_genres=genres.genres)

        starting_genre_links = []

        for num in choices:
            starting_genre_links.append(genres.genres[num][1])

        session['name'] = request.form['name'].strip()
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

        if 'recent_guess' in session.keys():
            if session['recent_guess'] == guess:
                return redirect(url_for('game'))

        if guess == '' or string.capwords(guess) == g.game.current:
            flash("You didn't guess who is in {}".format(string.capwords(g.game.current)))
        else:            
            valid_guess = g.game.check_guess(guess)

            if not valid_guess:
                flash("You've already made a connection between {} and {}".format(string.capwords(guess), g.game.current))
        
        session['recent_guess'] = guess


        # Now update the session variables with the latest game state 
        update_session(g.game.connections, 
                       g.game.chain, 
                       g.game.current, 
                       g.game.current_list,
                       g.game.strikes)

    if session['strikes'] < 3:

        game_url = 'game_play.html'

    else:

        game_url = 'game_over.html'
        session['gameover'] = True


    return render_template(game_url, 
                           current=session['current'],
                           chain = session['chain'][::-1], 
                           score=session['score'], 
                           strikes=session['strikes'],
                           colors=colors,
                           name=session['name'])

@app.route('/test')
def test():
    g.entry = Processor()

    g.entry.add_user('Alice', 5, ["Good Will Hunting", "Matt Damon", "The Departed", "mark whalberg", "ted"])   
    g.entry.add_user('Bob', 4, ["Good Will", "Matt Damon", "Good Will", "Ben Affleck"])
    g.entry.add_user('Casey', 5, ["Trading Places", "Eddie Murphy", "The Departed", "Matt Damon", "The Martian"])
    g.entry.add_user('David', 1, ["Hercules", "Ben Affleck"])

    scores = g.entry.get_high_scores()
    print(scores)
    return 'hi'

