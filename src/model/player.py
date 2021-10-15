import json
from datetime import datetime, date
from http import HTTPStatus

from src.data_access.EasyConnection import EasyConnection
from src.model import Status


class Player:

    def __init__(self):
        self.nickname = None
        self.gender = None
        self.birthday = None
        self.status = None
        self.isModerator = None
        self.isVerified = None
        self.password = None
        self.email = None
        self.player_id = None

    def instantiate_hashmap_to_register(self, hash_player_received: dict):
        self.nickname = hash_player_received["nickname"]
        self.gender = hash_player_received["gender"]
        self.birthday = hash_player_received["birthday"]
        self.status = 1
        self.isModerator = False
        self.isVerified = False
        self.password = hash_player_received["password"]
        self.email = hash_player_received["email"]

    def instantiate_hashmap_to_login(self, hash_player_received: dict):
        self.email = hash_player_received["email"]
        self.password = hash_player_received["password"]

    def instantiate_hashmap_to_update(self, hashplayer_received: dict):
        self.email = hashplayer_received["email"]
        self.password = hashplayer_received["password"]
        self.nickname = hashplayer_received["nickname"]
        self.gender = hashplayer_received["gender"]

    def make_to_json_login(self, token):
        return json.dumps({
            "nickname": self.nickname,
            "isModerator": self.isModerator,
            "email": self.email,
            "token": token,
            "birthday": self.birthday,
            "gender": self.gender
        })

    def sign_up(self) -> bool:
        status = HTTPStatus.INTERNAL_SERVER_ERROR
        if not self.is_registered():
            query = "INSERT INTO player (nickname, gender, birthday, status, isModerator, isVerified, password, email) VALUES " \
                    "(%s, %s, %s, %s, %s, %s,  %s, %s);"
            values = [self.nickname, self.gender, self.birthday, self.status, self.isModerator, self.isVerified,
                      self.password,
                      self.email]
            self.send_query(query, values)
            status = HTTPStatus.CREATED
        else:
            status = HTTPStatus.CONFLICT
        return status

    def get_id(self) -> int:
        id_recovered = -1
        query = "SELECT player_id FROM player WHERE email = %s;"
        values = [self.email]
        resultado = self.select(query, values)
        id_recuperado = resultado[0]["player_id"]
        self.player_id = id_recuperado
        return id_recuperado

    def login(self) -> int:
        status = HTTPStatus.INTERNAL_SERVER_ERROR
        query = "SELECT * FROM player WHERE email = %s AND password = %s ;"
        values = [self.email, self.password]
        result = self.select(query,values)
        if len(result) > 0:
            self.nickname = result[0]["nickname"]
            self.isModerator = result[0]["isModerator"]
            self.birthday = result[0]["birthday"]
            self.gender = result[0]["gender"]
            status = HTTPStatus.OK
        else:
            status = HTTPStatus.NOT_FOUND
        return status

    def is_registered(self) -> bool:
        is_registered = False
        query = "SELECT * FROM player WHERE email = %s;"
        values = [self.email]
        result = self.select(query, values)
        if len(result) > 0:
            is_registered = True
        return is_registered

    def update(self) -> int:
        status = HTTPStatus.INTERNAL_SERVER_ERROR
        if self.is_registered():
            query = "UPDATE player SET nickname = %s, gender = %s, password = %s WHERE email = %s;"
            values = [self.nickname, self.gender, self.password, self.email]
            if self.send_query(query, values):
                status =HTTPStatus.OK
        else:
            status = HTTPStatus.NOT_FOUND
        return status

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
