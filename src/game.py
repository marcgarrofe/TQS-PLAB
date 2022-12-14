import random
import copy

LIST_SUITS = ['spades', 'diamonds', 'hearts', 'clubs']
LIST_NUMBERS = list(range(1, 14, 1))
COLOR_DICT = {
    'spades': 'black',
    'diamonds': 'red',
    'hearts': 'red',
    'clubs': 'black'
}


class Card:
    def __init__(self, suit, number, visible=False):
        if suit not in LIST_SUITS:
            raise ValueError("Suit not correct")

        if type(number) != int:
            raise TypeError("Only Int type numbers are allowed")

        if number < min(LIST_NUMBERS) or number > max(LIST_NUMBERS):
            raise ValueError("Number not correct")

        self._suit = suit
        self._number = number
        self._color = COLOR_DICT[suit]
        self._reveled_card = visible

    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        if self._suit != other.get_suit():
            return False
        if self._number != other.get_number():
            return False
        if self._color != other.get_color():
            return False
        if self._reveled_card != other.get_reveled_state():
            return False
        return True

    def get_suit(self):
        return self._suit

    def get_number(self):
        return self._number

    def get_color(self):
        return self._color

    def get_reveled_state(self):
        return self._reveled_card

    def set_card_visible(self):
        self._reveled_card = True

    def get_dict_card(self):
        card_dict = {
            'suit': self.get_suit(),
            'number': self.get_number(),
            'reveled_state': self.get_reveled_state()
        }
        return card_dict


