from http import HTTPStatus

from flask import Blueprint, request, Response

from src.model.Game import Game
from src.model.Player import Player
from src.model.Player_game import Player_game

game_routes = Blueprint("game_routes", __name__)




@game_routes.route("/player/game", methods=["GET"])
def get_game_played_by_player():
    email = str(request.headers.get("email"))
    game_name = str(request.headers.get("game"))
    response = Response(status=HTTPStatus.BAD_REQUEST)
    status_response = HTTPStatus.BAD_REQUEST
    json_response = None

    if email is not None and game_name is not None:
        player = Player()
        player.email = email
        player.get_id()
        game = Game()
        game.name = game_name
        game.get_id()
        player_game = Player_game()
        player_game.id_player = player.player_id
        player_game.game = game.id
        json_response = player_game.get_player_game_info()
        if json_response is not None:
            status_response = HTTPStatus.OK
            response = Response(
                json_response,
                status=status_response,
                mimetype="application/json"
            )

    return response



