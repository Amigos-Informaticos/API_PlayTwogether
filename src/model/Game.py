from http import HTTPStatus

from src.data_access.EasyConnection import EasyConnection
from src.model.Player import Player


class Game:

    @staticmethod
    def add_game(game_information: dict) -> int:
        status = HTTPStatus.BAD_REQUEST

        if game_information is not None:
            game_name = str(game_information["gameName"])
            if game_name == "valorant":
                status = Game.add_valorant(game_information)
            else:
                status = HTTPStatus.NOT_IMPLEMENTED
        return status

    @staticmethod
    def add_fortnite(fortnite_info: dict) -> int:
        status = HTTPStatus.INTERNAL_SERVER_ERROR
        return status

    @staticmethod
    def add_valorant(valorant_info: dict) -> int:
        status = HTTPStatus.INTERNAL_SERVER_ERROR
        if Game.validate_valorant_info(valorant_info):
            email = str(valorant_info["email"])
            player = Player()
            player.email = email

            if player.is_registered_and_active() and not Game.is_registred_valorant(email):
                query = "INSERT INTO valorant (hoursPlayed, rank, agent, nickname, id_player) VALUES (%s, %s, %s, %s, %s);"
                hours_played = int(valorant_info["hoursPlayed"])
                rank = int(valorant_info["rank"])
                agent = int(valorant_info["agent"])
                nickname = str(valorant_info["nickname"])

                id_player = player.get_id()
                values = [hours_played, rank, agent, nickname, id_player]
                Game.send_query(query, values)
                status = HTTPStatus.CREATED

            else:
                status = HTTPStatus.CONFLICT
        else:
            status = HTTPStatus.BAD_REQUEST
        return status

    @staticmethod
    def add_apex(apex_info: dict) -> int:
        status = HTTPStatus.INTERNAL_SERVER_ERROR
        return status

    @staticmethod
    def add_lol(lol_info: dict) -> int:
        status = HTTPStatus.INTERNAL_SERVER_ERROR
        return status

    @staticmethod
    def is_registered_fortnite(email) -> bool:
        is_registered = False
        player = Player()
        player.email = email
        player.get_id()
        if player.player_id is not None:
            query = "SELECT nickname FROM fortnite WHERE id_player = %s;"
            values = [player.player_id]
            result = Game.select(query, values)
            if len(result) > 0:
                is_registered = True

        return is_registered

    @staticmethod
    def is_registred_valorant(email) -> bool:
        is_registered = False
        player = Player()
        player.email = email
        player.get_id()
        if player.player_id is not None:
            query = "SELECT nickname FROM valorant WHERE id_player = %s;"
            values = [player.player_id]
            result = Game.select(query, values)
            if len(result) > 0:
                is_registered = True

        return is_registered

    @staticmethod
    def is_registred_apex(email) -> bool:
        is_registered = False
        player = Player()
        player.email = email
        player.get_id()
        if player.player_id is not None:
            query = "SELECT nickname FROM apexLegends WHERE id_player = %s;"
            values = [player.player_id]
            result = Game.select(query, values)
            if len(result) > 0:
                is_registered = True

        return is_registered

    @staticmethod
    def is_registred_lol(email) -> bool:
        is_registered = False
        player = Player()
        player.email = email
        player.get_id()
        if player.player_id is not None:
            query = "SELECT nickname FROM lol WHERE id_player = %s;"
            values = [player.player_id]
            result = Game.select(query, values)
            if len(result) > 0:
                is_registered = True

        return is_registered

    @staticmethod
    def validate_fortnite_info(fortnite_info: dict) -> bool:
        is_valid = False
        values_required = {"email", "hoursPlayed", "scrimsScore", "startSeason", "nickname"}

        if all(key in fortnite_info for key in values_required):
            email = str(fortnite_info["email"])
            hours_played = str(fortnite_info["scrimsScore"])
            start_season = str(fortnite_info["startSeason"])
            nickname = str(fortnite_info["nickname"])
            if Player.is_email(email) and Player.is_nickname(nickname) and Game.is_hours_played_valid(hours_played) \
                    and Game.is_valid_season(start_season):
                is_valid = True

        return is_valid

    @staticmethod
    def validate_valorant_info(valorant_info: dict) -> bool:
        is_valid = False
        values_required = {"email", "hoursPlayed", "rank", "agent", "nickname"}
        if all(key in values_required for key in values_required):
            email = str(valorant_info["email"])
            hours_played = str(valorant_info["hoursPlayed"])
            rank = str(valorant_info["rank"])
            agent = str(valorant_info["agent"])
            nickname = str(valorant_info["nickname"])

            if Player.is_email(email) and Player.is_nickname(nickname) and Game.is_hours_played_valid(hours_played)\
                    and Game.is_valid_agent_valorant(agent) and Game.is_valid_rank_valorant(rank):
                is_valid = True
        return is_valid

    @staticmethod
    def validate_apex_info(fortnite_info) -> bool:
        is_valid = False
        return is_valid

    @staticmethod
    def validate_lol_info(fortnite_info) -> bool:
        is_valid = False
        return is_valid

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

    @staticmethod
    def is_hours_played_valid(hours: str) -> bool:
        is_valid = False
        if hours.isdigit() and 100000 > int(hours) >= 0:
            is_valid = True

        return is_valid

    @staticmethod
    def is_valid_season(season: str) -> bool:
        is_valid = False
        if season.isdigit() and 8 < int(season) > 0:
            is_valid = True

        return is_valid

    @staticmethod
    def is_valid_rank_valorant(rank: str) -> bool:
        is_valid = False
        if rank.isdigit():
            rank_int = int(rank)
            if 7 > rank_int > 0 or 13 > rank_int > 10:
                is_valid = True

        return is_valid

    @staticmethod
    def is_valid_agent_valorant(agent: str) -> bool:
        is_valid = False
        if agent.isdigit():
            agent_int = int(agent)
            if 16 > agent_int > 0:
                is_valid = True

        return  is_valid