class Game:
    def __init__(self, game=None, draw_pile=None, goal_pile=None, tableau_pile=None):
        # Check if game copy is provided
        if game is not None:
            self._draw_pile = copy.deepcopy(game.get_draw_pile())
            self._goal_pile = copy.deepcopy(game.get_goal_pile())
            self._tableau_pile = copy.deepcopy(game.get_tableau_pile())
        # If not all the required pile values are provided. The Game starts in random state
        elif draw_pile is None and goal_pile is None and tableau_pile is None:
            self._draw_pile = list()
            self._goal_pile = [[] for i in range(4)]
            self._tableau_pile = [[] for i in range(7)]

            self.deck = list()
            self.init_deck()
            self.init_piles()
        else:
            self._draw_pile = draw_pile.copy()
            self._goal_pile = goal_pile.copy()
            self._tableau_pile = tableau_pile.copy()

        self.num_movements = 0  # Init score num of movements

    def __eq__(self, other):
        if not isinstance(other, Game):
            return False
        if self._draw_pile != other.get_draw_pile():
            return False
        if self._goal_pile != other.get_goal_pile():
            return False
        if self._tableau_pile != other.get_tableau_pile():
            return False
        return True

    def init_deck(self):
        for suit in LIST_SUITS:
            for number in LIST_NUMBERS:
                self.deck.append(Card(suit=suit, number=number))

    def init_piles(self):
        # Init Draw Pile
        self._draw_pile = self.deck.copy()  # Copy deck into Draw Pile
        random.shuffle(self._draw_pile)  # Shuffle Draw Pile

        # Init Tableau Pile
        for pile_index in range(len(self._tableau_pile)):
            for num_cards in range(pile_index + 1):
                self._tableau_pile[pile_index].append(self._draw_pile.pop(0))

                # Set last pile card visible
                if num_cards == pile_index:
                    self._tableau_pile[pile_index][-1].set_card_visible()

    def get_draw_pile(self):
        return self._draw_pile

    def get_goal_pile(self):
        return self._goal_pile

    def get_tableau_pile(self):
        return self._tableau_pile

    def check_valid_tableau_to_tableau(self, origin_pile_number, destination_pile_number, origin_card_y):
        # Check if destination pile is empty and origin card is not 'King'.
        if (len(self._tableau_pile[destination_pile_number]) == 0) and \
                (self._tableau_pile[origin_pile_number][origin_card_y].get_number() != 13):
            return False

        # Check if 'King' card is moving to an empty space
        if (self._tableau_pile[origin_pile_number][origin_card_y].get_number() == 13) \
                and (len(self._tableau_pile[destination_pile_number]) == 0) \
                and (self._tableau_pile[origin_pile_number][origin_card_y].get_reveled_state() is True):
            return True

        # Check if origin card is reveled
        if self._tableau_pile[origin_pile_number][origin_card_y].get_reveled_state() is False:
            return False

        # Check colour is different
        if self._tableau_pile[origin_pile_number][origin_card_y].get_color() == \
                self._tableau_pile[destination_pile_number][-1].get_color():
            return False

        # Check number destination card is consecutive and greater than last origin card moved
        if (self._tableau_pile[origin_pile_number][origin_card_y].get_number() + 1) != \
                self._tableau_pile[destination_pile_number][-1].get_number():
            return False

        return True

    def check_valid_draw_to_tableau(self, destination_pile_number):
        # Check if Draw Pile has cards
        if len(self._draw_pile) == 0:
            return False

        # Check if 'King' is placed in a empty Tableau Pile
        if self._draw_pile[-1].get_number() == 13 and len(self._tableau_pile[destination_pile_number]) == 0:
            return True

        # Check if destination Pile is empty and the cards is not a 'King'
        if len(self._tableau_pile[destination_pile_number]) == 0:
            return False

        # Check colour is different
        if self._draw_pile[-1].get_color() == \
                self._tableau_pile[destination_pile_number][-1].get_color():
            return False

        # Check number destination card is consecutive and greater than last origin card moved
        if (self._draw_pile[-1].get_number() + 1) != \
                self._tableau_pile[destination_pile_number][-1].get_number():
            return False

        return True

    def check_valid_tableau_to_goal(self, origin_pile_number, destination_pile_number):
        # Check if Goal Pile is emtpy and card is 'Ace'
        if (len(self._goal_pile[destination_pile_number]) == 0) and \
                (self._tableau_pile[origin_pile_number][-1].get_number() == 1):
            return True

        # Check if Goal Pile is empty and card is NOT 'Ace'
        if (len(self._goal_pile[destination_pile_number]) == 0) and \
                (self._tableau_pile[origin_pile_number][-1].get_number() != 1):
            return False

        # Check if movement card is valid. Check same suit
        if self._goal_pile[destination_pile_number][-1].get_suit() != \
                self._tableau_pile[origin_pile_number][-1].get_suit():
            return False

        # Check if movement is valid. Consecutive numbers
        if (self._goal_pile[destination_pile_number][-1].get_number() + 1) != \
                self._tableau_pile[origin_pile_number][-1].get_number():
            return False

        return True

    def check_valid_draw_to_goal(self, destination_pile_number):
        # Check if Goal Pile is emtpy and card is 'Ace'
        if (len(self._goal_pile[destination_pile_number]) == 0) and \
                (self._draw_pile[-1].get_number() == 1):
            return True

        # Check if Goal Pile is emtpy and card is NOT 'Ace'
        if (len(self._goal_pile[destination_pile_number]) == 0) and \
                (self._draw_pile[-1].get_number() != 1):
            return False

        # Check if movement card is valid. Check same suit
        if self._goal_pile[destination_pile_number][-1].get_suit() != \
                self._draw_pile[-1].get_suit():
            return False

        # Check if movement is valid. Consecutive numbers
        if (self._goal_pile[destination_pile_number][-1].get_number() + 1) != \
                self._draw_pile[-1].get_number():
            return False

        return True

    def move_card_tableau_to_tableau(self, origin_pile_number, destination_pile_number, origin_card_y):
        # Check if movement is valid
        if not self.check_valid_tableau_to_tableau(origin_pile_number, destination_pile_number, origin_card_y):
            return False
        # Copy the origin cards
        list_cards = list(self._tableau_pile[origin_pile_number][origin_card_y:])
        # Delete cards from origin
        for _ in range(abs(origin_card_y)):
            self._tableau_pile[origin_pile_number].pop(-1)
        # Copy origin Card/s into destination pile
        self._tableau_pile[destination_pile_number] += list_cards
        # Update visible state of the last card from origin pile (if exists)
        if len(self._tableau_pile[origin_pile_number]) > 0:
            self._tableau_pile[origin_pile_number][-1].set_card_visible()
        # Increment num of movements
        self.num_movements += 1

        return True

    def move_card_draw_to_tableau(self, destination_pile_number):
        # Check if movement is valid
        if not self.check_valid_draw_to_tableau(destination_pile_number):
            return False
        # Pop last card from Draw Pile
        draw_card = self._draw_pile.pop(-1)
        # Change card visible state
        draw_card.set_card_visible()
        # Paste last card into the destination pile
        self._tableau_pile[destination_pile_number].append(draw_card)
        # Update visible state from Draw Pile last card
        if len(self._draw_pile) > 0:
            self._draw_pile[-1].set_card_visible()
        # Increment num of movements
        self.num_movements += 1

        return True

    def move_card_tableau_to_goal(self, origin_pile_number, destination_pile_number):
        # Check if movement is valid
        if not self.check_valid_tableau_to_goal(origin_pile_number, destination_pile_number):
            return False
        # Pop last card from origin Tableau Pile
        draw_card = self._tableau_pile[origin_pile_number].pop(-1)
        # Paste last card into the destination pile
        self._goal_pile[destination_pile_number].append(draw_card)
        # Update visible state from Draw Pile last card
        if len(self._tableau_pile[origin_pile_number]) > 0:
            self._tableau_pile[origin_pile_number][-1].set_card_visible()
        # Increment num of movements
        self.num_movements += 1

        return True

    def move_card_draw_to_goal(self, destination_pile_number):
        # Check if movement is valid
        if not self.check_valid_draw_to_goal(destination_pile_number):
            return False
        # Pop last card from origin Draw Pile
        draw_card = self._draw_pile.pop(-1)
        # Paste last card into the destination pile
        self._goal_pile[destination_pile_number].append(draw_card)
        # Update visible state from Draw Pile last card
        if len(self._draw_pile) > 0:
            self._draw_pile[-1].set_card_visible()
        # Increment num of movements
        self.num_movements += 1

        return True

    def new_draw_card(self):
        if len(self._draw_pile) <= 1:
            return False
        # Pop last card from draw pile
        last_card = self._draw_pile.pop(-1)
        # Insert at the beginning
        self._draw_pile.insert(0, last_card)
        # Increment num of movements
        self.num_movements += 1

        return True


