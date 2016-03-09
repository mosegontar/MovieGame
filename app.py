import os

import data_getter
from flask import Flask, render_template, sessions, url_for

app = Flask(__name__)

# Config
SECRET_KEY = 'secretkey'
app.config.from_object(__name__)

@app.route('/')
def main():
	movie = data_getter.start_at_top()
	title = data_getter.get_title(movie)
	return render_template('base.html', current=title)

if __name__ == '__main__':
	app.run(debug=True)
