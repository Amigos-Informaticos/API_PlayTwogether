from src.model.GameValidator import GameValidator


def test_is_registered_valorant():
    assert GameValidator.is_registred_valorant("rendon.luisgerardo@gmail.com")


def test_is_not_registered_valorant():
    assert not GameValidator.is_registred_valorant("grimlicrash@outlook.com")


def test_is_hours_played_valid():
    assert GameValidator.is_hours_played_valid("99000")


def test_is_hours_played_invalid():
    assert not GameValidator.is_hours_played_valid("-1")


def test_is_hours_played_invalid_decimal():
    assert not GameValidator.is_hours_played_valid("99000.5")


def test_is_valid_rank_valorant():
    assert GameValidator.is_valid_rank_valorant("1")


def test_is_valid_rank_valorant_greater():
    assert GameValidator.is_valid_rank_valorant("12")


def test_is_invalid_rank_valorant_decimal():
    assert not GameValidator.is_valid_rank_valorant("12.5")


def test_is_invalid_rank_valorant_cero():
    assert not GameValidator.is_valid_rank_valorant("0")


def test_is_invalid_rank_valorant_negative():
    assert not GameValidator.is_valid_rank_valorant("-1")


def test_is_invalid_rank_valorant_word():
    assert not GameValidator.is_valid_rank_valorant("hola")


def test_is_valid_agent_valorant():
    assert GameValidator.is_valid_agent_valorant("1")


def test_is_valid_agent_valorant_greater():
    assert GameValidator.is_valid_agent_valorant("12")


def test_is_invalid_agent_valorant_greater():
    assert not GameValidator.is_valid_agent_valorant("17")


def test_is_invalid_agent_valorant_negative():
    assert not GameValidator.is_valid_agent_valorant("-1")


def test_is_invalid_agent_valorant_cero():
    assert not GameValidator.is_valid_agent_valorant("0")


def test_is_invalid_agent_valorant_word():
    assert not GameValidator.is_valid_agent_valorant("hola")
