from http import HTTPStatus
from flask import Blueprint, request, Response, session

from src.model.player import Player
from src.services.Auth import Auth

rutas_player = Blueprint("rutas_player", __name__)

@rutas_player.route("/players", methods = ["POST"])
def sign_up():
    print(request)
    player_recibido = request.json
    respuesta = Response(status=HTTPStatus.BAD_REQUEST)
    valores_requeridos = {"nickname", "gender", "birthday", "email", "password"}
    if player_recibido is not None:
        if all(llave in player_recibido for llave in valores_requeridos):
            player = Player()
            player.instantiate_hashmap_to_register(player_recibido)
            if player.sign_up():
                print("Player registrado!")
                print(player_recibido["email"])
                print("El id del player es: ")
                respuesta = Response(status=HTTPStatus.OK)
            else:
                respuesta = Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
    return respuesta

@rutas_player.route("/login", methods= ["POST"])
def sign_in():
    print(request)
    player_received = request.json
    response = Response(status=HTTPStatus.BAD_REQUEST)
    values_required = {"email", "password"}
    if player_received is not None:
        if all(key in player_received for key in values_required):
            player = Player()
            player.instantiate_hashmap_to_login(player_received)
            result = player.login()

            if result == HTTPStatus.OK:
                player.get_id()
                token = Auth.generate_token(player)
                session.permanent = True
                session["token"] = token


                player_json = player.make_to_json_login(token)
                response = Response(
                    player_json,
                    status=HTTPStatus.OK,
                    mimetype="application/json"
                )
            else:
                response = Response(status=result)

    return response

@rutas_player.route("/admin", methods=["POST"])
@Auth.administrator_permission()
def is_admin():
    response = Response(status=HTTPStatus.OK)
    return response