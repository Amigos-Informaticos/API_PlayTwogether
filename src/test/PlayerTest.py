from aifc import Error

from src.model.Player import Player
import pytest

player = Player()
player.email = "gerardo@gmail.com"

email_without_atsing = "gerardogmail.com"
email_withou_com = "gerardo@gmail"
institutional_email = "ZS18012187@estudiantes.uv.mx"
email_valid = "rendon.luisgerardo@gmail.com"
email_empty = ""

dict_player_valid = {
    "nickname": "Jorge",
    "gender": "F",
    "birthday": "1998-11-24",
    "email": "jorge@gmail.com",
    "password": "12345678",
    "startTime": 9,
    "endTime": 14
}


def test_get_id():
    assert player.get_id() == 1


def test_email_without_atsing():
    assert not Player.is_email(email_without_atsing).valid


def test_email_withou_com():
    assert not Player.is_email(email_withou_com).valid


def test_institutional_email():
    assert Player.is_email(institutional_email).valid


def test_email_valid():
    assert Player.is_email(email_valid).valid


def test_email_empty():
    assert not Player.is_email(email_empty).valid


def test_is_time_to_play_valid_string():
    assert not Player.is_time_to_play_valid("Hola", "5.5").valid


def test_is_time_to_play_valid_floats():
    assert not Player.is_time_to_play_valid("10.5", "20").valid


def test_is_time_to_play_valid_greater():
    assert not Player.is_time_to_play_valid("27", "29").valid


def test_is_time_to_play_valid_smaller_0():
    assert not Player.is_time_to_play_valid("-20", "-21").valid


def test_is_nickname_with_space():
    assert not Player.is_nickname("hola 98").valid


def test_is_nickname_smaller():
    assert not Player.is_nickname("123").valid


def test_is_nickname_valid_smaller():
    assert Player.is_nickname("Yira98").valid


def test_is_nickname_valid_greater():
    assert Player.is_nickname("123456789123456").valid


def test_is_gender_valid():
    assert Player.is_gender_valid("F")


def test_dict_player_valid():
    assert Player.validate_dict_to_singup(dict_player_valid)


def test_is_register_exception():
    expect_occurred = False
    try:
        player.is_registered()
    except Error:
        expect_occurred = True
    assert expect_occurred


def test_encrypt():
    password = Player.encode_password("1234567")
    print("La contra es")
    print(password)
    password_esperada = Player.encode_password("1234567")
    assert password == password_esperada


def test_password_contains_number():
    assert Player.password_contains_number("Hola9")


def test_password_donest_contains_number():
    assert not Player.password_contains_number("hola")


def test_not_pasword_valid_without_numbers():
    assert not Player.is_password_valid("holaaaaaaaa")


def test_not_pasword_valid_without_uper():
    assert not Player.is_password_valid("holaaaaaaaa99")


def test_not_password_valid_short():
    assert not Player.is_password_valid("Hola7")


def test_is_pasword_valid():
    assert not Player.is_password_valid("El7")


def test_encryp_pass():
    password = Player.encode_password("Beethoven1")
    print("La password es: ")
    print(password)
    assert True
