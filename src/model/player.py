from src.data_access.EasyConnection import EasyConnection
from src.model import Status


class Player:

    def __init__(self):
        self.name = None
        self.gender = None
        self.age = None
        self.status = None
        self.isModerator = None
        self.isVerified = None
        self.password = None
        self.email = None
        self.player_id = None

    def instantiate_hashmap_to_register(self, hash_player_received: dict):
        self.name= hash_player_received["name"]
        self.gender = hash_player_received["gender"]
        self.age = hash_player_received["age"]
        self.status = Status.ACTIVO
        self.isModerator = False
        self.isVerified = False
        self.password = hash_player_received["password"]
        self.email = hash_player_received["email"]


    def sign_up(self) -> bool:
        registered = False
        conexion = EasyConnection()
        query = "INSERT INTO player (nickname, email, password) VALUES (%s, %s, %s) ;"
        values = [self.nickname, self.email, self.password]
        conexion.send_query(query, values)
        registered = True
        return registered
