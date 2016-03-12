import string
import tomatopicker as Picker

class Game(object):
    """Retriever object gets data from Rottentomatoes.com and updates game stats"""

    def __init__(self):
        """Retriever object is initialized""" 

        self.connections = {}
        self.chain = []
        self.score = len(self.chain)

        self.strikes = 0

        self.current = None
        self.current_list = None

    def check_connections(self, guess):
        print(self.connections)
        if guess.lower() in self.connections[self.current.lower()]:
            return True
        else:
            return False

    def make_connection(self, guess):

        parent = self.current.lower()
        child = guess

        self.connections.setdefault(parent, []).append(child)
        self.connections.setdefault(child, []).append(parent)


    def check_guess(self, guess):

        guess = guess.lower()

        if guess in self.current_list.keys():

            if self.check_connections(guess):
                # If guess correct, but connection between actor--film already made, return with no penalty
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



"""
g = Game()

chain = ["Good Will Hunting", "Matt Damon", "Saving Private Ryan", "Tom Hanks", "You've Got Mail", "Meg Ryan", "Sleepless in Seattle", "Tom Hanks", "Catch Me if You Can", "Leonardo Dicaprio", "The Departed", "Matt Damon"]

for index in range(1, len(chain)):



g.current = chain[-1].lower()

g.check_connections('The Bourne Identity')

"""


