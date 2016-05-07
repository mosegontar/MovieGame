from MovieGame import app, db
from MovieGame.models import Users, Choices, Games
from sqlalchemy import Enum, desc

def get_current(game):
    """Get current chain head as a Choices object."""
    if not game:
        return None
    else:
        chain_head = game[-1][-1]
        current = Choices.query.get(chain_head)
        return current


def get_connection(game):
    """Create & return dictionary of all relationships in a game's rounds"""
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
    """Check if a connection exists between user guess and game chain head."""
    if not game:
        return False
    else:        
        current = get_current(game).name
        connections = get_connection(game)

        if guess.lower() in connections[current]:
            return True
        else:
            return False


def get_chain(game):
    """Get the game chain (the list of user answers)."""
    if not game:
        chain = []
    else:
        first_item = Choices.query.get(game[0][1]).name
        chain = [Choices.query.get(round_num[2]).name for round_num in game]
        chain.insert(0, first_item)

    return chain


def get_user_data(user_id):
    """Return a user based on primary key as a Users object."""
    user_entry = Users.query.filter(Users.id == user_id).first()

    return user_entry


def get_game(user_id):
    """Get the Games object based on a user_id."""
    game = db.session.query(Games.round_number, Games.parent_id, Games.child_id).\
        filter(Games.user_id == user_id).all()

    return game


def update_user(user_id, new_strike):
    """Update an existing user's data."""
    user = get_user_data(user_id)

    game = get_game(user_id)
    chain_length = len(get_chain(game))

    user.score = chain_length

    if new_strike:
        user.strikes += 1

    db.session.commit()


def add_user(name):
    """Add a user to the db."""
    user = Users(username=name)
    db.session.add(user)
    db.session.commit()
    return user.id


def add_round(user_id, round_number, parent_id, child_id):
    """Add a round entry to the a particular game."""
    round_entry = Games(user_id=user_id,
                        round_number=round_number,
                        parent_id=parent_id,
                        child_id=child_id)

    db.session.add(round_entry)
    db.session.commit()

def get_choice_data(name):
    """Get existing Choices object based on actor or movie name."""
    choice = Choices.query.filter_by(name=name).first()
    return choice


def add_choice(name, moviedb_id, choice_type):
    """Add choice (actor or movie) to database."""
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
    """Get high scores."""
    scores = Users.query.filter(Users.score > 1).\
        order_by(desc(Users.score)).all()

    return scores

def test():
    
    gwh = Choices(name="Good Will Hunting",
                  moviedb_id=6,
                  choice_type="movie")
    db.session.add(gwh)

    bi = Choices(name="The Bourne Identity",
                 moviedb_id=7,
                 choice_type="movie")

    db.session.add(bi)

    db.session.commit()

    movies = {"Good Will Hunting": [("Matt Damon", 1, "actor"), 
                                    ("Ben Afleck", 2, "actor"), 
                                    ("Robin Williams", 3, "actor")],
              "The Bourne Identity":[("Bourne Actor 1", 4, "actor"), 
                                     ("Matt Damon", 1, "actor"), 
                                     ("Bourne Actor 2", 5, "actor")]}

    for movie_name in movies.keys():
        exists = Choices.query.filter(Choices.name == movie_name).first()
        if exists:
            actors = movies.get(movie_name)
            for name, movie_id, choice_type in actors:
                print(name, movie_id, choice_type)
                actor = Choices(name=name,
                                moviedb_id=movie_id,
                                choice_type=choice_type)
                db.session.add(actor)
                db.session.commit()

                print(actor.name, "is an actor")
                mov = exists
                mov.connections.append(actor)
                db.session.add(mov)
                db.session.commit()
                for m in mov.connections:
                    print(mov.name, "contains", m.name)

    matt_damon = Choices.query.filter(Choices.name == "Matt Damon").first()
    print("Matt Damon's name is {}".format(matt_damon.name))
    print(len(matt_damon.connections))
    for movi in matt_damon.connections:
        print(movi.name, "stars", matt_damon.name)



