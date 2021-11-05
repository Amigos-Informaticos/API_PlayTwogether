from src.data_access.EasyConnection import EasyConnection


class ConnectionDataBase:

    @staticmethod
    def select(query, values):
        connection = EasyConnection()
        result = connection.select(query, values)
        return result

    @staticmethod
    def send_query(query, values):
        sent = False
        connection = EasyConnection()
        connection.send_query(query, values)
        sent = True
        return sent
