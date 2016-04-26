import string
import MovieGame.movie_info as MovieAPI

class Game(object):
    """Game object updates and keeps current game state (score, chain, etc) and validates guesses"""

    def __init__(self):
        """Retriever object is initialized""" 

        self.connections = {}
        self.chain = []
        self.score = len(self.chain)

        self.strikes = 0

        self.current = None
        self.current_list = None

    def check_connections(self, guess):
        """Check whether an actor-movie connection has already been established"""

        if guess.lower() in self.connections[self.current.lower()]:
            return True
        else:
            return False

    def make_connection(self, guess):
        """Records an actor-movie connection"""

        parent = self.current.lower()
        child = guess

        self.connections.setdefault(parent, []).append(child)
        self.connections.setdefault(child, []).append(parent)


    def check_guess(self, guess):
        """Checks user guess and updates game state """
        
        # user = get user

        guess = guess.lower()

        """ 
        current = get current
        if current.choice_type == "movie":
            current_list = MovieAPI.get_cast(current.moviedb_id)
        else:
            current_list = MovieAPI.get_films(current.moviedb_id)

        if guess in current_list.keys():
            # check connections
            ## if guess is correct, but actor-movie connection already made, return with no strike penalty
                return False

            now add entry:
                round_entry = Games(user_id=user.id,
                                    user_game_number=user.game_number, 
                                    round_number=index, 
                                    parent_id=parent_entry.id, 
                                    child_id=child_entry.id) 

                db.session.add(round_entry)



        else:
            update user with strike

        db.session.commit()
        return True



        """

        if guess in self.current_list.keys():

            if self.check_connections(guess):
                # If guess is correct, but actor-movie connection already made, return with no strike peanlty
                return False
        
            self.make_connection(guess)

            value_id = self.current_list.get(guess)

            self.current = string.capwords(guess)
            self.chain.append(self.current)

            if len(self.chain) % 2 == 0:
                self.current_list = MovieAPI.get_films(value_id)
            else:
                self.current_list = MovieAPI.get_cast(value_id)
        else:

            self.strikes += 1

        return True

