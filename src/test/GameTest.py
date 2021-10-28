from src.model.Game import Game


def test_is_registered_fortnite():
    assert Game.is_registered_fortnite("rendon.luisgerardo@gmail.com")


def test_is_not_registered_fortnite():
    assert not Game.is_registered_fortnite("grimlicrash@outlook.com")


def test_is_registered_apex():
    assert Game.is_registred_apex("rendon.luisgerardo@gmail.com")


def test_is_not_registered_apex():
    assert not Game.is_registred_apex("grimlicrash@outlook.com")


def test_is_registered_valorant():
    assert Game.is_registred_valorant("rendon.luisgerardo@gmail.com")


def test_is_not_registered_valorant():
    assert not Game.is_registred_valorant("grimlicrash@outlook.com")


def test_is_registered_lol():
    assert Game.is_registred_lol("rendon.luisgerardo@gmail.com")


def test_is_not_registered_lol():
    assert not Game.is_registred_lol("grimlicrash@outlook.com")


def test_is_hours_played_valid():
    assert Game.is_hours_played_valid("99000")


def test_is_hours_played_invalid():
    assert not Game.is_hours_played_valid("-1")


def test_is_hours_played_invalid_decimal():
    assert not Game.is_hours_played_valid("99000.5")


def test_is_valid_rank_valorant():
    assert Game.is_valid_rank_valorant("1")


def test_is_valid_rank_valorant_greater():
    assert Game.is_valid_rank_valorant("12")


def test_is_invalid_rank_valorant_decimal():
    assert not Game.is_valid_rank_valorant("12.5")


def test_is_invalid_rank_valorant_cero():
    assert not Game.is_valid_rank_valorant("0")


def test_is_invalid_rank_valorant_negative():
    assert not Game.is_valid_rank_valorant("-1")


def test_is_invalid_rank_valorant_word():
    assert not Game.is_valid_rank_valorant("hola")


def test_is_valid_agent_valorant():
    assert Game.is_valid_agent_valorant("1")


def test_is_valid_agent_valorant_greater():
    assert Game.is_valid_agent_valorant("12")


def test_is_invalid_agent_valorant_greater():
    assert not Game.is_valid_agent_valorant("17")


def test_is_invalid_agent_valorant_negative():
    assert not Game.is_valid_agent_valorant("-1")


def test_is_invalid_agent_valorant_cero():
    assert not Game.is_valid_agent_valorant("0")


def test_is_invalid_agent_valorant_word():
    assert not Game.is_valid_agent_valorant("hola")