def game_to_dict(game):
    if type(game) != Game:
        raise TypeError('Param game must be Class Game Type')

    dict_game = dict()
    list_draw_pile = list()
    list_goal_pile = list()
    list_tableau_pile = list()

    for card in game.get_draw_pile():
        list_draw_pile.append(card.get_dict_card())

    for pile in game.get_goal_pile():
        list_pile = list()
        for card in pile:
            list_pile.append(card.get_dict_card())
        list_goal_pile.append(list_pile)

    for pile in game.get_tableau_pile():
        list_pile = list()
        for card in pile:
            list_pile.append(card.get_dict_card())
        list_tableau_pile.append(list_pile)

    dict_game['draw_pile'] = list_draw_pile
    dict_game['goal_pile'] = list_goal_pile
    dict_game['tableau_pile'] = list_tableau_pile

    return dict_game


def dict_to_game(game_dict):
    if type(game_dict) != dict:
        raise TypeError('Param game must be Dict Type')
    if 'draw_pile' not in game_dict.keys():
        raise ValueError('Draw Pile not in dictionary')
    if 'goal_pile' not in game_dict.keys():
        raise ValueError('Goal Pile not in dictionary')
    if 'tableau_pile' not in game_dict.keys():
        raise ValueError('Tableau Pile not in dictionary')

    list_draw_pile = list()
    list_goal_pile = list()
    list_tableau_pile = list()

    for card in game_dict['draw_pile']:
        list_draw_pile.append(Card(suit=card['suit'], number=card['number'], visible=card['reveled_state']))

    for pile in game_dict['goal_pile']:
        list_pile = list()
        for card in pile:
            list_pile.append(Card(suit=card['suit'], number=card['number'], visible=card['reveled_state']))
        list_goal_pile.append(list_pile)

    for pile in game_dict['tableau_pile']:
        list_pile = list()
        for card in pile:
            list_pile.append(Card(suit=card['suit'], number=card['number'], visible=card['reveled_state']))
        list_tableau_pile.append(list_pile)

    return Game(draw_pile=list_draw_pile,
                goal_pile=list_goal_pile,
                tableau_pile=list_tableau_pile)
