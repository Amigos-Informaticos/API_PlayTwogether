from http import HTTPStatus

from src.model.Player_game import Player_game

player_game = Player_game()
player_game.accountLevel = 77
player_game.game = 1
player_game.hoursPlayed = 500
player_game.note = "Soy muy buen jugador y he ganado muchos torneos"
player_game.persongage = 1
player_game.id_player = 4
player_game.id_rank = 1
player_game.rol = 11


def test_add_player():
    assert player_game.add_player() == HTTPStatus.CREATED


def test_get_player_game_information():
    json_info = player_game.get_player_game_info()
    game_name = json_info[0]
    print(json_info)
    assert game_name == "valorant"


def test_search_player():
    info = {"nickname": "efra"}
    result = Player_game.find_player(info)
    assert len(result) > 0
