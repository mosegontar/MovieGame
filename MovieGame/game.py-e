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

        guess = guess.lower()

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


        """
        print("self.current = ", self.current)
        print(self.current_list)

        if len(self.chain) % 2 == 0:
            found = False
            for movie in self.current_list:
                if guess == movie['title'].lower():
                    id_num = movie['id']
                    working_list = MovieAPI.get_cast(id_num)
                    found = True
                    print(movie['title'], "TITLE")
                    break
            if found:
                self.current_list = working_list[0:3]
                print(self.current_list)
            else:
                self.current_list ="NADA"

        else:
            for actor in self.current_list:
                found = False
                if guess == actor['name'].lower():
                    id_num = actor['id']
                    working_list = MovieAPI.get_films(id_num)
                    found = True
                    print(actor['name'], "NAME")
                    break
            if found:
                self.current_list = working_list[0:3]
                print(self.current_list)
            else:
                self.current_list ="NADA"


        self.current = guess
        self.chain.append(self.current)

        """

        """

        guess = guess.lower()
        if len(self.chain) % 2 == 0:
            working_list = [movie['title'].lower() for movie in self.current_list]
        else:
            working_list = [actor['name'].lower() for actor in self.current_list]

        if guess in working_list:
            self.current = string.capwords(guess)
            self.chain.append(self.current)
            if len(self.chain) % 2 == 0:
                self.current_list = MovieAPI.get_films(fixed_link)
            else:
                self.current_list = Picker.get_cast(fixed_link) 
        else:
            self.strikes += 1       
        """
