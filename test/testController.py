import unittest
from src.controller import check_draw_position, check_tableau_position, check_goal_position, Controller
from src.vista import CARD_POSITION
from test.mockObjectsGame import mock_game_list
from test.testModel import MockDataBaseScore


class TestCheckDrawPosition(unittest.TestCase):
    def test_border_position(self):
        """
        Black-box test
        Test border and limit values
        """
        self.assertTrue(check_draw_position(CARD_POSITION['draw_pile']['x'], CARD_POSITION['draw_pile']['y']))

        self.assertTrue(check_draw_position(CARD_POSITION['draw_pile']['x'],
                                            CARD_POSITION['draw_pile']['y'] + CARD_POSITION['card_px']['y']))

        self.assertTrue(check_draw_position(CARD_POSITION['draw_pile']['x'] + CARD_POSITION['card_px']['x'],
                                            CARD_POSITION['draw_pile']['y']))

        self.assertTrue(check_draw_position(CARD_POSITION['draw_pile']['x'] + CARD_POSITION['card_px']['x'],
                                            CARD_POSITION['draw_pile']['y'] + CARD_POSITION['card_px']['y']))

        self.assertFalse(check_draw_position(CARD_POSITION['draw_pile']['x'] + CARD_POSITION['card_px']['x'] + 10,
                                            CARD_POSITION['draw_pile']['y'] + CARD_POSITION['card_px']['y']))

        self.assertFalse(check_draw_position(CARD_POSITION['draw_pile']['x'] + CARD_POSITION['card_px']['x'],
                                             CARD_POSITION['draw_pile']['y'] + CARD_POSITION['card_px']['y'] + 10))

        self.assertFalse(check_draw_position(CARD_POSITION['draw_pile']['x'] + CARD_POSITION['card_px']['x'] + 10,
                                             CARD_POSITION['draw_pile']['y'] + CARD_POSITION['card_px']['y'] + 10))

    def test_position(self):
        """
        Black-box test
        """
        self.assertTrue(check_draw_position(CARD_POSITION['draw_pile']['x'] + 10, CARD_POSITION['draw_pile']['y'] + 10))


class TestCheckTableauPosition(unittest.TestCase):
    def test_border_position(self):
        """
        Black-box test
        Test border and limit values
        """
        game = mock_game_list[0]
        self.assertEqual(check_tableau_position(x=CARD_POSITION['tableau_pile']['x'],
                                                y=CARD_POSITION['tableau_pile']['y'],
                                                tableau=game.get_tableau_pile()), [True, 0, -1])

        self.assertEqual(check_tableau_position(x=CARD_POSITION['tableau_pile']['x'],
                                                y=CARD_POSITION['tableau_pile']['y'] + CARD_POSITION['card_px']['y'],
                                                tableau=game.get_tableau_pile()), [True, 0, -1])

        self.assertEqual(check_tableau_position(x=CARD_POSITION['tableau_pile']['x'] +
                                                  CARD_POSITION['tableau_pile']['x_margin'] +
                                                  CARD_POSITION['card_px']['x'],
                                                y=CARD_POSITION['tableau_pile']['y'],
                                                tableau=game.get_tableau_pile()), [True, 1, -2])

        self.assertEqual(check_tableau_position(x=CARD_POSITION['tableau_pile']['x'] +
                                                  CARD_POSITION['tableau_pile']['x_margin'] +
                                                  CARD_POSITION['card_px']['x'],
                                                y=CARD_POSITION['tableau_pile']['y'] +
                                                  CARD_POSITION['tableau_pile']['y_margin'],
                                                tableau=game.get_tableau_pile()), [True, 1, -1])

    def test_limit_position(self):
        game = mock_game_list[0]
        self.assertEqual(check_tableau_position(x=CARD_POSITION['tableau_pile']['x'] +
                                                  CARD_POSITION['tableau_pile']['x_margin'] +
                                                  CARD_POSITION['card_px']['x'] + 1,
                                                y=CARD_POSITION['tableau_pile']['y'],
                                                tableau=game.get_tableau_pile()), [True, 1, -2])

        self.assertEqual(check_tableau_position(x=CARD_POSITION['tableau_pile']['x'],
                                                y=CARD_POSITION['tableau_pile']['y'] - 1,
                                                tableau=game.get_tableau_pile()), [False, None, None])

    def test_position(self):
        game = mock_game_list[0]
        self.assertEqual(check_tableau_position(x=CARD_POSITION['tableau_pile']['x'],
                                                y=CARD_POSITION['tableau_pile']['y'] + CARD_POSITION['card_px']['y'] + 10,
                                                tableau=game.get_tableau_pile()), [False, None, None])

        self.assertEqual(check_tableau_position(x=CARD_POSITION['tableau_pile']['x'],
                                                y=CARD_POSITION['tableau_pile']['y'] - 10,
                                                tableau=game.get_tableau_pile()), [False, None, None])

        self.assertEqual(check_tableau_position(x=CARD_POSITION['tableau_pile']['x'],
                                                y=CARD_POSITION['tableau_pile']['y'] + 10,
                                                tableau=game.get_tableau_pile()), [True, 0, -1])

        self.assertEqual(check_tableau_position(x=CARD_POSITION['tableau_pile']['x'] + 30,
                                                y=CARD_POSITION['tableau_pile']['y'] + 10,
                                                tableau=game.get_tableau_pile()), [True, 0, -1])

        self.assertEqual(check_tableau_position(x=3000,
                                                y=CARD_POSITION['tableau_pile']['y'] + 10,
                                                tableau=game.get_tableau_pile()), [False, None, None])

        self.assertEqual(check_tableau_position(x=CARD_POSITION['tableau_pile']['x'] + 2*CARD_POSITION['card_px']['x'] +\
                                                  2*CARD_POSITION['tableau_pile']['x_margin'],
                                                y=CARD_POSITION['tableau_pile']['y'] +\
                                                  CARD_POSITION['tableau_pile']['y_margin'] * len(mock_game_list[0].get_tableau_pile()[0]) + 1,
                                                tableau=game.get_tableau_pile()), [True, 2, -1])


