from __future__ import annotations
from classes.player import Player


class HousesNumError(Exception):
    """"Raised when number of houses or hotels is incorrect."""
    pass


class MortgageError(Exception):
    """Raised when mortgage or lifting mortgage is not permitted."""
    pass


class Field:
    """Abstract class representing field on the board.

    Attributes
    ----------
    _field_id : int
        Field index
    _name : str
        Feild name
    """

    def __init__(self, field_id: int, name: str) -> None:
        """Initates field attributes

        Parameters
        ----------
        _field_id : int
            Field index
        _name : str
            Feild name
        """
        self._field_id = field_id
        self._name = name

    def field_id(self) -> int:
        """Gets index of the field."""
        return self._field_id

    def name(self) -> str:
        """Gets name of the field."""
        return self._name

    def __str__(self) -> str:
        """Gets the description of the field"""
        return f'{self._name}\nField id: {self._field_id}'

    def description_table(self) -> list[str, str]:
        """Gets the full descripition in form of table."""
        return [['name', self._name], ['field id', self._field_id]]

    def step_on_description_table(self) -> list[str, str]:
        """Gets the descripition in form of table."""
        return [['name', self._name], ['field id', self._field_id]]


class PropertyField(Field):
    """Class representing property field.

    Attributes
    ----------
    _field_id : int
        Field index
    _name : str
        Feild name
    _other_rents : Dict of str to int
        Dictionary of the rents other than base rent.
    _colour : str
        Property colour.
    _base_rent : int
        Rent that is valid when property is not upgraded
    _owner : Player
        The player who owns the field.
    _current_rent : int
        The rent that is currently valid.
    _price : int
        The amount of money required to buy a property.
    _mortgage : bool
        Is the field mortgaged.
    """

    def __init__(self,
                 field_id: int,
                 name: str,
                 colour: str,
                 base_rent: int,
                 prices:  dict[str, int],
                 other_rents: dict[str, int]):
        """Initates field attributes

        Parameters
        ----------
        field_id: int
            Field index.
        name: str
            Field name.
        colour: str
            Field colour.
        base_rent: int
            Rent that is valid when property is not upgraded.
        prices:  dict of str to int
            Dictionary of prices connected to the field. Required keys:
                                                        ["base_price"].
        other_rents: Dict of str to int
            Dictionary of the rents other than base rent. Required keys:
                                                ["mortgage", "owned_2"].
        """
        super().__init__(field_id, name)
        self._other_rents = other_rents
        self._colour = colour
        self._base_rent = base_rent
        self._owner = None
        self._current_rent = base_rent
        self._price = prices["base_price"]
        self._mortgage = False

    def is_mortgaged(self):
        """Checks if the field is mortgaged."""
        return self._mortgage

    def base_rent(self) -> int:
        """Gets the rent of the non-upgraded field."""
        return self._base_rent

    def colour(self) -> str:
        """Gets the colour of the field."""
        return self._colour

    def owner(self) -> Player:
        """Gets the owner of the field."""
        return self._owner

    def current_rent(self) -> int:
        """Gets the current rent."""
        return self._current_rent

    def set_owner(self, new_owner: Player) -> None:
        """Sets the new owner."""
        self._owner = new_owner

    def set_current_rent(self, new_rent: int) -> None:
        """Sets the current rent.
        Raises
        ------
        ValueError
            When new rent is less than zero or is not an integer.
        """
        if new_rent < 0 or type(new_rent) is not int:
            raise ValueError('Rent must be positive integer')
        self._current_rent = new_rent

    def double_rent(self) -> None:
        """Doubles the currnt rent."""
        self._current_rent = 2 * self._base_rent

    def price(self) -> int:
        """Gets the price of the property."""
        return self._price

    def mortgage_price(self) -> int:
        """Gets the price you earn for mortgagig the field."""
        return self._other_rents['mortgage']

    def total_value(self) -> int:
        """Gets the amount of money field can be sold it for."""
        return 0 if self._mortgage else 0.5 * self._price

    def update_rent(self) -> None:
        """Changes the rent according to the upgrades and mortgages."""
        self._current_rent = 0 if self._mortgage else self._base_rent

    def __str__(self) -> str:
        """Gets the basic description of field attributes."""
        output_str = super().__str__()
        output_str += f'\ncolour: {self._colour}'
        output_str += f'\nrent: {self._current_rent}'
        return output_str

    def full_description_table(self) -> list[str, str]:
        """Gets the full description of the field in form of table."""
        table = super().description_table()
        if self._mortgage:
            table.append(['MORTGAGED', 'MORTGAGED'])
        table.append(['colour', self._colour])
        table.append(['rent', self._current_rent])
        table.append(['price', self._price])
        table.append(['mortgage price', self.mortgage_price()])
        return table

    def description_table(self) -> list[str, str]:
        """Gets the description of main field attributes in form of table."""
        table = super().description_table()
        if self._mortgage:
            table.append(['MORTGAGED', 'MORTGAGED'])
            return table
        table.append(['colour', self._colour])
        table.append(['rent', self._current_rent])
        table.append(['mortgage price', self.mortgage_price()])
        return table

    def step_on_description_table(self) -> list[str, str]:
        """Gets the field dscription needed when player puts pawn on field."""
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

    def do_mortgage(self) -> None:
        """Set _mortgage flag to True and update the rent.

        Raises
        ------
        MortgageError
            If the field is already mortgaged."""
        if self._mortgage:
            raise MortgageError('Field already mortgaged')
        self._mortgage = True
        self.update_rent()

    def lift_mortgage(self) -> None:
        """Set _mortgage flag to False and update the rent.

        Raises
        ------
        MortgageError
            If the field is not mortgaged."""
        if not self._mortgage:
            raise MortgageError('Field not mortgaged')
        self._mortgage = False
        self.update_rent()

    def return_to_bank(self) -> None:
        """Removes mortgage and owner."""
        self._owner = None
        if self._mortgage:
            self.lift_mortgage()
        self.update_rent()


