from classes.player import Player, JailError
import pytest


JAIL_FIELD_ID = 10


def test_id():
    player1 = Player()
    player2 = Player()
    assert player1.player_id() == 0
    assert player2.player_id() == 1


def test_move_pawn():
    player1 = Player()
    assert player1.current_pawn_position() == 0
    player1.set_dice_roll_sum(9)
    player1.move_pawn()
    assert player1.current_pawn_position() == 9


def test_set_position():
    player1 = Player()
    player1.set_position(5, 15)
    assert player1.current_pawn_position() == 5


def test_put_in_jail():
    player1 = Player()
    player1.put_in_jail(JAIL_FIELD_ID)
    assert player1.is_in_jail()
    assert player1.current_pawn_position() == JAIL_FIELD_ID


def test_jail_error_in_jail():
    player1 = Player()
    player1.put_in_jail(JAIL_FIELD_ID)
    with pytest.raises(JailError):
        player1.put_in_jail(JAIL_FIELD_ID)


def test_get_out_of_jail():
    player1 = Player()
    player1.put_in_jail(JAIL_FIELD_ID)
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
