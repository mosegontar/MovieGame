import os

from data_getter import Retriever
from flask import Flask, g, render_template, session, url_for, request, redirect

app = Flask(__name__)


# Config
SECRET_KEY = '\xac\xd6z\xb3\xe4j&}\x120\xc71/{\xe4\x95\xa6\xdd_\x9e\x9e\xb1\xd3p'
app.config.from_object(__name__)

@app.before_request
def before_request(methods=['GET', 'POST']):
    """Updates game state before each request"""

    # if page is accessed after game is lost, clear session cookies for new game
    if 'gameover' in session.keys():
       session.clear()

    # before each request, initialize a new game object and store it on g 
    g.game = Retriever()

    # if a game is not already in progress, set session variables to game object's initial values
    if 'name' not in session.keys():
        g.game.start_at_top()
        session['chain'] = g.game.chain
        session['name'] = g.game.name
        g.game.chain.append(g.game.name)
        session['strikes'] = g.game.strikes
        session['score'] = len(session['chain']) - 1
        session['name_list'] = g.game.name_dict

    # if a game IS in progress, update the game object to the values stored in the session variables
    else:
        g.game.chain = session['chain']
        g.game.name = session['name']
        g.game.strikes = session['strikes']
        g.game.score = session['score']
        g.game.name_dict = session['name_list']


@app.route('/reset', methods=['POST'])
def reset():
    session['gameover'] = True
    return redirect(url_for('game'))

@app.route('/', methods=['GET', 'POST'])
def game():
    """Runs game play"""

    # At each POST request, run game play
    if request.method == 'POST':
        
        choice = request.form['answer'].strip()
        
        if choice.lower() in g.game.name_dict.keys():
        
            g.game.name = choice.title()
        
            link = g.game.name_dict.get(choice.lower())
            link = g.game.fix_link(link)
        
            g.game.chain.append(g.game.name)
            g.game.score += 1
        
            if len(g.game.chain) % 2 == 0:
                g.game.name_dict = g.game.get_films(link)
            else:
                g.game.name_dict = g.game.get_cast(link)
        else:
            g.game.strikes += 1

        # Now update the session variables with the lastest game state 
        session['chain'] = g.game.chain
        session['name'] = g.game.name
        session['strikes'] = g.game.strikes
        session['score'] = len(session['chain']) - 1
        session['name_list'] = g.game.name_dict


    # If game in progress, render game with latest state
    if session['strikes'] < 3:
        return render_template('base.html', current=session['name'], chain=session['chain'][::-1], score=session['score'], strikes=session['strikes'])

    # If game over (3 strikes), provide feedback and set session['gameover'] to True
    else:
        session['name'] = "Your score is %s and strikes: %s" % (session['score'], session['strikes'])
        session['gameover'] = True
        return render_template('base.html', current=session['name'], chain=session['chain'][::-1], score=session['score'], strikes=session['strikes'])



if __name__ == '__main__':
    app.run(debug=True)
