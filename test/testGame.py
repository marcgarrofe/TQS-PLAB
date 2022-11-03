import unittest
from src.game import Game
from src.game import Card
from src.game import game_to_dict
from test.mockObjectsGame import mock_game_list
import copy


class TestCard(unittest.TestCase):
    def test_init(self):
        card = Card('spades', 1)
        self.assertEqual(card.get_suit(), 'spades')
        self.assertEqual(card.get_number(), 1)
        self.assertFalse(card.get_reveled_state())
        card.set_card_visible()                         # Change Card Visible State
        self.assertTrue(card.get_reveled_state())

        with self.assertRaisesRegex(ValueError, "Suit not correct"):
            _ = Card('spades2', 1)
        with self.assertRaisesRegex(ValueError, "Number not correct"):
            _ = Card('spades', -1)
        with self.assertRaisesRegex(ValueError, "Number not correct"):
            _ = Card('spades', 14)
        with self.assertRaisesRegex(ValueError, "Suit not correct"):
            _ = Card('.spades', 15)
        with self.assertRaisesRegex(TypeError, "Only Int type numbers are allowed"):
            _ = Card('spades', 'test')

    def test_equal(self):
        card_1 = Card('spades', 1)
        card_1_copy = Card('spades', 1)
        self.assertEqual(card_1, card_1_copy)
        card_2 = Card('spades', 2)
        self.assertNotEqual(card_1, card_2)
        card_3 = Card('diamonds', 2)
        self.assertNotEqual(card_3, card_2)
        self.assertNotEqual(card_1, card_3)
        self.assertNotEqual(card_1, int(3))
        card_4 = Card('spades', 1, visible=True)
        self.assertNotEqual(card_1, card_4)
        card_1_red = Card('spades', 1)
        card_1_red._color = 'red'
        self.assertNotEqual(card_1_red, card_1)

    def test_get_json_card(self):
        card_1 = Card('spades', 1)
        self.assertEqual(card_1.get_dict_card(), {'suit': 'spades',
                                                  'number': 1,
                                                  'reveled_state': False})
        card_1.set_card_visible()
        self.assertEqual(card_1.get_dict_card(), {'suit': 'spades',
                                                  'number': 1,
                                                  'reveled_state': True})