class Street(PropertyField):
    """Class representing Street field where you can build houses on.

    Attributes
    ----------
    _field_id : int
        Field index
    _name : str
        Feild name
    _other_rents : Dict of str to int
        Dictionary of the rents other than base rent.
    _colour : str
        Property colour.
    _base_rent : int
        Rent that is valid when property is not upgraded
    _owner : Player
        The player who owns the field.
    _current_rent : int
        The rent that is currently valid.
    _price : int
        The amount of money required to buy a property.
    _mortgage : bool
        Is the field mortgaged.
    _prices : dict of str to int
        dictionary of prices
    _houses_num : int
        Number of houses on the field.
    _hotel : bool
        Does the field have hotel on.
    """

    def __init__(self,
                 field_id: int,
                 name: str,
                 colour: str,
                 rent: int,
                 prices: dict[str, int],
                 other_rents: dict[str, int]):
        """Initates field attributes

        Parameters
        ----------
        field_id: int
            Field index.
        name: str
            Field name.
        colour: str
            Field colour.
        rent: int
            Rent that is valid when property is not upgraded.
        prices:  dict of str to int
            Dictionary of prices connected to the field. Required keys:
                            ["base_price", "house_cost", "hotel_cost"].
        other_rents: Dict of str to int
            Dictionary of the rents other than base rent. Required keys:
                        ["w_one_house","w_two_houses","w_three_houses",
                                    "w_four_houses","w_hotel","mortgage"].
        """
        super().__init__(field_id, name, colour, rent, prices, other_rents)
        self._prices = prices
        self._current_rent = self._base_rent
        self._houses_num = 0
        self._hotel = False

    def houses_num(self) -> int:
        """Gets the number of houses on the field."""
        return self._houses_num

    def hotel(self) -> bool:
        """Checks if hotel is no the field."""
        return self._hotel

    def add_house(self) -> None:
        """Adds house to the field and updates rent.

        Raises
        ------
        HousesNumError
            If on the field is hotel or the houses number not less than 4."""
        if self._hotel or self._houses_num >= 4:
            raise HousesNumError('There is already 4 houses or hotel on field')
        self._houses_num += 1
        self.update_rent()

    def add_hotel(self) -> None:
        """Adds hotel to the field and updates rent.

        Raises
        ------
        HousesNumError
            If on the field is hotel or the houses number less than 4."""
        if self._hotel or self._houses_num < 4:
            raise HousesNumError(
                'House is already on field or not enough houses')
        self._hotel = True
        self._houses_num = 0
        self.update_rent()

    def update_rent(self) -> None:
        """Updates rent accordingly to the current houses and hotels number."""
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
        """Gets the cost of one house."""
        return self._prices['house_cost']

    def hotel_cost(self) -> int:
        """Gets the cost of one hotel."""
        return self._prices['hotel_cost']

    def remove_house(self) -> None:
        """Removes the house from field and update rent.

        Raises
        ------
        HousesNumError
            If the houses num is equal to zero or there is a hotel on field."""
        if self._houses_num == 0 or self._hotel:
            raise HousesNumError
        self._houses_num -= 1
        self.update_rent()

    def remove_hotel(self) -> None:
        """Removes the hotel from fiel dand updates rent.

        Raises
        ------
        HousesNumError
            If there is not hotel on the field.
        """
        if not self._hotel:
            raise HousesNumError
        self._hotel = False
        self._houses_num = 4
        self.update_rent()

    def total_value(self) -> int:
        """Gets the amount of money the field can be sold for.

        Gets the sum of each house and hotel value, and half of the initial
        field price. If the field is mortgaged, returns 0."""
        if self._mortgage:
            return 0
        value = 0.5 * self._price + self._houses_num * \
            self.house_cost()
        value += self.hotel_cost() if self._hotel else 0
        return value

    def __str__(self) -> str:
        """Gets the basic description of field attributes."""
        output_str = super().__str__()
        output_str += f'\nnumber of houses: {self._houses_num}'
        output_str += f'\nhotel: {self._hotel}'
        return output_str

    def full_description_table(self) -> list[str, str]:
        """Gets the full description of the field in form of table."""
        table = super().full_description_table()
        table.append(['number of houses', self._houses_num])
        table.append(['hotel', 'yes' if self._hotel else 'no'])
        table.append(['house cost', self.house_cost()])
        table.append(['hotel cost', self.hotel_cost()])
        return table

    def description_table(self) -> list[str, str]:
        """Gets the description of main field attributes in form of table."""
        table = super().description_table()
        table.append(['number of houses', self._houses_num])
        table.append(['hotel', 'yes' if self._hotel else 'no'])
        return table

    def step_on_description_table(self) -> list[str, str]:
        """Gets the field dscription needed when player puts pawn on field."""
        table = super().step_on_description_table()
        table.append(['number of houses', self._houses_num])
        table.append(['hotel', 'yes' if self._hotel else 'no'])
        return table

    def return_to_bank(self):
        """Removes all field upgrades and owner."""
        super().return_to_bank()
        self._houses_num = 0
        self._hotel = False
        self.update_rent()


class SpecialField(Field):
    """Class representing special field such as start, jail or field.

    Attributes
    ----------
    _field_id : int
        Field index
    _name : str
        Feild name
    """

    def __init__(self, field_id, name):
        """Initates field attributes

        Parameters
        ----------
        _field_id : int
            Field index
        _name : str
            Feild name
        """
        super().__init__(field_id, name)
