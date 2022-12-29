from __future__ import annotations
from typing import List, Dict
from .field import Field


class Board:
    def __init__(self, property_fields: List[Field],
                 num_of_fields_col: Dict[str, int],
                 special_fields: List[Field] = None,
                 chance_cards=None,
                 community_chest_cards=None):
        self._property_fields = property_fields
        self._special_fields = special_fields
        if self._special_fields is None:
            self._special_fields = []
        self._chance_cards = chance_cards
        self._comunity_chest_cards = community_chest_cards
        if chance_cards is None:
            self._chance_cards = []
        if community_chest_cards is None:
            self._community_chest_cards = []
        self._all_fields = self._property_fields + self._special_fields
        self._number_of_fields_colour = num_of_fields_col

    def get_field_by_id(self, id):
        for field in self._all_fields:
            if field.field_id() == id:
                return field
