import json
from http import HTTPStatus

from src.data_access.ConnectionDataBase import ConnectionDataBase
from src.data_access.EasyConnection import EasyConnection
from src.model.Game import Game
from src.model.Personage import Personage
from src.model.Player import Player
from src.model.Rank import Rank
from src.model.Rol import Rol


class Player_game:
    def __init__(self):
        self.accountLevel = None
        self.game = None
        self.hoursPlayed = None
        self.note = None
        self.persongage = None
        self.id_player = None
        self.id_rank = None
        self.rol = None
        self.nickname = None

    def make_json_games_played_by_player(self) -> dict:
        info = {
            "accountLevel": self.accountLevel,
            "rank": self.id_rank,
            "name": self.game
        }
        return info

    def get_player_game_info(self):
        query = "SELECT * FROM player_game WHERE id_player = %s and game = %s;"
        values = [self.id_player, self.game]
        result = []
        result = ConnectionDataBase.select(query, values)
        player_game_info = None

        if result:
            game = Game()
            game.id = result[0]["game"]
            game.get_name()

            personage = Personage()
            personage.id = result[0]["personage"]
            personage.get_name()

            rank = Rank()
            rank.id = result[0]["id_rank"]
            rank.get_name()

            rol = Rol()
            rol.id = result[0]["rol"]
            rol.get_name()

            player_game_info = json.dumps({
                "accountLevel": result[0]["accountLevel"],
                "game": game.name,
                "hoursPlayed": result[0]["hoursPlayed"],
                "note": result[0]["note"],
                "personage": personage.name,
                "rank": rank.name,
                "rol": rol.name,
                "nickname": result[0]["nickname"]
            })
        return player_game_info

    def add_player(self) -> int:
        status = HTTPStatus.INTERNAL_SERVER_ERROR
        query = "CALL PA_register_player_game(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = [self.accountLevel, self.game, self.hoursPlayed, self.note, self.persongage, self.id_player,
                  self.id_rank, self.rol, self.nickname]
        if ConnectionDataBase.send_query(query, values):
            status = HTTPStatus.CREATED
        return status

    @staticmethod
    def get_games_played_by_player(nickname: str):
        games_id = None
        result = None
        player = Player()
        player.nickname = nickname
        id_player = player.get_id_by_nickname()
        games_played = []
        if id_player is not -1:
            query = "SELECT accountLevel, enumRank.rankName, game.name FROM player_game INNER JOIN enumRank ON" \
                    " player_game.id_rank = enumRank.id INNER JOIN game ON player_game.game = game.id_game WHERE" \
                    " id_player = %s;"
            values = [id_player]
            result = ConnectionDataBase.select(query, values)
            if result:
                for individual_game in result:
                    game_aux = Player_game()
                    game_aux.game = individual_game["name"]
                    game_aux.id_rank = individual_game["rankName"]
                    game_aux.accountLevel = individual_game["accountLevel"]
                    games_played.append(game_aux.make_json_games_played_by_player())
        return games_played

    @staticmethod
    def add_game(game_information: dict) -> int:
        status = HTTPStatus.BAD_REQUEST

        if game_information is not None:
            game_name = str(game_information["gameName"])
            if game_name == "valorant":
                status = 0
            else:
                status = HTTPStatus.NOT_IMPLEMENTED
        return status

    @staticmethod
    def register_lol_chmapions():
        f = open(r'C:\Users\Gerardo Soft\PycharmProjects\PlayTwogether\src\model\champions.json', encoding="utf8")
        data = json.load(f)

        query = "INSERT INTO enumPersonage(name) VALUES (%s);"

        for invividual in data:
            values = [invividual["name"]]
            ConnectionDataBase.send_query(query, values)
            print(invividual["name"])
        f.close()
