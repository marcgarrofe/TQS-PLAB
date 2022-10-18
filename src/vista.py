import tkinter as tk
from PIL import Image, ImageTk
import os


WINDOW_SIZE = "1000x600"
CARD_SIZE_X = 500
CARD_SIZE_Y = 726
IMG_RATIO_RESIZE = 5

PATH_CARDS_IMG = "../images/cards"

LIST_SUITS = ['spades', 'diamonds', 'hearts', 'clubs']
LIST_CARDS_NUMBERS = list(range(1, 14, 1))


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
            dict_cards[suit][int(number)] = img.copy()

    return dict_cards


class Vista:
    def __init__(self, controller):
        # Init controller
        self.controller = controller
        # Init Tkinter
        self.gui = tk.Tk(className='card game')
        # Set Window Size
        self.gui.geometry(WINDOW_SIZE)

    def menu(self):
        self.clear_frame()
        start_game_button = tk.Button(self.gui, text="Start Game", command=self.controller.call_game)
        start_game_button.pack()
        ranking_button = tk.Button(self.gui, text="Ranking", command=self.controller.call_ranking)
        ranking_button.pack()

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





    def test_display_card_deck(self):
        load = Image.open("../images/red_joker.png").resize((int(CARD_SIZE_X / IMG_RATIO_RESIZE),
                                                             int(CARD_SIZE_Y / IMG_RATIO_RESIZE)))
        render = ImageTk.PhotoImage(load)
        img = tk.Label(self.gui, image=render)
        img.image = render
        img.place(x=5, y=10)

        back_to_menu_button = tk.Button(self.gui, text="Back to Menu", command=self.controller.call_menu)
        back_to_menu_button.pack()
