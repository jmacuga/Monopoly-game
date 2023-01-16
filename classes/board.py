from __future__ import annotations
from typing import List, Dict
from classes.field import Field
from itertools import cycle


class Board:
    def __init__(self, property_fields: List[Field],
                 num_of_fields_col: Dict[str, int],
                 special_fields: List[Field] = None,
                 chance_cards=None):
        self._property_fields = property_fields
        if special_fields is None:
            special_fields = []
        self._special_fields = special_fields
        if chance_cards is None:
            chance_cards = []
        self._chance_cards = cycle(chance_cards)
        self._all_fields = self._generate_all_fields_dict()
        self._number_of_fields_colour = num_of_fields_col
        self.current_chance_card = None

    def _generate_all_fields_dict(self) -> Dict[int, Field]:
        all_fields = {}
        for field in self._property_fields + self._special_fields:
            all_fields[field.field_id()] = field
        return all_fields

    def get_field_by_id(self, field_id: int) -> Dict[int, Field]:
        return self._all_fields[field_id]

    def get_fields_owner(self, field_id: int) -> int:
        return self._all_fields[field_id].owner()

# TODO test
    def get_max_number_of_same_colour(self, colour: str) -> int:
        return self._number_of_fields_colour[colour]

# TODO test
    def get_all_fields_of_colour(self, colour: str) -> List[Field]:
        same_colour = []
        for f in self._property_fields:
            if f.colour() == colour:
                same_colour.append(f)
        return same_colour

    def get_new_chance_card(self):
        self.current_chance_card = next(self._chance_cards)
        return self.current_chance_card

    def current_chance_card(self):
        return self.current_chance_card
