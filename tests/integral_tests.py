from classes.board import Board
from classes.field import PropertyField
from classes.player import Player


def test_change_owner():
    player = Player()
    field1 = PropertyField(0, "field1", 'blue', 50)
    field2 = PropertyField(1, 'field2', 'blue', 50)
    board = Board([field1, field2], {'blue': 2})
    assert field1.owner() is None
    board.get_field_by_id(0).set_owner(player)
    assert field1.owner() == player
    board.get_field_by_id(1).set_owner(player)
    assert field2.owner() == player
