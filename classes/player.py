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
    """Object representing player

    Attributes
    ----------
    _name : str
        player's name
    _owned_property_fields : set
        set of indices of fields owned by player
    _current_dice_roll_sum : int
        sum of the dots on dice
    _is_in_jail : bool
        is the player in jail;
    _money : int
        amount of money owned by player
    _current_pawnPosition : int
        index of field the player is currently on
    pased_start_field
        has theplayer passed start field in last move
    is_bancrupt
        is player bancrupt
    """

    def __init__(self, name: str = None) -> None:
        """Initiates object atributes.

        Parameters
        ----------
        name : str, optional
            name of the player
        """
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

    def name(self) -> str:
        """Get player's name."""
        return self._name

    def current_dice_roll_sum(self) -> int:
        """Get current result of dice roll."""
        return self._current_dice_roll_sum

    def is_in_jail(self) -> bool:
        """Check if the player is currently in jail."""
        return self._is_in_jail

    def money(self) -> int:
        """Get current amount of money owned by th eplayer."""
        return self._money

    def current_pawn_position(self) -> int:
        """Get index of field that player is currently on."""
        return self._current_pawn_position

    def set_dice_roll_sum(self, dice_sum: int) -> None:
        """Set the result of dice roll.

        Parameters
        ----------
        dice_sum : int
            New current sum of dots on dice.
        """
        self._current_dice_roll_sum = dice_sum

    def move_pawn(self) -> None:
        """Change player's position by the current dice sum."""
        old_pos = self._current_pawn_position
        self._current_pawn_position = (
            self._current_pawn_position + self._current_dice_roll_sum) \
            % (GameConstants.MAX_FIELD_ID + 1)
        if self._current_dice_roll_sum > GameConstants.MAX_FIELD_ID - old_pos:
            self.passed_start_field = True
        else:
            self.passed_start_field = False

    def set_position(self, field_id: int) -> None:
        """Set current player's position to given field index."""
        if field_id > GameConstants.MAX_FIELD_ID:
            raise ValueError
        self._current_pawn_position = field_id

    def spend_money(self, amount: int) -> None:
        """Decrease player's money by give amount."""
        check_amount_of_money(amount)
        self._money -= amount

    def earn_money(self, amount: int) -> None:
        """Increase player's money by given amount."""
        check_amount_of_money(amount)
        self._money += amount

    def add_property(self, field_id: int) -> None:
        """Add given field index to the set of fields owned by player.

        Parameters
        ----------
        field_id : int
            Index of added field

        Raises
        ------
        TypeError
            if the field_id is not int
        FieldError
            If the field_id is already in the owned set
        """
        if type(field_id) is not int:
            raise TypeError
        if field_id in self._owned_property_fields:
            raise FieldIdError
        self._owned_property_fields.add(field_id)

    def remove_property(self, field_id: int) -> None:
        """Remove given property id from set of owned fields.

        Parameters
        ----------
        field_id : int
            Index of removed field

        Raises
        ------
        FieldError
            If the field_id is not in the owned set
        """
        try:
            self._owned_property_fields.remove(field_id)
        except (KeyError):
            raise FieldIdError("Field nou owned by player")

    def put_in_jail(self) -> None:
        """Sets is in jail flag to true.

        Raises
        ------
        JailError
            If player is already in jail.
        """
        if self._is_in_jail:
            raise JailError("Player is already in jail")
        self._is_in_jail = True
        self._current_pawn_position = GameConstants.JAIL_FIELD_ID

    def get_out_of_jail(self) -> None:
        """Sets _is_in_jail flag to False.

        Raises
        ------
        JailError
            If player is not in jail.
        """
        if not self._is_in_jail:
            raise JailError("Player is not in jail")
        self._is_in_jail = False

    def owned_property_fields(self) -> Set[int]:
        """Gets set of indices of fields owned by the player."""
        return self._owned_property_fields

    def __str__(self) -> str:
        """Gets name, money and current position of player in table format"""
        output = [['name', self._name],
                  ['money', self._money],
                  ['current position', self._current_pawn_position]]
        return tabulate(output, tablefmt='grid')
