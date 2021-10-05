from http import HTTPStatus
from flask import Blueprint, request, Response

from src.model.player import Player

rutas_player = Blueprint("rutas_player", __name__)

@rutas_player.route("/players", methods = ["POST"])
def registrar_player():
    print(request)
    player_recibido = request.json
    respuesta = Response(status=HTTPStatus.BAD_REQUEST)
    valores_requeridos = {"name", "gender", "age", "email", "password"}
    if player_recibido is not None:
        if all(llave in player_recibido for llave in valores_requeridos):
            player = Player()
            player.instantiate_hashmap_to_register(player_recibido)
            if player.sign_up():
                #player_id = player.get_id()

                print("Player registrado!")
                print(player_recibido["email"])
                print("El id del player es: ")
                #print( player_id)
                respuesta = Response(status=HTTPStatus.OK)
            else:
                respuesta = Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
    return respuesta
