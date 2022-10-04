import json
from os.path import exists


class DataBase:
    def __init__(self, data_base_path="../data/score.json"):
        assert(type(data_base_path) == str)
        self._db_path = data_base_path

        if exists(self._db_path):
            with open(self._db_path) as json_file:
                self._db_dict = json.load(json_file)
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

    def update_db(self):
        json_object = json.dumps(self.get_db())
        with open(self.get_db_path(), "w") as outfile:
            outfile.write(json_object)
