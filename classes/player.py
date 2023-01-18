from classes.game_constants import GameConstants
from tabulate import tabulate
from typing import Set


class FieldIdError(Exception):
    pass


class JailError(Exception):
    pass


def check_amount_of_money(amount):
    if type(amount) is not int:
        raise TypeError
    if amount < 0:
        raise ValueError


class Player:
    max_id = 0

    def __init__(self, name=None) -> None:
        self._player_id = Player.max_id
        Player.max_id += 1
        self._name = name
        if self._name is None:
            self._name = ''
        self._owned_property_fields = set()
        self._current_dice_roll_sum = None
        self._is_in_jail = False
        self._money = 0
        self._current_pawn_position = None
        self.passed_start_field = False
        self.is_bancrupt = False

    def player_id(self) -> int:
        return self._player_id

    def name(self) -> str:
        return self._name

    def set_players_id(self, new_id: int) -> None:
        if new_id < 0 or type(new_id) != int:
            raise ValueError
        self._player_id = new_id

    def current_dice_roll_sum(self) -> int:
        return self._current_dice_roll_sum

    def is_in_jail(self) -> bool:
        return self._is_in_jail

    def money(self) -> int:
        return self._money

    def current_pawn_position(self) -> int:
        return self._current_pawn_position

    def set_dice_roll_sum(self, dice_sum: int) -> None:
        self._current_dice_roll_sum = dice_sum

    def move_pawn(self) -> None:
        old_pos = self._current_pawn_position
        self._current_pawn_position = (
            self._current_pawn_position + self._current_dice_roll_sum) \
            % (GameConstants.MAX_FIELD_ID + 1)
        if self._current_dice_roll_sum > GameConstants.MAX_FIELD_ID - old_pos:
            self.passed_start_field = True
        else:
            self.passed_start_field = False

    def set_position(self, field_id: int) -> None:
        if field_id > GameConstants.MAX_FIELD_ID:
            raise ValueError
        self._current_pawn_position = field_id

    def spend_money(self, amount: int) -> None:
        check_amount_of_money(amount)
        self._money -= amount

    def earn_money(self, amount: int) -> None:
        check_amount_of_money(amount)
        self._money += amount

    def add_property(self, field_id: int) -> None:
        if type(field_id) is not int:
            raise TypeError
        if field_id in self._owned_property_fields:
            raise FieldIdError
        self._owned_property_fields.add(field_id)

    def remove_property(self, field_id: int) -> None:
        try:
            self._owned_property_fields.remove(field_id)
        except (KeyError):
            raise FieldIdError("Field already owned by player")

    def put_in_jail(self) -> None:
        if self._is_in_jail:
            raise JailError("Player is already in jail")
        self._is_in_jail = True
        self._current_pawn_position = GameConstants.JAIL_FIELD_ID

    def get_out_of_jail(self) -> None:
        if not self._is_in_jail:
            raise JailError("Player is not in jail")
        self._is_in_jail = False

    def owned_property_fields(self) -> Set[int]:
        return self._owned_property_fields

    def __str__(self) -> str:
        output = [['name', self._name],
                  ['money', self._money],
                  ['current position', self._current_pawn_position]]
        return tabulate(output, tablefmt='grid')
