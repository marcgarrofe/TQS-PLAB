from model import DataBase
from vista import Vista


class Controller:
    def __init__(self):
        # Init Model DB
        self.db = DataBase()
        # Init Vista
        self.gui = Vista(self)
        # Launch menu

    def menu(self):
        # Vista Menu
        self.gui.menu()
        # Get User response
        # Switch case vista to call = Ranking o Game
        pass

    def call_ranking(self):
        self.gui.clear_frame()          # Clear GUI frame
        score_data = self.db.get_db()   # Get Score Data
        self.gui.ranking(score_data)    # Call GUI Ranking

    def call_game(self):
        self.gui.clear_frame()              # Clear GUI frame
        self.gui.test_display_card_deck()   # Call GUI Game

    def gui_refresh(self):
        self.gui.refresh()

    def show_ranking(self):
        # Get Model Ranking score
        # Call Ranking Vista
        pass

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
