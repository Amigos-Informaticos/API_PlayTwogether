from src.data_access.ConnectionDataBase import ConnectionDataBase


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

