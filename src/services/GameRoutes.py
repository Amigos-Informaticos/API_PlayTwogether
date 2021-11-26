import json
from http import HTTPStatus

from flask import Blueprint, request, Response
from mysql.connector.errors import DatabaseError, InterfaceError

from src.model.Game import Game
from src.model.Player import Player
from src.model.Player_game import Player_game
from src.services.Auth import Auth

game_routes = Blueprint("game_routes", __name__)


@game_routes.route("/players/<nickname>/<game>", methods=["GET"])
def get_game_played_by_player(nickname, game):
    response = Response(status=HTTPStatus.BAD_REQUEST)
    json_response = None
    if nickname is not None and game is not None:
        try:
            player = Player()
            player.nickname = nickname
            player.get_id_by_nickname()
            game_played = Game()
            game_played.name = game
            game_played.get_id()
            response = Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
            if game_played.id != -1 and player.player_id != -1:
                player_game = Player_game()
                player_game.id_player = player.player_id
                player_game.game = game_played.id
                json_response = player_game.get_player_game_info()
                if json_response is not None:
                    status_response = HTTPStatus.OK
                    response = Response(
                        json_response,
                        status=status_response,
                        mimetype="application/json"
                    )
            else:
                response = Response(status=HTTPStatus.NOT_FOUND)
        except (DatabaseError, InterfaceError):
            response = Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
    return response


@game_routes.route("/player/game", methods=["POST"])
@Auth.requires_authentication()
def add_game_played_by_player():
    player_game_json = request.json
    status_server = HTTPStatus.BAD_REQUEST
    response = Response(status=status_server)
    values_required = {"accountLevel", "game", "hoursPlayed", "note", "personage", "email", "id_rank", "rol",
                       "nickname"}
    if player_game_json is not None:
        if all(key in player_game_json for key in values_required):
            try:
                player_game = Player_game()
                if player_game.instantiate_hashmap_to_register(player_game_json):
                    player_game.add_player()
                    response = Response(status=HTTPStatus.OK)
            except (DatabaseError, InterfaceError) as e:
                response = Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
                print(e)
    return response


@game_routes.route("/players/<nickname>/games", methods=["GET"])
def get_games_played_by_player(nickname):
    response = Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
    try:
        games = Player_game.get_games_played_by_player(nickname)
        if len(games) > 0:
            games_json = json.dumps(games)
            response = Response(games_json, status=HTTPStatus.OK, mimetype="application/json")
        else:
            response = Response(status=HTTPStatus.NOT_FOUND)
    except (DatabaseError, InterfaceError) as e:
        response = Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        print(e)

    return response

@game_routes.route("/game/<name>/personages")
def get_personages(name):
    response = Response(status=HTTPStatus.NOT_FOUND)
    try:
        game = Game()
        game.name = name
        game.get_id()
        if game.id != -1:
            personages = game.get_personages()
            personages_json = json.dumps(personages)
            response = Response(personages_json, status=HTTPStatus.OK, mimetype="application/json")
    except (DatabaseError, InterfaceError) as e:
        response = Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
    return  response