class TestCheckGoalPosition(unittest.TestCase):
    def test_border_position(self):
        """
        Black-box test
        Test border values
        """
        self.assertEqual(check_goal_position(x=CARD_POSITION['goal_pile']['x'],
                                             y=CARD_POSITION['goal_pile']['y']), [True, 0])

        self.assertEqual(check_goal_position(x=CARD_POSITION['goal_pile']['x'] + CARD_POSITION['card_px']['x'],
                                             y=CARD_POSITION['goal_pile']['y']), [True, 0])

        self.assertEqual(check_goal_position(x=CARD_POSITION['goal_pile']['x'],
                                             y=CARD_POSITION['goal_pile']['y'] + CARD_POSITION['card_px']['y']),
                         [True, 0])

        self.assertEqual(check_goal_position(x=CARD_POSITION['goal_pile']['x'] + CARD_POSITION['card_px']['x'],
                                             y=CARD_POSITION['goal_pile']['y'] + CARD_POSITION['card_px']['y']),
                         [True, 0])

        self.assertEqual(check_goal_position(x=CARD_POSITION['goal_pile']['x'] + CARD_POSITION['goal_pile']['margin'] +
                                               CARD_POSITION['card_px']['x'],
                                             y=CARD_POSITION['goal_pile']['y']), [True, 1])

    def test_limits_position(self):
        """
        Black-box test
        Test limit values
        """
        self.assertEqual(check_goal_position(x=CARD_POSITION['goal_pile']['x'] + 1,
                                             y=CARD_POSITION['goal_pile']['y']), [True, 0])

        self.assertEqual(check_goal_position(x=CARD_POSITION['goal_pile']['x'] - 1,
                                             y=CARD_POSITION['goal_pile']['y']), [False, None])

        self.assertEqual(check_goal_position(x=CARD_POSITION['goal_pile']['x'] + CARD_POSITION['card_px']['x'],
                                             y=CARD_POSITION['goal_pile']['y'] + 1), [True, 0])

        self.assertEqual(check_goal_position(x=CARD_POSITION['goal_pile']['x'] - 1,
                                             y=CARD_POSITION['goal_pile']['y'] - 1), [False, None])

        self.assertEqual(check_goal_position(x=CARD_POSITION['goal_pile']['x'] - 1,
                                             y=CARD_POSITION['goal_pile']['y'] - 1), [False, None])


class TestInit(unittest.TestCase):
    def test_init(self):
        mock_db_score = MockDataBaseScore()
        controller = Controller(init_vista=False, mock_model_game=mock_db_score)

        pass

    def test_add_score(self):
        pass

