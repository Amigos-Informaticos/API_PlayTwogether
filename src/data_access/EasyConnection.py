import json

import mysql.connector
from pathlib import Path


class EasyConnection:
    def __init__(self):
        self.user = ""
        self.password = ""
        self.database = ""
        self.host = ""
        self.init_with_json()
        self.connection = None

    def init_with_json(self):
        path = Path(__file__).parent / "./config.json"
        file = open(path)
        data = json.load(file)
        self.user = data['user']
        self.password = data['password']
        self.database = data['database']
        self.host = data['host']

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

            if values is not None:
                cursor = self.connect(True)
                parameters = tuple(values)
            else:
                cursor = self.connect()
            cursor.execute(query, parameters)
            self.connection.commit()
            executed = True
            self.close_connection()

        return executed

    def select(self, query, values: list = None):
        results = []
        if self.host is not None:
            parameters: tuple = ()
            if values is not None:
                cursor = self.connect(True)
                parameters = tuple(values)
            else:
                cursor = self.connect(False)
            cursor.execute(query, parameters)
            tmp_results = cursor.fetchall()
            for row in tmp_results:
                results.append(dict(zip(cursor.column_names, row)))
            self.close_connection()
        return results
