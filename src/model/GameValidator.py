from src.model.Player_game import GameValidator
from src.model.Player import Player


class GameValidator:


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

            if Player.is_email(email) and Player.is_nickname(nickname) and GameValidator.is_hours_played_valid(hours_played) \
                    and Valorant.is_valid_agent_valorant(agent) and Valorant.is_valid_rank_valorant(rank):
                is_valid = True
        return is_valid

    @staticmethod
    def is_valid_agent_valorant(agent: str) -> bool:
        is_valid = False
        if agent.isdigit():
            agent_int = int(agent)
            if 16 > agent_int > 0:
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
    def is_registred_valorant(email) -> bool:
        is_registered = False
        player = Player()
        player.email = email
        player.get_id()
        if player.player_id is not None:
            query = "SELECT nickname FROM valorant WHERE id_player = %s;"
            values = [player.player_id]
            result = GameValidator.select(query, values)
            if len(result) > 0:
                is_registered = True

        return is_registered

    @staticmethod
    def is_hours_played_valid(hours: str) -> bool:
        is_valid = False
        if hours.isdigit() and 100000 > int(hours) >= 0:
            is_valid = True

        return is_valid

    @staticmethod
    def validate_fortnite_info(fortnite_info: dict) -> bool:
        is_valid = False
        values_required = {"email", "hoursPlayed", "scrimsScore", "startSeason", "nickname"}

        if all(key in fortnite_info for key in values_required):
            email = str(fortnite_info["email"])
            hours_played = str(fortnite_info["scrimsScore"])
            start_season = str(fortnite_info["startSeason"])
            nickname = str(fortnite_info["nickname"])
            if Player.is_email(email) and Player.is_nickname(nickname) and GameValidator.is_hours_played_valid(hours_played) \
                    and GameValidator.is_valid_season(start_season):
                is_valid = True

        return is_valid

