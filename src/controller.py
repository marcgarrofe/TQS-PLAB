from src.model import DataBase
from src.vista import Vista, CARD_POSITION
from src.game import Game
from pynput import mouse

WINDOWS = ['menu', 'ranking', 'game']


def check_draw_position(x, y):
    if (x >= CARD_POSITION['draw_pile']['x']) and \
            (x <= CARD_POSITION['draw_pile']['x'] + CARD_POSITION['card_px']['x']) and \
            (y >= CARD_POSITION['draw_pile']['y']) and \
            (y <= CARD_POSITION['draw_pile']['y'] + CARD_POSITION['card_px']['y']):
        return True
    else:
        return False


def check_goal_position(x, y):
    x_min_margin = CARD_POSITION['goal_pile']['x']
    x_max_margin = CARD_POSITION['goal_pile']['x'] + 4 * CARD_POSITION['card_px']['x'] + 3 * CARD_POSITION['goal_pile']['margin']

    y_min_margin = CARD_POSITION['goal_pile']['y']
    y_max_margin = CARD_POSITION['goal_pile']['y'] + CARD_POSITION['card_px']['y']

    if (x >= x_min_margin) and \
            (x <= x_max_margin) and \
            (y >= y_min_margin) and \
            (y <= y_max_margin):

        absolute_x_pos = x - CARD_POSITION['goal_pile']['x']
        pile_number = int(absolute_x_pos / (CARD_POSITION['goal_pile']['margin'] + CARD_POSITION['card_px']['x']))

        return [True, pile_number]
    else:
        return [False, None]


def check_tableau_position(x, y, tableau):
    # Calculate Tableau Pile number
    column_x_size = int(((CARD_POSITION['card_px']['x'] * len(tableau)) + (CARD_POSITION['tableau_pile']['x_margin'] * (len(tableau) - 1))) / len(tableau))
    pile_number = int(x / column_x_size)

    if pile_number >= len(tableau):
        return [False, None, None]

    y_min_pile = CARD_POSITION['tableau_pile']['y']
    y_max_pile = CARD_POSITION['tableau_pile']['y'] + CARD_POSITION['card_px']['y'] +\
                 ((len(tableau[pile_number]) - 1) * CARD_POSITION['tableau_pile']['y_margin'])

    if y < y_min_pile or y > y_max_pile:
        return [False, None, None]                    # Card out from Pile 'y' borders

    last_card_y = (CARD_POSITION['tableau_pile']['y_margin'] * (len(tableau[pile_number]) - 1)   # Last card
                   + CARD_POSITION['tableau_pile']['y'])

    num_cards = len(tableau[pile_number])
    if num_cards <= 1:                # Empty Pile or only one card
        row_pile = -1
    elif last_card_y < y:
        row_pile = -1
    else:
        absolute_y_pos = y - CARD_POSITION['tableau_pile']['y']
        row_pile = int(absolute_y_pos / CARD_POSITION['tableau_pile']['y_margin'])
        row_pile = row_pile - len(tableau[pile_number])
    # print((pile_number, row_pile))
    return [True, pile_number, row_pile]


