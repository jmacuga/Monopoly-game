from classes.player import Player, JailError
import pytest
from classes.game_constants import GameConstants


def test_id():
    player1 = Player()
    player2 = Player()
    player1.set_players_id(0)
    player2.set_players_id(1)
    assert player1.player_id() == 0
    assert player2.player_id() == 1


def test_move_pawn():
    player1 = Player()
    assert player1.current_pawn_position() is None
    player1.set_position(0)
    assert player1.current_pawn_position() == 0
    player1.set_dice_roll_sum(9)
    player1.move_pawn()
    assert player1.current_pawn_position() == 9


def test_move_pawn_above_max_field_id():
    player1 = Player()
    player1.set_position(int(GameConstants.MAX_FIELD_ID))
    assert player1.current_pawn_position() == GameConstants.MAX_FIELD_ID
    player1.set_dice_roll_sum(3)
    player1.move_pawn()
    assert player1.current_pawn_position() == 2


def test_set_position():
    player1 = Player()
    player1.set_position(5)
    assert player1.current_pawn_position() == 5


def test_set_position_above_max_field_id():
    player1 = Player()
    player1.set_position(GameConstants.MAX_FIELD_ID)
    with pytest.raises(ValueError):
        player1.set_position(GameConstants.MAX_FIELD_ID + 1)


def test_put_in_jail():
    player1 = Player()
    player1.put_in_jail(GameConstants.MAX_FIELD_ID)
    assert player1.is_in_jail()
    assert player1.current_pawn_position() == GameConstants.MAX_FIELD_ID


def test_jail_error_in_jail():
    player1 = Player()
    player1.put_in_jail(GameConstants.JAIL_FIELD_ID)
    with pytest.raises(JailError):
        player1.put_in_jail(GameConstants.JAIL_FIELD_ID)


def test_get_out_of_jail():
    player1 = Player()
    player1.put_in_jail(GameConstants.JAIL_FIELD_ID)
    player1.get_out_of_jail()
    assert not player1.is_in_jail()


def test_jail_error_not_in_jail():
    player1 = Player()
    with pytest.raises(JailError):
        player1.get_out_of_jail()


def test_buy_property():
    player1 = Player()
    player1.buy_property(1)
    assert player1._owned_property_fields == {1}


def test_sell_property():
    player1 = Player()
    player1.buy_property(1)
    player1.buy_property(2)
    player1.sell_property(1)
    assert player1._owned_property_fields == {2}
