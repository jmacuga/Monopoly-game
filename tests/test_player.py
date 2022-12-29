from classes.player import Player, JailError
import pytest


class TestPlayer:
    player1 = Player()
    player2 = Player()
    JAIL_FIELD_ID = 10

    def test_id(self):
        assert self.player1.player_id() == 0
        assert self.player2.player_id() == 1

    def test_move_pawn(self):
        assert self.player1.current_pawn_position() == 0
        self.player1.set_dice_roll_sum(9)
        self.player1.move_pawn()
        assert self.player1.current_pawn_position() == 9

    def test_set_position(self):
        self.player1.set_position(5, 15)
        assert self.player1.current_pawn_position() == 5

    def test_put_in_jail(self):
        self.player1.put_in_jail(self.JAIL_FIELD_ID)
        assert self.player1.is_in_jail()
        assert self.player1.current_pawn_position() == self.JAIL_FIELD_ID

    def test_jail_error_in_jail(self):
        self.player1.put_in_jail(self.JAIL_FIELD_ID)
        with pytest.raises(JailError):
            self.player1.put_in_jail(self.JAIL_FIELD_ID)

    def test_get_out_of_jail(self):
        self.player1.put_in_jail(self.JAIL_FIELD_ID)
        self.player1.get_out_of_jail()
        assert not self.player1.is_in_jail()

    def test_jail_error_not_in_jail(self):
        with pytest.raises(JailError):
            self.player1.get_out_of_jail()
