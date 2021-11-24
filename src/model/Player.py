import json
from datetime import datetime, date
from http import HTTPStatus

import cryptocode as cryptocode
from email_validator import validate_email, EmailNotValidError
from src.data_access.ConnectionDataBase import ConnectionDataBase
from src.model.Message import Message


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
        self.schedule = None

    def instantiate_hashmap_to_register(self, hash_player_received: dict):
        self.nickname = hash_player_received["nickname"]
        self.gender = hash_player_received["gender"]
        self.birthday = hash_player_received["birthday"]
        self.status = 1
        self.isModerator = False
        self.isVerified = False
        self.password = hash_player_received["password"]
        self.email = hash_player_received["email"]
        self.schedule = hash_player_received["schedule"]

    def instantiate_hashmap_to_login(self, hash_player_received: dict):
        self.email = hash_player_received["email"]
        self.password = hash_player_received["password"]

    def instantiate_hashmap_to_update(self, hashplayer_received: dict):
        self.email = hashplayer_received["email"]
        self.password = hashplayer_received["password"]
        self.nickname = hashplayer_received["nickname"]
        self.gender = hashplayer_received["gender"]
        self.schedule = hashplayer_received["schedule"]
        self.birthday = hashplayer_received["birthday"]

    def make_to_json_login(self, token):
        return json.dumps({
            "nickname": self.nickname,
            "isModerator": self.isModerator,
            "email": self.email,
            "token": token,
            "birthday": self.birthday.strftime('%Y-%m-%d'),
            "gender": self.gender
        })

    def make_json_players_found(self) -> dict:
        return {
            "nickname" : self.nickname,
            "isVerified" : self.isVerified,
            "birthday" : self.birthday
        }

    def sign_up(self) -> bool:
        status = HTTPStatus.INTERNAL_SERVER_ERROR
        if not self.is_registered():
            query = "INSERT INTO player (nickname, gender, birthday, status, isModerator, isVerified, password, email, schedule) VALUES " \
                    "(%s, %s, %s, %s, %s, %s, %s, %s, %s);"
            password_encryp =Player.encryp_password(self.password)
            values = [self.nickname, self.gender, self.birthday, self.status, self.isModerator, self.isVerified,
                      password_encryp, self.email, self.schedule]
            ConnectionDataBase.send_query(query, values)
            status = HTTPStatus.CREATED
        else:
            status = HTTPStatus.CONFLICT
        return status

    def get_id(self) -> int:
        id_recovered = -1
        query = "SELECT player_id FROM player WHERE email = %s;"
        values = [self.email]
        resultado = ConnectionDataBase.select(query, values)
        id_recuperado = resultado[0]["player_id"]
        self.player_id = id_recuperado
        return id_recuperado

    def get_id_by_nickname(self) -> int:
        id_recovered = -1
        query = "SELECT player_id FROM player WHERE nickname = %s;"
        values = [self.nickname]
        resultado = ConnectionDataBase.select(query, values)
        if len(resultado) > 0:
            id_recovered = resultado[0]["player_id"]
            self.player_id = id_recovered
        return id_recovered

    def login(self) -> int:
        status = HTTPStatus.INTERNAL_SERVER_ERROR
        query = "SELECT * FROM player WHERE email = %s AND password = %s AND status = 1 ;"
        password_encryp = Player.encryp_password(self.password)
        values = [self.email, password_encryp]
        result = ConnectionDataBase.select(query, values)
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
        query = "SELECT * FROM player WHERE email = %s OR nickname = %s;"
        values = [self.email, self.nickname]
        result = ConnectionDataBase.select(query, values)
        if len(result) > 0:
            is_registered = True
        return is_registered

    def is_registered_and_active(self) -> bool:
        is_registered = False
        query = "SELECT * FROM player WHERE email = %s and status = 1;"
        values = [self.email]
        result = ConnectionDataBase.select(query, values)
        if len(result) > 0:
            is_registered = True
        return is_registered

    def is_registered_and_active_nickname(self) -> bool:
        is_registered = False
        query = "SELECT * FROM player WHERE nickname = %s and status = 1;"
        values = [self.nickname]
        result = ConnectionDataBase.select(query, values)
        if len(result) > 0:
            is_registered = True
        return is_registered

    def update(self) -> int:
        status = HTTPStatus.INTERNAL_SERVER_ERROR
        if self.is_registered():
            query = "UPDATE player SET nickname = %s, gender = %s, password = %s, schedule = %s, birthday = %s WHERE" \
                    " email = %s;"
            values = [self.nickname, self.gender, self.password, self.schedule, self.birthday, self.email]
            if ConnectionDataBase.send_query(query, values):
                status = HTTPStatus.OK
        else:
            status = HTTPStatus.NOT_FOUND
        return status

    @staticmethod
    def is_email(email):
        is_valid = False
        try:
            valid = validate_email(email)
            is_valid = True
        except EmailNotValidError as e:
            is_valid = False
        return is_valid

    @staticmethod
    def is_min_age_valid(min_age: str) -> bool:
        is_valid = False
        if min_age.isdigit():
            min_age = int(min_age)
            if 30 > min_age > 0:
                is_valid = True
        return is_valid

    @staticmethod
    def is_hour_valid(time) -> bool:
        is_valid = False
        if 0 <= time <= 23:
            is_valid = True

        return is_valid

    @staticmethod
    def is_nickname(nickname: str):
        is_valid = False
        if 25 >= len(nickname) >= 4:
            contains_space = ' ' in nickname
            if not contains_space:
                is_valid = True
        return is_valid

    @staticmethod
    def is_gender_valid(gender: str):
        is_valid = False

        is_valid = gender.upper() == "F" or gender.upper() == "M" or gender.upper() == "O"

        return is_valid

    @staticmethod
    def calculate_age(born: date):
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    @staticmethod
    def is_birthday_valid(birthday: str):
        is_valid = False

        if Player.is_format_date(birthday):
            date = datetime.strptime(birthday, '%Y-%m-%d')
            age = Player.calculate_age(date)
            if 100 >= age > 12:
                is_valid = True

        return is_valid

    @staticmethod
    def is_format_date(date_text) -> bool:

        is_valid = False
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
            is_valid = True
        except ValueError:
            is_valid = False
        return is_valid

    @staticmethod
    def is_password_valid(password: str) -> bool:
        is_valid = False
        if len(password) > 0:
            is_valid = True

        return is_valid

    @staticmethod
    def validate_dict_to_singup(dict) -> bool:
        is_valid = False
        nickname = str(dict["nickname"])
        gender = str(dict["gender"])
        birthday = str(dict["birthday"])
        email = str(dict["email"])
        password = str(dict["password"])
        schedule = str(dict["schedule"])
        if Player.is_nickname(nickname) and Player.is_gender_valid(gender) \
                and Player.is_birthday_valid(birthday) and Player.is_email(email) \
                and Player.is_password_valid(password) \
                and Player.schedule_exist(schedule):
            is_valid = True

        return is_valid

    @staticmethod
    def schedule_exist(schedule: int) -> bool:
        query = "SELECT * FROM schedule WHERE schedule_id = %s;"
        values = [schedule]
        result = ConnectionDataBase.select(query, values)
        exist = len(result) > 0
        return exist

    def delete(self) -> int:
        status = HTTPStatus.INTERNAL_SERVER_ERROR
        if self.is_registered():
            query = "UPDATE player SET status = 2 WHERE email = %s AND status = 1;"
            values = [self.email]
            if ConnectionDataBase.send_query(query, values):
                status = HTTPStatus.OK
        else:
            status = HTTPStatus.NOT_FOUND

        return status

    def verify(self) -> int:
        status = HTTPStatus.INTERNAL_SERVER_ERROR
        if self.is_registered_and_active_nickname():
            query = "UPDATE player SET isVerified = 1 WHERE nickname = %s"
            values = [self.nickname]
            if ConnectionDataBase.send_query(query, values):
                status = HTTPStatus.OK
        else:
            status = HTTPStatus.NOT_FOUND
        return status

    def ban(self) -> int:
        status = HTTPStatus.INTERNAL_SERVER_ERROR
        if self.is_registered_and_active_nickname():
            query = "UPDATE player SET status = 3 WHERE nickname = %s AND status = 1;"
            values = [self.nickname]
            if ConnectionDataBase.send_query(query, values):
                status = HTTPStatus.OK
        else:
            status = HTTPStatus.NOT_FOUND
        return status

    def get_player_info(self):
        query = "SELECT gender, birthday, isVerified FROM player WHERE nickname = %s;"
        player_json = None
        values = [self.nickname]
        result = ConnectionDataBase.select(query, values)
        if len(result) > 0:
            self.birthday = result[0]["birthday"]
            self.gender = result[0]["gender"]
            self.isVerified = result[0]["isVerified"]
            player_json = json.dumps({
                "birthday": self.birthday.strftime('%Y-%m-%d'),
                "gender": self.gender,
                "isVerified": self.isVerified
            })
        return player_json

    @staticmethod
    def encryp_password(password: str) -> str:
        password_encryp = cryptocode.encrypt(password, "beethoven")
        return password_encryp


