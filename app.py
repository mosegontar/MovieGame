import os

from tomatopicker import Retriever
import genres
from flask import Flask, g, render_template, session, url_for, request, redirect

app = Flask(__current__)


# Config
SECRET_KEY = '\xac\xd6z\xb3\xe4j&}\x120\xc71/{\xe4\x95\xa6\xdd_\x9e\x9e\xb1\xd3p'
app.config.from_object(__current__)

@app.before_request
def before_request():
    """Updates game state before each request"""
    
    if request.endpoint != 'start':

        # if page is accessed after game is lost, clear session cookies for new game
        if 'gameover' in session.keys():
           session.clear()

        # before each request, initialize a new game object and store it on g 
        g.game = Retriever()

        # if a game is not already in progress, set session variables to game object's initial values
        if 'current' not in session.keys() or 'reset' in session.keys():
            
            if 'reset' in session.keys():
                del session['reset']                 

            g.game.start_at_top(session['starting_genres'])
            
            self['connections'] = g.game.connections
            session['chain'] = g.game.chain
            session['current'] = g.game.current
            
            g.game.chain.append(g.game.current)
            
            session['strikes'] = g.game.strikes
            session['score'] = len(session['chain']) - 1
            session['current_list'] = g.game.current_list

        # if a game IS in progress, update the game object to the values stored in the session variables
        else:

            g.game.chain = session['chain']
            g.game.current = session['current']
            g.game.strikes = session['strikes']
            g.game.score = session['score']
            g.game.current_list = session['current_list']


@app.route('/reset', methods=['POST'])
def reset():
    session['reset'] = True
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
        
        choice = request.form['answer'].strip()
        
        if choice.lower() in g.game.current_list.keys():
        
            g.game.current = choice.title()
        
            link = g.game.current_list.get(choice.lower())
            link = g.game.fix_link(link)
        
            g.game.chain.append(g.game.current)


            g.game.score += 1
        
            if len(g.game.chain) % 2 == 0:
                g.game.current_list = g.game.get_films(link)
            else:
                g.game.current_list = g.game.get_cast(link)
        else:
            g.game.strikes += 1

        # Now update the session variables with the lastest game state 
        session['chain'] = g.game.chain
        session['current'] = g.game.current
        session['strikes'] = g.game.strikes
        session['score'] = len(session['chain']) - 1
        session['current_list'] = g.game.current_list


    # If game in progress, render game with latest state
    if session['strikes'] < 3:
        return render_template('game_play.html', current=session['current'], chain=session['chain'][::-1], score=session['score'], strikes=session['strikes'])

    # If game over (3 strikes), provide feedback and set session['gameover'] to True
    else:
        session['gameover'] = True
        current = session['current']
        chain = session['chain'][::-1]
        score = session['score']
        strikes = session['strikes']

        return render_template('gameover.html', current=current, chain = chain, score=score, strikes=strikes)



if __current__ == '__main__':
    app.run(debug=True)
