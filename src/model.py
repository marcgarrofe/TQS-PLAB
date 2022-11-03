import json
from os.path import exists, dirname, join

DIRNAME = dirname(__file__)


class DataBase:
    def __init__(self, data_base_type='score', data_base_path="../data/score.json"):
        if type(data_base_path) != str:
            raise TypeError("Path to DB must be String type")
        data_base_path = join(DIRNAME, data_base_path)
        self._db_path = data_base_path

        if data_base_type not in ['score', 'game']:
            raise ValueError("Data base type allowed: score and game")
        self._db_type = data_base_type

        if exists(self._db_path):
            self._db_dict = self.load_db()
        else:
            self._db_dict = []

    def get_db_path(self):
        return self._db_path

    def get_db(self):
        return self._db_dict

    def add_score(self, player: str, score: int):
        if self._db_type != 'score':
            raise TypeError('Only Score type DB can add new scores')

        new_score = {
            "name": player,
            "score": score
        }
        self._db_dict.append(new_score)
        self.update_db()

    def save_game(self, game_dict: dict):
        if self._db_type != 'game':
            raise TypeError('Only Game type DB can add new scores')
        if type(game_dict) != dict:
            raise TypeError('Game must be provided in python dictionary type')
        if 'draw_pile' not in game_dict.keys:
            raise ValueError('Draw Pile not in dictionary')
        if 'goal_pile' not in game_dict.keys:
            raise ValueError('Goal Pile not in dictionary')
        if 'tableau_pile' not in game_dict.keys:
            raise ValueError('Tableau Pile not in dictionary')

        self._db_dict = game_dict
        self.update_db()

    def update_db(self):
        json_object = json.dumps(self.get_db(), indent=1)
        with open(self.get_db_path(), "w") as outfile:
            outfile.write(json_object)

    def load_db(self):
        with open(self._db_path) as json_file:
            db_dict = json.load(json_file)
        return db_dict
