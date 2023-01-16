from __future__ import annotations
from classes.player import Player
from typing import Dict, List


class PlayerError(Exception):
    pass


class HousesNumError(Exception):
    pass


class HotelError(Exception):
    pass


class MortgageError(Exception):
    pass


class Field:
    def __init__(self, field_id: int, name: str):
        self._field_id = field_id
        self._name = name
        self._players_on = {}

    def field_id(self) -> int:
        return self._field_id

    def name(self) -> str:
        return self._name

    def get_players_on_ids(self) -> List:
        # returns list of ids of players that currently stand on field
        return list(self._players_on.keys())

    def put_player_on(self, player: Player) -> None:
        if player.player_id() in self._players_on:
            raise PlayerError('Player already on field')
        self._players_on[player.player_id()] = player

    def take_player_from(self, player: Player) -> None:
        if player.player_id() not in self._players_on:
            raise PlayerError('Player not on field')
        self._players_on.pop(player.player_id())

    def __str__(self) -> str:
        return f'{self._name}\nField id: {self._field_id}'

    def description_table(self) -> List[str, str]:
        return [['name', self._name], ['field id', self._field_id]]

    def step_on_description_table(self) -> List[str, str]:
        return [['name', self._name], ['field id', self._field_id]]


class PropertyField(Field):
    def __init__(self,
                 field_id: int,
                 name: str,
                 colour: str,
                 base_rent: int,
                 prices:  Dict[str, int],
                 other_rents: Dict[str, int]):
        super().__init__(field_id, name)
        self._other_rents = other_rents
        self._colour = colour
        self._base_rent = base_rent
        self._owner = None
        self._current_rent = base_rent
        self._price = prices["base_price"]
        self._mortgage = False

    def is_mortgaged(self):
        return self._mortgage

    def base_rent(self) -> int:
        return self._base_rent

    def colour(self) -> str:
        return self._colour

    def owner(self) -> Player:
        return self._owner

    def current_rent(self) -> int:
        return self._current_rent

    def set_owner(self, new_owner: Player) -> None:
        self._owner = new_owner

    def set_current_rent(self, new_rent: int) -> None:
        if new_rent < 0 or type(new_rent) is not int:
            raise ValueError('Rent must be positive integer')
        self._current_rent = new_rent

    def double_rent(self) -> None:
        self._current_rent = 2 * self._base_rent

    def price(self) -> int:
        return self._price

    def mortgage_price(self) -> int:
        return self._other_rents['mortgage']

    def total_value(self) -> int:
        return self.mortgage_price()

    def update_rent(self) -> None:
        self._current_rent = 0 if self._mortgage else self._base_rent

    def __str__(self) -> str:
        output_str = super().__str__()
        output_str += f'\ncolour: {self._colour}'
        output_str += f'\nrent: {self._current_rent}'
        return output_str

    def full_description_table(self) -> List[str, str]:
        table = super().description_table()
        if self._mortgage:
            table.append(['MORTGAGED', 'MORTGAGED'])
        table.append(['colour', self._colour])
        table.append(['rent', self._current_rent])
        table.append(['price', self._price])
        table.append(['mortgage price', self.mortgage_price()])
        return table

    def description_table(self) -> List[str, str]:
        table = super().description_table()
        if self._mortgage:
            table.append(['MORTGAGED', 'MORTGAGED'])
            return table
        table.append(['colour', self._colour])
        table.append(['rent', self._current_rent])
        table.append(['mortgage price', self.mortgage_price()])
        return table

    def step_on_description_table(self) -> List[str, str]:
        owner_name = '-'
        if self._owner is not None:
            owner_name = self._owner.name()
        table = super().step_on_description_table()
        table.append(
            ['owner', owner_name])
        if self._mortgage:
            table.append(['MORTGAGED', 'MORTGAGED'])
            return table
        table.append(['colour', self._colour])
        table.append(['rent', self._current_rent])
        table.append(['price', self._price])
        return table

    def do_mortgage(self):
        if self._mortgage:
            raise MortgageError('Field already mortgaged')
        self._mortgage = True
        self.update_rent()

    def lift_mortgage(self):
        if not self._mortgage:
            raise MortgageError('Field not mortgaged')
        self._mortgage = False
        self.update_rent()


class Street(PropertyField):
    def __init__(self,
                 field_id: int,
                 name: str,
                 colour: str,
                 rent: int,
                 prices: Dict[str, int],
                 other_rents: Dict[str, int]):
        super().__init__(field_id, name, colour, rent, prices, other_rents)
        self._prices = prices
        self._current_rent = self._base_rent
        self._houses_num = 0
        self._hotel = False

    def houses_num(self) -> int:
        return self._houses_num

    def hotel(self) -> bool:
        return self._hotel

    def add_house(self) -> None:
        if self._hotel or self._houses_num >= 4:
            raise ValueError
        self._houses_num += 1
        self.update_rent()

    def add_hotel(self) -> None:
        if self._hotel or self._houses_num < 4:
            raise ValueError
        self._hotel = True
        self._houses_num -= 4
        self.update_rent()

    def update_rent(self) -> None:
        new_rent = self._base_rent
        if self._houses_num == 1:
            new_rent = self._other_rents['w_one_house']
        elif self._houses_num == 2:
            new_rent = self._other_rents['w_two_houses']
        elif self._houses_num == 3:
            new_rent = self._other_rents['w_three_houses']
        elif self._houses_num == 4:
            new_rent = self._other_rents['w_four_houses']
        elif self._hotel:
            new_rent = self._other_rents['w_hotel']
        self._current_rent = new_rent

    def house_cost(self) -> int:
        return self._prices['house_cost']

    def hotel_cost(self) -> int:
        return self._prices['hotel_cost']

    def remove_house(self) -> None:
        if self._hotel or self.houses_num == 0:
            return
        self._houses_num -= 1
        self.update_rent()

    def remove_hotel(self) -> None:
        if self._hotel:
            return
        self._hotel = False
        self.update_rent()

    def total_value(self) -> int:
        if self.is_mortgaged():
            return 0
        value = self.mortgage_price() + self._houses_num * \
            self.house_cost()
        value += self.hotel_cost() if self._hotel else 0
        return value

    def __str__(self) -> str:
        output_str = super().__str__()
        output_str += f'\nnumber of houses: {self._houses_num}'
        output_str += f'\nhotel: {self._hotel}'
        return output_str

    def full_description_table(self) -> List[str, str]:
        table = super().full_description_table()
        table.append(['number of houses', self._houses_num])
        table.append(['hotel', 'yes' if self._hotel else 'no'])
        table.append(['house cost', self.house_cost()])
        table.append(['hotel cost', self.hotel_cost()])
        return table

    def description_table(self) -> List[str, str]:
        table = super().description_table()
        table.append(['number of houses', self._houses_num])
        table.append(['hotel', 'yes' if self._hotel else 'no'])
        return table

    def step_on_description_table(self) -> List[str, str]:
        table = super().step_on_description_table()
        table.append(['number of houses', self._houses_num])
        table.append(['hotel', 'yes' if self._hotel else 'no'])
        return table


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
