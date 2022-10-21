from model import DataBase
from vista import Vista
from game import Game

WINDOWS = ['menu', 'ranking', 'game']

class Controller:
    def __init__(self):
        self.db = DataBase()                # Init Model DB
        self.gui = Vista(self)              # Init Vista GUI
        self.call_menu()                    # Launch menu
        self.window = None                  # Declare Window type
        self.game = None                    # Declare Game

    def call_menu(self):
        self.gui.clear_frame()              # Clear GUI frame
        self.gui.menu()                     # Call GUI Menu
        self.window = 'menu'

    def call_ranking(self):
        self.gui.clear_frame()              # Clear GUI frame
        score_data = self.db.get_db()       # Get Score Data
        self.gui.ranking(score_data)        # Call GUI Ranking
        self.window = 'ranking'

    def call_game(self):
        self.gui.clear_frame()              # Clear GUI frame
        self.game = Game()                  # Declare Random Game
        self.gui.test_display_card_deck(self.game)   # Call GUI Game
        self.window = 'game'

    def call_exit(self):
        self.gui.clear_frame()      # Clear GUI Frame
        self.gui.destroy()          # Destroy Terminal

    def gui_refresh(self):
        self.gui.refresh()

    def save_game(self):
        # Call Model save_game()
        pass

    def add_score(self):
        # Call Vista : Ask for players name
        # Call model add_Score()
        pass

    def play(self):
        # Implement game logic
        pass

    def run_controller(self):
        self.gui_refresh()
