from Storage import Storage
from Move import Move
from Parser import TZFEParser
from Lexer import TZFELexer

class Game:
    """
    The class that keeps track of a Game session
    Each game is represented by a Storage class object
    """

    def __init__(self):
        self.storage = None

    def new_game(self):
        """
        Starts a new game by creating a Storage object and generates 2 random tiles
        """
        self.storage = Storage()
        self.lexer = TZFELexer()
        self.parser = TZFEParser(self.storage)

        # Generate two initial tiles
        self.storage.generate_update()
        self.storage.generate_update()

        # Clean the screen
        print("2048> Hi, I am the 2048-game Engine.")
        self.storage.show_current_state()
        self.storage.logstate()

    def interactive(self):
        """
        Used to start a user-controlled interactive loop
        This uses the getchar module
        """
        self.game_running = True
        while self.game_running:
            print("2048> Please type a command.")
            command = input("----> ")

            self.parser.parse(self.lexer.tokenize(command))
            
            if self.check_game_over() != 0:
                self.game_running = False
                break

    def check_game_over(self):
        return self.storage.check_game_over()

    def get_max_tiles(self):
        return self.storage.get_max_tiles()
