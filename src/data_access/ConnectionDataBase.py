from src.data_access.EasyConnection import EasyConnection


class ConnectionDataBase:
    connection = None

    @staticmethod
    def select(query, values):
        ConnectionDataBase.connection = EasyConnection()
        result = ConnectionDataBase.connection.select(query, values)
        return result

    @staticmethod
    def send_query(query, values):
        sent = False
        ConnectionDataBase.connection = EasyConnection()
        ConnectionDataBase.connection.send_query(query, values)
        sent = True
        return sent

    @staticmethod
    def close_connection():
        if ConnectionDataBase.connection.connection is not None:
            ConnectionDataBase.connection.close_connection()
            print("Conexion cerrada")
