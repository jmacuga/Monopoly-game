class FieldIdError(Exception):
    pass


class DiceSumError(Exception):
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
        self._owned_property_fields = {}
        self._current_dice_roll_sum = None
        self._is_in_jail = False
        self._money = 0
        self._current_pawn_position = 0

    def player_id(self):
        return self._player_id

    def current_dice_roll_sum(self):
        return self._current_dice_roll_sum

    def is_in_jail(self):
        return self._is_in_jail

    def money(self):
        return self._money

    def current_pawn_position(self):
        return self._current_pawn_position

    def set_dice_roll_sum(self, dice_sum):
        if dice_sum < 0 or dice_sum > 12:
            raise DiceSumError("dice sum must be between 0 and 12")
        self._current_dice_roll_sum = dice_sum

    def move_pawn(self):
        self._current_pawn_position += self._current_dice_roll_sum

    def set_position(self, field_id, num_of_fields):
        if field_id not in range(0, num_of_fields + 1):
            raise FieldIdError
        self._current_pawn_position = field_id

    def spend_money(self, amount):
        check_amount_of_money(amount)
        self._money -= amount

    def earn_money(self, amount):
        check_amount_of_money(amount)
        self._money += amount

    def buy_property(self, field_id: int):
        if type(field_id) is not int:
            raise TypeError
        if field_id in self._owned_property_fields:
            raise FieldIdError
        self._owned_property_fields.append(field_id)

    def get_owned_property_by_id(self, searched_id):
        for index, field_id in enumerate(self._owned_property_fields):
            if field_id == searched_id:
                return index

    def sell_property(self, field_id):
        if field_id not in self._owned_property_fields:
            raise FieldIdError
        index = self.get_owned_property_by_id(field_id)
        self._owned_property_fields.pop(index)

    def put_in_jail(self, JAIL_FIELD_ID):
        if self._is_in_jail:
            raise JailError("Player is already in jail")
        self._is_in_jail = True
        self._current_pawn_position = JAIL_FIELD_ID

    def get_out_of_jail(self):
        if not self._is_in_jail:
            raise JailError("Player is not in jail")
        self._is_in_jail = False
