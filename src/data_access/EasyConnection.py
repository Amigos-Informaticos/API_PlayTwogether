import mysql.connector
from mysql.connector import Error


class EasyConnection:
    def __init__(self):
        self.user = "amigo"
        self.password = "beethoven"
        self.database = "playTwogether"
        self.host = "amigosinformaticos.ddns.net"
        self.connection = None

    def connect(self, include_params: bool = False):
        self.connection = mysql.connector.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )
        return self.connection.cursor(prepared=include_params)

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()

    def send_query(self, query, values: list = None):
        executed = False
        if self.host is not None:
            parameters: tuple = ()
            try:
                if values is not None:
                    cursor = self.connect(True)
                    parameters = tuple(values)
                else:
                    cursor = self.connect()
                cursor.execute(query, parameters)
                self.connection.commit()
                executed = True
            except Error as error:
                print(f"Problem connecting to the database: {error}")
            finally:
                self.close_connection()
        return executed

    def select(self, query, values: list = None):
        results = []
        if self.host is not None:
            parameters: tuple = ()
            try:
                if values is not None:
                    cursor = self.connect(True)
                    parameters = tuple(values)
                else:
                    cursor = self.connect(False)
                cursor.execute(query, parameters)
                tmp_results = cursor.fetchall()
                for row in tmp_results:
                    results.append(dict(zip(cursor.column_names, row)))
            except Error as error:
                print(f"Problem connecting to the database: {error}")
            finally:
                self.close_connection()
        return results