from src.data_access.ConnectionDataBase import ConnectionDataBase


class Personage:
    def __init__(self):
        self.id = -1
        self.name = None

    def get_name(self) :
        result = None
        query = "SELECT name FROM enumPersonage WHERE id = %s;"
        values = [self.id]
        result = ConnectionDataBase.select(query, values)
        if result is not None:
            self.name = str(result[0]["name"])