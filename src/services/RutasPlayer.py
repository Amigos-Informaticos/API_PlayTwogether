import io
import json
from ftplib import FTP
from http import HTTPStatus
from sqlite3 import DatabaseError, InterfaceError
from tempfile import NamedTemporaryFile

from flask import Blueprint, request, Response, session, send_file

from src.model.Game import Game
from src.model.Player import Player
from src.model.Player_game import Player_game
from src.services.Auth import Auth

rutas_player = Blueprint("rutas_player", __name__)


@rutas_player.route("/players", methods=["POST"])
def sign_up():
    print(request)
    player_recibido = request.json
    response = Response(status=HTTPStatus.BAD_REQUEST)
    valores_requeridos = {"nickname", "gender", "birthday", "email", "password", "schedule"}
    if player_recibido is not None:
        if all(llave in player_recibido for llave in valores_requeridos):
            if Player.validate_dict_to_singup(player_recibido):
                player = Player()
                try:
                    player.instantiate_hashmap_to_register(player_recibido)
                    status_from_model = player.sign_up()
                    response = Response(status=status_from_model)
                except (DatabaseError, InterfaceError) as e:
                    response = Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
                    print(e)
    return response


@rutas_player.route("/login", methods=["POST"])
def login():
    print(request)
    player_received = request.json
    response = Response(status=HTTPStatus.BAD_REQUEST)
    values_required = {"email", "password"}
    if player_received is not None:
        if all(key in player_received for key in values_required):
            try:
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
            except (DatabaseError, InterfaceError) as e:
                response = Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
                print(e)

    return response


@rutas_player.route("/logout", methods=["GET"])
@Auth.requires_token
def logout():
    token = request.headers.get("token")
    session.clear()
    return Response(status=HTTPStatus.OK)


@rutas_player.route("/admin", methods=["POST"])
@Auth.administrator_permission()
def is_admin():
    response = Response(status=HTTPStatus.OK)
    return response


@rutas_player.route("/players", methods=["PUT"])
@Auth.requires_authentication()
def update():
    response = Response(status=HTTPStatus.BAD_REQUEST)
    player_received = request.json
    values_required = {"email", "password", "gender", "nickname", "schedule"}
    if all(key in player_received for key in values_required):
        player = Player()
        try:
            player.instantiate_hashmap_to_update(player_received)
            status_from_model = player.update()
            response = Response(status=status_from_model)
        except (DatabaseError, InterfaceError) as e:
            response = Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
            print(e)

    return response


@rutas_player.route("/players", methods=["DELETE"])
@Auth.requires_authentication()
def delete():
    status = HTTPStatus.BAD_REQUEST
    player_received = request.json
    values_required = {"email"}
    if all(key in player_received for key in values_required):
        player = Player()
        try:
            player.email = player_received["email"]
            status = player.delete()
            response = Response(status=status)
        except (DatabaseError, InterfaceError) as e:
            response = Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
            print(e)
    return response


@rutas_player.route("/players/<nickname>/verify", methods=["PATCH"])
@Auth.administrator_permission()
def verify(nickname):
    player = Player()
    player.nickname = nickname
    try:
        status_response = player.verify()
        response = Response(status=status_response)
    except (DatabaseError, InterfaceError) as e:
        response = Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        print(e)
    return response


@rutas_player.route("/players/<nickname>", methods=["GET"])
def get_player(nickname):
    response = Response(status=HTTPStatus.NOT_FOUND)
    player = Player()
    player.nickname = nickname
    try:
        player_json = player.get_player_info()
        if player_json is not None:
            response = Response(player_json,
                                status=HTTPStatus.OK,
                                mimetype="application/json")
    except (DatabaseError, InterfaceError) as e:
        response = Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        print(e)
    return response


@rutas_player.route("/players/<nickname>/ban", methods=["PATCH"])
def ban_player(nickname):
    player = Player()
    player.nickname = nickname
    response = Response(status=HTTPStatus.BAD_REQUEST)
    try:
        status_response = player.ban()
        response = Response(status=status_response)
    except (DatabaseError, InterfaceError) as e:
        response = Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        print(e)
    return response


@rutas_player.route("/players/<nickname>/image", methods=["POST"])
def add_image(nickname):
    image = request.files["image"]
    response = Response(status=HTTPStatus.BAD_REQUEST)
    saved = False
    ftp_connection = FTP("amigosinformaticos.ddns.net")
    ftp_connection.login("pi", "beethoven", "noaccount")
    ftp_connection.cwd("playt")
    command = f"STOR {nickname}.png"
    try:
        code = ftp_connection.storbinary(command, image.stream)
        code = code.split(" ")[0]
        if code == "226":
            response = Response(status=HTTPStatus.CREATED)
    except:
        response = Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
    finally:
        ftp_connection.close()
    return response


@rutas_player.route("/players/<nickname>/image", methods=["GET"])
def get_image(nickname):
    response = Response(status=HTTPStatus.NOT_FOUND)
    # ftp_connection = FTP("amigosinformaticos.ddns.net")
    # ftp_connection.login("pi", "beethoven", "noaccount")
    # ftp_connection.cwd("playt")

    # image = NamedTemporaryFile(mode="wrb+")

    # try:
    #  with open(image.name, "wb+") as open_file:
    #     command = f"RETR {nickname}.png"
    #    ftp_connection.retrbinary(command, open_file.write)

    # except:

    #   response = Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
    # finally:
    #   ftp_connection.close()

    # with open(image.name, "rb") as open_file:
    #   response = send_file(io.BytesIO(open_file.read()), mimetype="image/png", as_attachment=False)

    return response


@rutas_player.route("/play", methods=["GET"])
def play():

    schedule = request.args.__contains__("schedule")

    # info = request.json
    response = Response(status=HTTPStatus.BAD_REQUEST)
    # if Player_game.has_at_least_one_attribute(info) and Player_game.validate_info_to_search_player(info):
    # Player_game.find_player_by_atributes(info)
    # response = Response(status=HTTPStatus.OK)
    return response


@rutas_player.route("/players", methods=["GET"])
def search_players():
    response = Response(status=HTTPStatus.BAD_REQUEST)
    info = {}
    if request.args.__contains__("info_page"):
        info["info_page"] = str (request.args.get("info_page"))
        if request.args.__contains__("nickname"):
            info["nickname"] = str(request.args.get("nickname"))
        else:
            if request.args.__contains__("schedule"):
                info["schedule"] = str (request.args.get("schedule"))
            if request.args.__contains__("gender"):
                info["gender"] = str (request.args.get("gender"))
            if request.args.__contains__("min_age"):
                info["min_age"] = str (request.args.get("min_age"))
            if request.args.__contains__("game"):
                info["game"] = str (request.args.get("game"))

    if len(info) > 1:
        if Player_game.has_at_least_one_attribute(info) and Player_game.validate_info_to_search_player(info):
            result = Player_game.find_player_by_atributes(info)
            if len(result) > 0:
                players_json = json.dumps(result)
                response = Response(players_json, status=HTTPStatus.OK, mimetype="application/json")

    return response
