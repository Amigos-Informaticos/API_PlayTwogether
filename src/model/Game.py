from src.data_access.ConnectionDataBase import ConnectionDataBase
from src.model.Personage import Personage


class Game:
    def __init__(self):
        self.id = -1
        self.name = ""

    def get_name(self):
        result = None
        query = "SELECT name FROM game WHERE id_game = %s;"
        values = [self.id]
        result = ConnectionDataBase.select(query, values)
        if result is not None:
            self.name = str(result[0]["name"])

    def get_id(self):
        result = None
        query = "SELECT id_game FROM game WHERE name = %s;"
        values = [self.name]
        result =ConnectionDataBase.select(query, values)
        if result:
            self.id = result[0]["id_game"]

    def get_personages(self):
        personages = []
        query = "SELECT id, name_personage from enumPersonage WHERE game_id = %s;"
        values = [self.id]
        result = ConnectionDataBase.select(query, values)
        for individual_personage in result:
            personage = Personage()
            personage.id = individual_personage["id"]
            personage.name = individual_personage["name_personage"]
            personages.append(personage.make_json())

        return personages
