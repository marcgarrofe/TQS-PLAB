import unittest
from src.controller import check_draw_position, check_tableau_position, check_goal_position, Controller
from src.vista import CARD_POSITION
from test.mockObjectsGame import mock_game_list


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

        self.assertEqual(check_tableau_position(x=CARD_POSITION['tableau_pile']['x'],
                                                y=CARD_POSITION['tableau_pile']['y'] + CARD_POSITION['card_px']['y'] + 10,
                                                tableau=game.get_tableau_pile()), [False, None, None])

        self.assertEqual(check_tableau_position(x=CARD_POSITION['tableau_pile']['x'],
                                                y=CARD_POSITION['tableau_pile']['y'] - 10,
                                                tableau=game.get_tableau_pile()), [False, None, None])


class TestCheckGoalPosition(unittest.TestCase):
    def test_border_position(self):
        """
        Black-box test
        Test border and limit values
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


class TestController(unittest.TestCase):
    def test_init(self):
        pass

    def test_add_score(self):
        pass