class Controller:
    def __init__(self):
        self.db = DataBase()                # Init Model DB
        self.gui = Vista(self)              # Init Vista GUI
        self.window = None                  # Declare Window type
        self.game = None                    # Declare Game
        self.mouse = mouse.Controller()     # Declare mouse controller
        self.mouse_state_pressed = None
        self.mouse_state_released = None
        self.call_menu()                    # Launch menu

    def call_menu(self):
        self.gui.clear_frame()              # Clear GUI frame
        self.gui.menu()                     # Call GUI Menu
        self.window = 'menu'
        self.gui_refresh()

    def call_ranking(self):
        self.gui.clear_frame()              # Clear GUI frame
        score_data = self.db.get_db()       # Get Score Data
        self.gui.ranking(score_data)        # Call GUI Ranking
        self.window = 'ranking'
        self.gui_refresh()

    def call_game(self):
        self.gui.clear_frame()              # Clear GUI frame
        self.game = Game()                  # Declare Random Game
        #self.gui.test_display_card_deck(self.game)   # Call GUI Game
        self.gui.game_refresh(game=self.game)
        self.window = 'game'
        self.run_game()

    def call_exit(self):
        self.gui.clear_frame()      # Clear GUI Frame
        self.gui.destroy()          # Destroy Terminal

    def gui_refresh(self, game=False):
        if not game:
            self.gui.refresh()
        else:
            self.gui.game_refresh()

    def save_game(self):
        # Call Model save_game()
        pass

    def add_score(self):
        # Call Vista : Ask for players name
        # Call model add_Score()
        pass

    def on_click(self, x, y, button, pressed):
        if button == button.left:
            print('{0} at {1}'.format(
                'Pressed' if pressed else 'Released',
                (x, y)))
            if pressed:
                self.mouse_state_pressed = {"x": int(x), "y": int(y)}
            else:
                self.mouse_state_released = {"x": int(x), "y": int(y)}
        else:
            self.mouse_state_pressed = None

    def run_game(self):
        listener = mouse.Listener(on_click=self.on_click)
        listener.start()

        while True:
            # If the mouse has been released, apply game changes
            if self.mouse_state_released:
                win_x, win_y = self.gui.get_window_coords()

                # Sanity check
                if not self.mouse_state_pressed and not self.mouse_state_pressed:
                    continue

                origin_x = self.mouse_state_pressed['x'] - win_x
                origin_y = self.mouse_state_pressed['y'] - win_y

                destination_x = self.mouse_state_released['x'] - win_x
                destination_y = self.mouse_state_released['y'] - win_y

                result_ok = False
                # Goal Pile is never origin
                if check_goal_position(origin_x, origin_y)[0]:
                    continue

                # Draw pile is never Destination if origin is not Draw Pile
                elif check_draw_position(destination_x, destination_y) and not check_draw_position(origin_x, origin_x):
                    continue

                # Get new card from Draw pile
                elif check_draw_position(destination_x, destination_y) and check_draw_position(origin_x, origin_x):
                    result_ok = self.game.new_draw_card()

                # Apply movement in Tableau
                elif check_tableau_position(origin_x, origin_y, self.game.get_tableau_pile())[0] and check_tableau_position(destination_x, destination_y, self.game.get_tableau_pile())[0]:
                    _, origin_pile, origin_row = check_tableau_position(origin_x, origin_y, self.game.get_tableau_pile())
                    _, destination_pile, _ = check_tableau_position(destination_x, destination_y, self.game.get_tableau_pile())

                    result_ok = self.game.move_card_tableau_to_tableau(origin_pile_number=origin_pile,
                                                           destination_pile_number=destination_pile,
                                                           origin_card_y=origin_row)

                # Apply movement from draw to tableau
                elif check_draw_position(origin_x, origin_y) and check_tableau_position(destination_x, destination_y, self.game.get_tableau_pile())[0]:
                    _, destination_pile, _ = check_tableau_position(destination_x, destination_y, self.game.get_tableau_pile())
                    result_ok = self.game.move_card_draw_to_tableau(destination_pile)

                # Apply movement from draw to goal
                elif check_draw_position(origin_x, origin_y) and check_goal_position(destination_x, destination_y)[0]:
                    # IMPLEMENTAR
                    continue

                # Apply movement from tableau to goal
                elif check_tableau_position(origin_x, origin_y, self.game.get_tableau_pile())[0] and check_goal_position(destination_x, destination_y)[0]:
                    _, origin_pile, origin_row = check_tableau_position(origin_x, origin_y, self.game.get_tableau_pile())
                    _, destination_pile = check_goal_position(destination_x, destination_y)

                    result_ok = self.game.move_card_tableau_to_goal(origin_pile, destination_pile)

                if result_ok:
                    print("Card moved")
                    self.gui.game_refresh(self.game)
                else:
                    print("Movement NOT allowed")

                # Reset mouse state
                self.mouse_state_released = None
                self.mouse_state_pressed = None
