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

    def sign_up(self) -> bool:
        registered = False
        conexion = EasyConnection()
        query = "INSERT INTO player (nickname, gender, birthday, status, isModerator, isVerified, password, email) VALUES " \
                "(%s, %s, %s, %s, %s, %s,  %s, %s);"
        values = [self.nickname, self.gender, self.birthday, self.status, self.isModerator, self.isVerified, self.password,
                  self.email]
        conexion.send_query(query, values)
        registered = True
        return registered

    def get_id(self) -> int:
        id_recuperado =-1
        query = "SELECT player_id FROM player WHERE email = %s;"
        values = [self.email]
        conexion = EasyConnection()
        resultado = conexion.send_query(query,values)
        id_recuperado = resultado [0]["player_id"]
        self.player_id = id_recuperado
        return id_recuperado



