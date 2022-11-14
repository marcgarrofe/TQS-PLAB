import unittest
from src.model import DataBase
from test.mockObjectsGame import mock_game_list
from src.game import Game, game_to_dict
import os

DIRNAME = os.path.dirname(__file__)


class TestDataBase(unittest.TestCase):
    def test_init(self):
        """
        White-box test
        Test Model Class init
        """
        db = DataBase(data_base_path="test")
        self.assertNotEqual(db.get_db_path(), "")
        empty_db = []
        self.assertEqual(db.get_db(), empty_db)

        db = DataBase(data_base_path="../data/test_score.json")
        self.assertNotEqual(db.get_db_path(), "")
        score_test_db = [{
            "name": "Pau",
            "score": 100
            },
            {
            "name": "Marc",
            "score": 90
        }]
        self.assertEqual(db.get_db(), score_test_db)

        with self.assertRaisesRegex(TypeError, "Path to DB must be String type"):
            _ = DataBase(data_base_path=int(0))
        with self.assertRaisesRegex(ValueError, "Data base type allowed: score and game"):
            _ = DataBase(data_base_type='score_')

    def test_add_score(self):
        """
        Black-box test
        Test Model Class add score function
        """
        # Delete file if exists
        rel_db_path = "../data/test_add_score.json"
        abs_db_path = os.path.join(DIRNAME, rel_db_path)
        if os.path.exists(abs_db_path):
            os.remove(abs_db_path)

        db = DataBase(data_base_path=rel_db_path)
        db.add_score(player="Biel", score=150)
        score_test_db = [{
            "name": "Biel",
            "score": 150
        }]
        self.assertEqual(db.get_db(), score_test_db)

        db.add_score(player="Marc", score=10)
        score_test_db = [{
            "name": "Biel",
            "score": 150
            },
            {
            "name": "Marc",
            "score": 10
        }]
        self.assertEqual(db.get_db(), score_test_db)

        with self.assertRaisesRegex(TypeError, 'Only Score type DB can add new scores'):
            db = DataBase(data_base_type='game', data_base_path=rel_db_path)
            db.add_score(player="Biel", score=150)

    def test_save_game(self):
        """
        Black-box test
        Test Model Class save game function
        """
        # Define empty game
        game = Game(draw_pile=list(), goal_pile=list(), tableau_pile=list())
        db_score = DataBase(data_base_type='score')

        with self.assertRaisesRegex(TypeError, 'Only Game type DB can add new scores'):
            db_score.save_game(game)

        db_game = DataBase(data_base_type='game')
        with self.assertRaisesRegex(TypeError, 'Game must be provided in python dictionary type'):
            db_game.save_game(int(0))
        with self.assertRaisesRegex(TypeError, 'Game must be provided in python dictionary type'):
            db_game.save_game(game)

        game_dict = game_to_dict(game)
        self.assertTrue(len(game_dict['goal_pile']) == 0)
        self.assertTrue(len(game_dict['draw_pile']) == 0)
        self.assertTrue(len(game_dict['tableau_pile']) == 0)

        # Define mock game
        game_2 = Game(mock_game_list[3])
        game_dict_2 = game_to_dict(game_2)
        self.assertEqual(game_dict_2['goal_pile'], [
            [{'suit': 'diamonds', 'number': 1, 'reveled_state': True}],
            [{'suit': 'clubs', 'number': 1, 'reveled_state': True}],
            [], []
        ])
        self.assertEqual(game_dict_2['draw_pile'], [])
        self.assertEqual(game_dict_2['tableau_pile'], [
            [], [],
            [{'suit': 'spades', 'number': 1, 'reveled_state': True}],
            [{'suit': 'hearts', 'number': 3, 'reveled_state': True},
             {'suit': 'clubs', 'number': 2, 'reveled_state': True}],
            [], [], []
        ])

        # Test Error Values
        # Drop Tableau Key in Dict
        del game_dict_2['tableau_pile']
        with self.assertRaisesRegex(ValueError, 'Tableau Pile not in dictionary'):
            db_game.save_game(game_dict_2)
        # Drop Goal Key in Dict
        del game_dict_2['goal_pile']
        with self.assertRaisesRegex(ValueError, 'Goal Pile not in dictionary'):
            db_game.save_game(game_dict_2)
        # Drop Draw Key in Dict
        del game_dict_2['draw_pile']
        with self.assertRaisesRegex(ValueError, 'Draw Pile not in dictionary'):
            db_game.save_game(game_dict_2)

        # Test a Game Saving
        game = Game(game=mock_game_list[4])
        game_dict = game_to_dict(game)
        db_game.save_game(game_dict)

    def test_load_db(self):
        db = DataBase()
        # Acabar


class MockDataBaseScore(DataBase):
    def __init__(self):
        self._db_path = '../data/score.json'
        self._db_type = 'Score'
        self._db_dict = [{
            "name": "Biel",
            "score": 150
        }, {
            "name": "Marc",
            "score": 10
        }]
