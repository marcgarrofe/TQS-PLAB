import json
from os.path import exists, dirname, join

DIRNAME = dirname(__file__)


class DataBase:
    def __init__(self, data_base_path="../data/score.json"):
        if type(data_base_path) != str:
            raise TypeError("Path to DB must be String type")
        data_base_path = join(DIRNAME, data_base_path)

        self._db_path = data_base_path

        if exists(self._db_path):
            self._db_dict = self.load_db()
        else:
            self._db_dict = []

    def get_db_path(self):
        return self._db_path

    def get_db(self):
        return self._db_dict

    def add_score(self, player: str, score: int):
        new_score = {
            "name": player,
            "score": score
        }
        self._db_dict.append(new_score)
        self.update_db()

    def save_game(self, game):
        # Implementar
        pass

    def update_db(self):
        json_object = json.dumps(self.get_db())
        with open(self.get_db_path(), "w") as outfile:
            outfile.write(json_object)

    def load_db(self):
        with open(self._db_path) as json_file:
            db_dict = json.load(json_file)
        return db_dict
