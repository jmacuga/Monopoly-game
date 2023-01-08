from __future__ import annotations
from classes.player import Player
from typing import Dict, List


class PlayerError(Exception):
    pass


class HousesNumError(Exception):
    pass


class HotelError(Exception):
    pass


class Field:
    def __init__(self, field_id: int, name: str):
        self._field_id = field_id
        self._name = name
        self._players_on = {}

    def field_id(self):
        return self._field_id

    def name(self):
        return self._name

    def get_players_on_ids(self) -> List:
        # returns list of ids of players that currently stand on field
        return list(self._players_on.keys())

    def put_player_on(self, player: Player):
        if player.player_id() in self._players_on:
            raise PlayerError('Player already on field')
        self._players_on[player.player_id()] = player

    def take_player_from(self, player: Player):
        if player.player_id() not in self._players_on:
            raise PlayerError('Player not on field')
        self._players_on.pop(player.player_id())


class PropertyField(Field):
    def __init__(self,
                 field_id: int,
                 name: str,
                 colour: str,
                 base_rent: int,
                 prices:  Dict[str, int]):
        super().__init__(field_id, name)
        self._colour = colour
        self._base_rent = base_rent
        self._owner = None
        self._current_rent = base_rent
        self._price = prices["base_price"]

    def base_rent(self):
        return self._base_rent

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
            raise ValueError('Rent must be positive integer')
        self._current_rent = new_rent

    def double_rent(self):
        self._current_rent = 2 * self._base_rent

    def price(self):
        return self._price


class Street(PropertyField):
    def __init__(self,
                 field_id: int,
                 name: str,
                 colour: str,
                 rent: int,
                 prices: Dict[str, int],
                 other_rents: Dict[str, int]):
        super().__init__(field_id, name, colour, rent, prices)
        self._other_rents = other_rents
        self._prices = prices
        self._current_rent = self._base_rent
        self._houses_num = 0
        self._hotels_num = 0

    def houses_num(self):
        return self._houses_num

    def hotels_num(self):
        return self._hotels_num

    def add_house(self):
        if self._hotels_num == 1:
            raise HousesNumError('There must not be more houses')
        if self._houses_num == 4:
            raise HousesNumError('There must not be more than four houses.')
        self._houses_num += 1
        self.update_rent()

    def add_hotel(self):
        if self._hotels_num == 1:
            raise HotelError("there must not be more than one hotel")
        if self._houses_num != 4:
            raise HotelError('There must be four houses to add a hotel')
        self._hotels_num += 1
        self._houses_num -= 4
        self.update_rent()

    def update_rent(self):
        new_rent = self._base_rent
        if self._houses_num == 1:
            new_rent = self._other_rents['w_one_house']
        elif self._houses_num == 2:
            new_rent = self._other_rents['w_two_houses']
        elif self._houses_num == 3:
            new_rent = self._other_rents['w_three_houses']
        elif self._houses_num == 4:
            new_rent = self._other_rents['w_four_houses']
        elif self._hotels_num == 1:
            new_rent = self._other_rents['w_hotel']
        self._current_rent = new_rent

    def house_cost(self):
        return self._prices['house_cost']

    def hotel_cost(self):
        return self._prices['hotel_cost']

    def mortgage_price(self):
        return self._other_rents['mortgage']


class SpecialField(Field):
    def __init__(self, field_id, name):
        super().__init__(field_id, name)


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