class TestGame(unittest.TestCase):
    def test_default_init(self):
        game = Game()

        tableau_pile = game.get_tableau_pile()
        self.assertEqual(len(tableau_pile), 7)          # Check number of Piles in the Tableau

        tableau_total_cars = 0
        for pile in tableau_pile:
            tableau_total_cars += len(pile)
        self.assertEqual(tableau_total_cars, 28)        # Check number of Cards in the Tableau

        draw_pile = game.get_draw_pile()
        self.assertEqual(len(draw_pile), 24)            # Check number of Cards in the Draw Pile

        goal_pile = game.get_goal_pile()
        self.assertEqual(len(goal_pile), 4)             # Check number of Piles in the Goal Pile

        goal_pile_total_cars = 0
        for pile in goal_pile:
            goal_pile_total_cars += len(pile)
        self.assertEqual(goal_pile_total_cars, 0)       # Check number of Cards in the Goal Pile

    def test_parameters_init(self):
        draw_pile = [Card('spades', 13), Card('clubs', 1)]
        goal_pile = [[Card('diamonds', 1, visible=True)], [Card('hearts', 1, visible=True)], [], []]
        tableau_pile = [[Card('diamonds', 7, visible=True)],
                        [Card('spades', 4), Card('spades', 6, visible=False)],
                        [Card('diamonds', 11)], [], [], [], []]

        game = Game(draw_pile=draw_pile, goal_pile=goal_pile, tableau_pile=tableau_pile)

        self.assertEqual(game.get_draw_pile(), draw_pile)
        self.assertEqual(game.get_goal_pile(), goal_pile)
        self.assertEqual(game.get_tableau_pile(), tableau_pile)

    def test_copy_init(self):
        game = Game(game=mock_game_list[0])
        self.assertEqual(game, mock_game_list[0])
        self.assertNotEqual(game, mock_game_list[1])        # Test Draw Pile
        self.assertNotEqual(game, mock_game_list[2])        # Test Draw Pile
        self.assertNotEqual(game, int(0))                   # Test argument type

        game_2 = Game(game=mock_game_list[2])
        game_2.move_card_tableau_to_goal(0, 0)
        self.assertNotEqual(game_2, mock_game_list[2])      # Test Goal Pile

        game_3 = Game(draw_pile=[], goal_pile=[], tableau_pile=[[Card('clubs', 1)], [], [], [], [], [], []])
        game_4 = Game(draw_pile=[], goal_pile=[], tableau_pile=[[Card('spades', 1)], [], [], [], [], [], []])
        self.assertNotEqual(game_3, game_4)                 # Test Tableau Pile

    def test_check_valid_tableau_to_tableau(self):
        game = Game(game=mock_game_list[0])
        # Move '9 of diamonds' to '10 of spades'
        self.assertTrue(game.check_valid_tableau_to_tableau(3, 2, -1))
        # Move '9 of diamonds' to an empty space
        self.assertFalse(game.check_valid_tableau_to_tableau(3, 6, -1))
        # Move '11 of diamonds' and '10 of spades' to '12 of spades'
        self.assertTrue(game.check_valid_tableau_to_tableau(2, 4, -2))
        # Move '13 of clubs' to an empty space
        self.assertTrue(game.check_valid_tableau_to_tableau(5, 6, -1))

        game = Game(game=mock_game_list[1])
        self.assertFalse(game.check_valid_tableau_to_tableau(0, 1, -4))
        self.assertTrue(game.check_valid_tableau_to_tableau(0, 3, -3))

    def test_check_valid_draw_to_tableau(self):
        game = Game(game=mock_game_list[0])
        # Move '13 of hearts' to an empty space
        self.assertTrue(game.check_valid_draw_to_tableau(6))
        # Move '13 of hearts' to an occupied pile
        self.assertFalse(game.check_valid_draw_to_tableau(5))

        game = Game(game=mock_game_list[1])
        # Move '8 of spades' to '9 of hearts'
        self.assertTrue(game.check_valid_draw_to_tableau(3))
        # Move '8 of spades' to '10 of hearts'
        self.assertFalse(game.check_valid_draw_to_tableau(2))
        # Move '8 of spades' to '10 of spades'
        self.assertFalse(game.check_valid_draw_to_tableau(4))
        # Move '8 of spades' to 'an empty space
        self.assertFalse(game.check_valid_draw_to_tableau(6))

    def test_check_valid_tableau_to_goal(self):
        game = Game(game=mock_game_list[2])
        # Move '2 of diamonds' to '1 of diamonds'
        self.assertTrue(game.check_valid_tableau_to_goal(0, 0))
        # Move '2 of diamonds' to '1 of clubs'
        self.assertFalse(game.check_valid_tableau_to_goal(0, 1))
        # Move '3 of diamonds' to '1 of diamonds'
        self.assertFalse(game.check_valid_tableau_to_goal(1, 0))
        # Move '3 of diamonds' to an empty space
        self.assertFalse(game.check_valid_tableau_to_goal(1, 2))
        # Move '1 of spades' to an empty space
        self.assertTrue(game.check_valid_tableau_to_goal(2, 2))

    def test_move_card_tableau_to_tableau(self):
        # Move '9 of diamonds' to '10 of spades'
        game = Game(game=mock_game_list[0])
        self.assertTrue(game.move_card_tableau_to_tableau(3, 2, -1))
        self.assertEqual(game.get_tableau_pile()[3], [])    # Check origin is empty
        self.assertEqual(game.get_tableau_pile()[2],        # Check destination has added card
                         [Card('diamonds', 11, visible=True),
                          Card('spades', 10, visible=True),
                          Card('diamonds', 9, visible=True)])

        # Move '9 of diamonds' to an empty space, then Move '9 of diamonds' to '10 of spades'
        game = Game(game=mock_game_list[0])
        self.assertFalse(game.move_card_tableau_to_tableau(3, 6, -1))
        self.assertTrue(game.move_card_tableau_to_tableau(3, 2, -1))
        self.assertEqual(game.get_tableau_pile()[3], [])    # Check origin is empty
        self.assertEqual(game.get_tableau_pile()[2],        # Check destination has added card
                         [Card('diamonds', 11, visible=True),
                          Card('spades', 10, visible=True),
                          Card('diamonds', 9, visible=True)])

        # Move '6 of spades' to '7 of diamonds', then move two last card to '8 of spades'
        game = Game(game=mock_game_list[0])
        self.assertTrue(game.move_card_tableau_to_tableau(1, 0, -1))
        self.assertEqual(game.get_tableau_pile()[0],        # Check destination has added card
                         [Card('diamonds', 7, visible=True),
                          Card('spades', 6, visible=True)])
        self.assertEqual(game.get_tableau_pile()[1],        # Check origin pile and updated visible state
                         [Card('spades', 8, visible=True)])

        self.assertTrue(game.move_card_tableau_to_tableau(0, 1, -2))
        self.assertEqual(game.get_tableau_pile()[1],        # Check destination pile has added card
                         [Card('spades', 8, visible=True),
                          Card('diamonds', 7, visible=True),
                          Card('spades', 6, visible=True)])
        self.assertEqual(game.get_tableau_pile()[0], [])    # Check origin pile is empty

        # Move '11 of diamonds' and '10 of spades' to '12 of spades'
        game = Game(game=mock_game_list[0])
        self.assertTrue(game.move_card_tableau_to_tableau(2, 4, -2))
        self.assertEqual(game.get_tableau_pile()[4],    # Check destination pile has added card
                         [Card('spades', 12, visible=True),
                          Card('diamonds', 11, visible=True),
                          Card('spades', 10, visible=True)])
        self.assertEqual(game.get_tableau_pile()[2], [])

        # Move '13 of clubs' to an empty space
        game = Game(game=mock_game_list[0])
        self.assertTrue(game.move_card_tableau_to_tableau(5, 6, -1))
        self.assertEqual(game.get_tableau_pile()[6],    # Check destination pile has added card
                         [Card('clubs', 13, visible=True)])
        self.assertEqual(game.get_tableau_pile()[5], [])

    def test_move_card_draw_to_tableau(self):
        # Move '13 of hearts' to an empty space
        game = Game(game=mock_game_list[0])
        self.assertTrue(game.move_card_draw_to_tableau(6))
        self.assertEqual(game.get_draw_pile(),          # Check draw pile
                         [Card('spades', 13),
                         Card('clubs', 1),
                         Card('diamonds', 2, visible=True)])
        self.assertEqual(game.get_tableau_pile()[6],    # Check destination pile
                         [Card('hearts', 13, visible=True)])

        # Move '13 of hearts' to an occupied pile
        game = Game(game=mock_game_list[0])
        self.assertFalse(game.move_card_draw_to_tableau(5))
        self.assertEqual(game.get_draw_pile(),          # Check draw hasn't changed
                         [Card('spades', 13),
                          Card('clubs', 1),
                          Card('diamonds', 2),
                          Card('hearts', 13, visible=True)])
        self.assertEqual(game.get_tableau_pile()[5],    # Check destination hasn't changed
                         [Card('clubs', 13, visible=True)])

        # Move '8 of spades' to '9 of hearts'
        game = Game(game=mock_game_list[1])
        self.assertTrue(game.move_card_draw_to_tableau(3))
        self.assertEqual(game.get_draw_pile(),          # Check draw pile
                         [])
        self.assertEqual(game.get_tableau_pile()[3],    # Check destination pile
                         [Card('hearts', 9, visible=True),
                          Card('spades', 8, visible=True)])

        # Move '8 of spades' to '10 of hearts'
        game = Game(game=mock_game_list[1])
        self.assertFalse(game.move_card_draw_to_tableau(2))
        # Move '8 of spades' to '10 of spades'
        self.assertFalse(game.move_card_draw_to_tableau(4))
        # Move '8 of spades' to 'an empty space
        self.assertFalse(game.move_card_draw_to_tableau(6))

    def test_move_card_tableau_to_goal(self):
        # Move '2 of diamonds' to '1 of diamonds'
        game = Game(game=mock_game_list[2])
        self.assertTrue(game.move_card_tableau_to_goal(0, 0))
        self.assertEqual(game.get_tableau_pile()[0],        # Check origin pile
                         [])
        self.assertEqual(game.get_goal_pile(),              # Check Full Goal pile
                         [[Card('diamonds', 1, visible=True),
                           Card('diamonds', 2, visible=True)],
                          [Card('clubs', 1, visible=True)], [], []])
        # Move '3 of diamonds' to '2 of diamonds'
        self.assertTrue(game.move_card_tableau_to_goal(1, 0))
        self.assertEqual(game.get_tableau_pile()[1],        # Check origin pile
                         [])
        self.assertEqual(game.get_goal_pile(),              # Check Full Goal pile
                         [[Card('diamonds', 1, visible=True),
                           Card('diamonds', 2, visible=True),
                           Card('diamonds', 3, visible=True)],
                          [Card('clubs', 1, visible=True)], [], []])

        # Move '2 of diamonds' to '1 of clubs'
        game = Game(game=mock_game_list[2])
        self.assertFalse(game.move_card_tableau_to_goal(0, 1))
        # Move '3 of diamonds' to '1 of diamonds'
        self.assertFalse(game.move_card_tableau_to_goal(1, 0))
        # Move '3 of diamonds' to an empty space
        self.assertFalse(game.move_card_tableau_to_goal(1, 2))

        # Move '1 of spades' to an empty space
        game = Game(game=mock_game_list[2])
        self.assertTrue(game.move_card_tableau_to_goal(2, 2))
        self.assertEqual(game.get_goal_pile(),              # Check goal pile
                         [[Card('diamonds', 1, visible=True)],
                          [Card('clubs', 1, visible=True)],
                          [Card('spades', 1, visible=True)],
                          []])
        self.assertEqual(game.get_tableau_pile(),
                         [[Card('diamonds', 2, visible=True)],
                          [Card('diamonds', 3, visible=True)],
                          [],
                          [Card('hearts', 3, visible=True),
                           Card('hearts', 2, visible=True)],
                          [], [], []])

    def test_new_draw_card(self):
        game = Game(draw_pile=[], goal_pile=[], tableau_pile=[])
        self.assertFalse(game.new_draw_card())              # Check no more cards on Draw Pile

        game_2 = Game(draw_pile=[Card('clubs', 1), Card('hearts', 2), Card('spades', 3)],
                      goal_pile=[], tableau_pile=[])
        self.assertTrue(game_2.new_draw_card())
        self.assertEqual(game_2.get_draw_pile(),
                         [Card('spades', 3), Card('clubs', 1), Card('hearts', 2)])


