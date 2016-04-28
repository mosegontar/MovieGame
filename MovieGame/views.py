import string

from flask import render_template, session, url_for, request, redirect, flash

from MovieGame import app
import MovieGame.movie_info as MovieAPI
import MovieGame.game as Game
import MovieGame.viewmodel as ViewModel


@app.route('/about')
def about():
    """About page."""
    return render_template('about.html')


@app.route('/', methods=['GET', 'POST'])
def start():
    """Starting Screen.

    GET: displays genres for selection.
    POST:generates list of top 100 movies from each chosen genre.
    """
    genres_list = MovieAPI.get_genres()

    if request.method == 'POST':

        choices = [int(index) for index in request.form.getlist('genres')]

        if not choices or request.form['name'].strip() == '':
            flash("Remember to select at least one category",
                  "and to enter your name!")
            return render_template('start.html', all_genres=genres_list)

        starting_genre_ids = []
        for num in choices:
            starting_genre_ids.append(num)

        random_movie = MovieAPI.get_random_movie(starting_genre_ids)
        session['starting_movie'] = random_movie

        username = request.form['name'].strip()
        session['user_id'] = ViewModel.add_user(username)

        return redirect(url_for('game'))

    else:

        session.clear()
        return render_template('start.html', all_genres=genres_list)


@app.route('/play', methods=['GET', 'POST'])
def game():
    """Run game play."""
    user, game, current, chain = Game.prepare_game()

    if request.method == 'POST':

        guess = request.form['answer'].strip()

        valid_guess = Game.check_guess(user.id, current, game, guess)
        if not valid_guess:
            flash("You've already made a connection between {} and {}".
                  format(string.capwords(guess),
                         string.capwords(current.name)))

        game, current, chain = Game.update_game_state(user.id, game)

    if user.strikes < 3:
        game_url = 'game_play.html'
    else:
        game_url = 'game_over.html'

    current = string.capwords(current.name)
    chain = [string.capwords(item) for item in chain]

    return render_template(game_url,
                           current=current,
                           chain=chain[::-1],
                           score=user.score,
                           strikes=user.strikes,
                           name=user.username)


@app.route('/high-scores')
def high_scores():
    """List all high scores."""
    scores = ViewModel.get_high_scores()

    return render_template('high_scores.html', scores=scores)


@app.route('/high-scores/user/<user_id>')
def user_high_score(user_id):
    """List chain and score for specific user."""
    user = ViewModel.get_user_data(user_id)
    game = ViewModel.get_game(user.id)
    chain = [string.capwords(item) for item in ViewModel.get_chain(game)]
    username = user.username
    score = user.score

    return render_template('user_reel.html',
                           username=username,
                           chain=chain,
                           score=score)
