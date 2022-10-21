import tkinter as tk
from PIL import Image, ImageTk
import os


WINDOW_SIZE = "1000x600"
CARD_SIZE_X = 500
CARD_SIZE_Y = 726
IMG_RATIO_RESIZE = 5

PATH_CARDS_IMG = "../images/cards"
PATH_FLIPPED_CARD = "../images/reversed_card.jpeg"
PATH_EMPTY_SLOT = "../images/empty_slot.jpeg"

LIST_SUITS = ['spades', 'diamonds', 'hearts', 'clubs']
LIST_CARDS_NUMBERS = list(range(1, 14, 1))

CARD_POSITION = {
    "card_px": {
        "x": int(CARD_SIZE_X / IMG_RATIO_RESIZE),
        "y": int(CARD_SIZE_Y / IMG_RATIO_RESIZE)
    },
    "draw_pile": {
        "x": 5,
        "y": 10
    },
    "goal_pile": {
        "x": 200,
        "y": 10,
        "margin": 30
    },
    "tableau_pile": {
        "x": 5,
        "y": 200,
        "x_margin": 20,
        "y_margin": 30
    }
}


def get_deck_img(path_cards_img):
    # Create empty dict for storing the cards
    dict_cards = dict.fromkeys(LIST_SUITS, dict())
    for suit in LIST_SUITS:
        dict_cards[suit] = dict.fromkeys(LIST_CARDS_NUMBERS, 0)

    # Load cards PNG from disk
    img_path_list = sorted(os.listdir(path_cards_img))
    for img_path in img_path_list:
        # Skip hidden files
        if not img_path.startswith('.'):
            number, _, suit = img_path.replace('.png', '').split('_')
            relative_img_path = path_cards_img + "/" + img_path
            img = Image.open(relative_img_path)
            img = img.resize((int(CARD_SIZE_X / IMG_RATIO_RESIZE), int(CARD_SIZE_Y / IMG_RATIO_RESIZE)))
            dict_cards[suit][int(number)] = ImageTk.PhotoImage(img.copy())

    # Load reversed card
    img = Image.open(PATH_FLIPPED_CARD)
    img = img.resize((int(CARD_SIZE_X / IMG_RATIO_RESIZE), int(CARD_SIZE_Y / IMG_RATIO_RESIZE)))
    dict_cards["flipped_card"] = ImageTk.PhotoImage(img.copy())

    # Load empty slot
    img = Image.open(PATH_EMPTY_SLOT)
    img = img.resize((int(CARD_SIZE_X / IMG_RATIO_RESIZE), int(CARD_SIZE_Y / IMG_RATIO_RESIZE)))
    dict_cards["empty_slot"] = ImageTk.PhotoImage(img.copy())

    return dict_cards


class Vista:
    def __init__(self, controller):
        # Init controller
        self.controller = controller
        # Init Tkinter
        self.gui = tk.Tk(className='card game')
        # Set Window Size
        self.gui.geometry(WINDOW_SIZE)
        # Init cards Img
        self.card_img = get_deck_img(PATH_CARDS_IMG)

    def menu(self):
        self.clear_frame()
        start_game_button = tk.Button(self.gui, text="Start Game", command=self.controller.call_game)
        start_game_button.pack()
        ranking_button = tk.Button(self.gui, text="Ranking", command=self.controller.call_ranking)
        ranking_button.pack()
        exit_button = tk.Button(self.gui, text="Exit", command=self.controller.call_exit)
        exit_button.pack()

    def ranking(self, data):
        for score in data:
            label = tk.Label(self.gui, text=score['name'])
            label.pack()

        back_to_menu_button = tk.Button(self.gui, text="Back to Menu", command=self.controller.call_menu)
        back_to_menu_button.pack()

    def refresh(self):
        # Define window loop
        self.gui.update_idletasks()
        self.gui.update()

    def clear_frame(self):
        for widgets in self.gui.winfo_children():
            widgets.destroy()

    def destroy(self):
        self.gui.destroy()

    def test_display_card_deck(self, game):
        # Print last card from Draw Pile
        last_card = game.get_draw_pile()[-1]
        last_card_render = self.card_img[last_card.get_suit()][last_card.get_number()]
        img = tk.Label(self.gui, image=last_card_render)
        img.place(x=CARD_POSITION['draw_pile']["x"], y=CARD_POSITION['draw_pile']["y"])

        # Print tableau pile
        tableau = game.get_tableau_pile()
        for pile_index, pile in enumerate(tableau):
            for card_index, card in enumerate(pile):
                card_x_pos = CARD_POSITION['tableau_pile']['x'] + \
                             (CARD_POSITION['tableau_pile']['x_margin'] + CARD_POSITION['card_px']['x']) * pile_index
                card_y_pos = CARD_POSITION['tableau_pile']['y_margin'] * card_index + CARD_POSITION['tableau_pile']['y']

                if card.get_reveled_state():
                    card_render = self.card_img[card.get_suit()][card.get_number()]
                else:
                    card_render = self.card_img['flipped_card']
                img = tk.Label(self.gui, image=card_render)
                img.place(x=card_x_pos, y=card_y_pos)

        # Print goal pile
        goal_pile = game.get_goal_pile()
        for pile_index, pile in enumerate(goal_pile):
            # X position is based on the tableau coordinates
            card_x_pos = CARD_POSITION['tableau_pile']['x'] + \
                         (CARD_POSITION['tableau_pile']['x_margin'] + CARD_POSITION['card_px']['x']) * (3 + pile_index)
            card_y_pos = CARD_POSITION['goal_pile']['y']

            # If Pile is empty, show empty rectangle
            if len(pile) == 0:
                card_render = self.card_img["empty_slot"]

            img = tk.Label(self.gui, image=card_render)
            img.place(x=card_x_pos, y=card_y_pos)

        back_to_menu_button = tk.Button(self.gui, text="Back to Menu", command=self.controller.call_menu)
        back_to_menu_button.pack()
