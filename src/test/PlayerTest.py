from src.model.player import Player
import pytest

player = Player()
player.email = "gerardo@gmail.com"


def test_get_id():
    assert player.get_id() == 1
