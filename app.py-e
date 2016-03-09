import os

from data_getter import Retriever
from flask import Flask, g, render_template, session, url_for, request

app = Flask(__name__)


# Config
SECRET_KEY = 'secretkey'
app.config.from_object(__name__)

@app.before_request
def before_request():

    if 'gameover' in session.keys():
       session.clear()

    g.game = Retriever()

    if 'name' not in session.keys():
        g.game.start_at_top()
        session['chain'] = g.game.chain
        session['name'] = g.game.name
        g.game.chain.append(g.game.name)
        session['strikes'] = g.game.strikes
        session['score'] = g.game.score
        session['name_list'] = g.game.name_dict
    else:
        g.game.chain = session['chain']
        g.game.name = session['name']
        g.game.strikes = session['strikes']
        g.game.score = session['score']
        g.game.name_dict = session['name_list']



@app.route('/', methods=['GET', 'POST'])
def main():
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

        session['chain'] = g.game.chain
        session['name'] = g.game.name
        session['strikes'] = g.game.strikes
        session['score'] = g.game.score
        session['name_list'] = g.game.name_dict


    if session['strikes'] <= 3:
        
        return render_template('base.html', current=session['name'], chain=session['chain'][::-1])

    else:
        session['name'] = "Your score is %s and strikes: %s" % (len(session['chain'])-1, session['strikes'])
        session['gameover'] = True
        return render_template('base.html', current=session['name'], chain=session['chain'])



if __name__ == '__main__':
    app.run(debug=True)
