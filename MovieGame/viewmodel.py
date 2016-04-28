from MovieGame import app, db
from MovieGame.models import *

def get_current(game):

    chain_head = game[-1][-1]
    current = Choices.query.get(chain_head)
    return current

def get_connection(game):
    connections = {}
    for round_num in game:
        parent = Choices.query.get(round_num[1])
        child = Choices.query.get(round_num[2])

        connections.setdefault(parent.name.lower(), []).append(child.name.lower())
        connections.setdefault(child.name.lower(), []).append(parent.name.lower())

    # Let's remove any duplicate relationships
    unique_connections = dict([(key, list(set(value))) for key, value in connections.items()])

    return unique_connections

def check_connection(guess, game):

    if not game: return False

    current = get_current(game).name
    connections = get_connection(game)

    if guess.lower() in connections[current]:
        return True
    else:
        return False

def get_chain(game):

    if not game:
        chain = []
    else:
        first_item = Choices.query.get(game[0][1]).name
        chain = [Choices.query.get(round_num[2]).name for round_num in game]
        chain.insert(0, first_item)

    return chain

def get_user_data(user_id):

    user_entry = Users.query.filter(Users.id == user_id).first()

    return user_entry

def get_game(user_id):

    game = db.session.query(Games.round_number, Games.parent_id, Games.child_id).\
        filter(Games.user_id == user_id).all()

    return game

def update_user(user_id, new_strike):

    user = get_user_data(user_id)
    
    game = get_game(user_id)
    chain_length = len(get_chain(game))

    user.score = chain_length

    if new_strike:
        user.strikes += 1

    db.session.commit()

def add_user(name):

    user = Users(username=name)
    db.session.add(user)
    db.session.commit()
    return user.id

def add_round(user_id, user_game_number, round_number, parent_id, child_id):

    round_entry = Games(user_id=user_id,
                    user_game_number=user_game_number, 
                    round_number=round_number, 
                    parent_id=parent_id, 
                    child_id=child_id) 

    db.session.add(round_entry)
    db.session.commit()

def get_choice_data(name):
    choice = Choices.query.filter_by(name=name).first()
    return choice

def add_choice(name, moviedb_id, choice_type):

    name = name.lower()

    entry_exists = get_choice_data(name)

    if entry_exists:
        entry = entry_exists
    else:
        entry = Choices(name=name, moviedb_id=moviedb_id, choice_type=choice_type)
        db.session.add(entry)
        db.session.commit()

    return entry

def get_high_scores():
    """Get high scores"""

    scores = db.session.query(Users.id, Users.username, Users.score).\
        order_by(desc(Users.score)).all()

    return scores

def get_user_movies():
    """Get user reel"""

    movie_chain = db.session.query(Choices.name, User.name).\
        filter(User.movies).filter(User.id == user_id).all()
    return movie_chain

