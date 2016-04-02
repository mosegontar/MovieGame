import string
import MovieGame.tomatopicker as Picker

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

        guess = guess.lower()
        if guess in self.current_list.keys():

            if self.check_connections(guess):
                # If guess correct, but actor-movie connection already made, return with no strike penalty
                return False

            self.make_connection(guess)

            link = self.current_list.get(guess)
            fixed_link = Picker.fix_link(link)
            self.current = string.capwords(guess)
            self.chain.append(self.current)

            # Since we begin all games with a movie, we know which data to grab by length of chain
            if len(self.chain) % 2 == 0:
                self.current_list = Picker.get_films(fixed_link)
            else:
                self.current_list = Picker.get_cast(fixed_link) 

        else:

            self.strikes += 1

        return True       



