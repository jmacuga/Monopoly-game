from __future__ import annotations
from .player import Player


class Field:
    def __init__(self, field_id, name):
        self._field_id = field_id
        self._name = name

    def field_id(self):
        return self._field_id

    def name(self):
        return self._name


class PropertyField(Field):
    def __init__(self, field_id, name, colour, base_rent):
        super().__init__(field_id, name)
        self._colour = colour
        self._rent = base_rent
        self._owner = None
        self._current_rent = base_rent

    def rent(self):
        return self._rent

    def colour(self):
        return self._colour

    def owner(self):
        return self._owner

    def current_rent(self):
        return self._current_rent

    def set_owner(self, new_owner: Player):
        self._owner = new_owner

    def set_current_rent(self, new_rent):
        if new_rent < 0 or type(new_rent) is not int:
            raise ValueError('Rent must be positie integer')
        self._current_rent = new_rent


class Street(PropertyField):
    def __init__(self, field_id, name, colour, rent, other_rents, prices):
        super().__init__(field_id, name, colour, rent)
        self._other_rents = other_rents
        self._prices = prices
        self._current_rent = self._rent
        self._houses_num = 0

    def houses_num(self):
        return self._houses_num


class Station(PropertyField):
    def __init__(self, field_id, name, colour, rent):
        super().__init__(field_id, name, colour, rent)


class ChanceField(Field):
    def __init__(self):
        super.__init__()


class CommunityChestField(Field):
    def __init__(self):
        super().__init__()


class IncomeTaxField(Field):
    def __init__(self):
        super().__init__()


class JailField(Field):
    def __init__(self):
        super().__init__()


class FreeParkingField(Field):
    def __init__(self):
        super().__init__()
