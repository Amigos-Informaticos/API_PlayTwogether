from http import HTTPStatus

from cryptography.fernet import Fernet, InvalidToken
from flask import session, Response, request

from datetime import datetime
from functools import update_wrapper
from typing import Any

from src.model.Player import Player


class Auth:
    secret_password: bytes = None

    @staticmethod
    def set_password():
        Auth.secret_password = Fernet.generate_key()

    @staticmethod
    def requires_token(operation):
        def verify_auth(*args, **kwargs):
            token = request.headers.get("token")
            saved_token = None
            try:
                saved_token = session["token"]
                if token is not None and saved_token is not None and token == saved_token:
                    session.modified = True
                    response = operation(*args, **kwargs)
                else:
                    response = Response(status=HTTPStatus.UNAUTHORIZED)
            except KeyError:
                if token is not None and saved_token is None:
                    response = Response(status=419)
                else:
                    response = Response(status=HTTPStatus.UNAUTHORIZED)
            return response

        return update_wrapper(verify_auth, operation)

    @staticmethod
    def administrator_permission():
        def decorator(operation):
            def verify_is_administrator(*args, **kwargs):
                token = request.headers.get("token")
                if token is not None:
                    token_values = Auth.decode_token(token)
                    if token_values["isModerator"] == "1":
                        response = operation(*args, **kwargs)
                    else:
                        response = Response(status=HTTPStatus.FORBIDDEN)
                else:
                    response = Response(status=HTTPStatus.FORBIDDEN)
                return response

            return update_wrapper(verify_is_administrator, operation)

        return decorator

    @staticmethod
    def requires_authentication():
        def decorator(operation):
            def verify_authentication(*args, **kwargs):
                token = request.headers.get("token")
                player_received = request.json
                if token is not None:
                    values = Auth.decode_token(token)
                    if values is not None:
                        if str(values["email"]) == str(player_received["email"]):
                            response = operation(*args, **kwargs)
                        else:
                            response = Response(status=HTTPStatus.FORBIDDEN)
                    else:
                        response = Response(status=HTTPStatus.FORBIDDEN)
                else:
                    response = Response(status=HTTPStatus.FORBIDDEN)
                return response

            return update_wrapper(verify_authentication, operation)
        return decorator

    @staticmethod
    def generate_token(player: Player) -> str:
        if Auth.secret_password is None:
            Auth.set_password()
        timestamp = datetime.now().strftime("%H:%M:%S")
        value: str = player.email + "/"
        value += player.password + "/"
        value += str(int(player.isModerator)) + "/"
        value += str(int(player.player_id)) + "/"
        value += timestamp
        token_value = Auth.encode(value, Auth.secret_password)
        print("El token es: ")
        print(token_value)
        return token_value

    @staticmethod
    def decode_token(token: str):
        try:
            if Auth.secret_password is None:
                Auth.set_password()
            decoded_token = Auth.decode(token, Auth.secret_password)
            decoded_token = decoded_token.split("/")
            return {
                "email": decoded_token[0],
                "password": decoded_token[1],
                "isModerator": decoded_token[2],
                "player_id": decoded_token[3]
            }
        except:
            return None

    @staticmethod
    def decode(value: str, key: bytes) -> str:
        return Fernet(key).decrypt(value.encode()).decode()

    @staticmethod
    def encode(value: str, key: bytes) -> str:
        return Fernet(key).encrypt(value.encode()).decode()
