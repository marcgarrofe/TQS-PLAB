import unittest
from src.model import DataBase
import os

DIRNAME = os.path.dirname(__file__)


class TestDataBase(unittest.TestCase):
    def test_init(self):
        db = DataBase("test")
        self.assertNotEqual(db.get_db_path(), "")
        empty_db = []
        self.assertEqual(db.get_db(), empty_db)

        db = DataBase("../data/test_score.json")
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
            _ = DataBase(int(0))

    def test_add_score(self):
        # Delete file if exists
        rel_db_path = "../data/test_add_score.json"
        abs_db_path = os.path.join(DIRNAME, rel_db_path)
        if os.path.exists(abs_db_path):
            os.remove(abs_db_path)

        db = DataBase(rel_db_path)
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

    def test_load_db(self):
        db = DataBase()
        # Acabar
