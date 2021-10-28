from http import HTTPStatus

from flask import Blueprint, request, Response

from src.model.Game import Game

game_routes = Blueprint("game_routes", __name__)


@game_routes.route("player/game", methods=["POST"])
def add_game():
    game_recived = request.json
    status = Game.add_game(game_recived)
    response = Response(status=status)
    return response