class TestGameToJson(unittest.TestCase):
    def test_game_to_dict(self):
        with self.assertRaisesRegex(TypeError, "Param game must be Class Game Type"):
            _ = game_to_dict(int(0))

        game = Game(game=mock_game_list[2])
        result_dict = game_to_dict(game)
        expected_dict = {
            'draw_pile': [],
            'goal_pile': [
                    [{'suit': 'diamonds', 'number': 1, 'reveled_state': True}],
                    [{'suit': 'clubs', 'number': 1, 'reveled_state': True}],
                    [],
                    []
            ],
            'tableau_pile': [
                [{'suit': 'diamonds', 'number': 2, 'reveled_state': True}],
                [{'suit': 'diamonds', 'number': 3, 'reveled_state': True}],
                [{'suit': 'spades', 'number': 1, 'reveled_state': True}],
                [{'suit': 'hearts', 'number': 3, 'reveled_state': True},
                    {'suit': 'hearts', 'number': 2, 'reveled_state': True}],
                [],
                [],
                []
            ]
        }
        self.assertEqual(result_dict, expected_dict)

        game_2 = Game(draw_pile=[Card('clubs', 1)], goal_pile=[], tableau_pile=[])
        result_dict_2 = game_to_dict(game_2)
        expected_dict_2 = {
            'draw_pile': [{'suit': 'clubs', 'number': 1, 'reveled_state': False}],
            'goal_pile': [],
            'tableau_pile': []
        }
        self.assertEqual(result_dict_2, expected_dict_2)
