from __future__ import annotations
from typing import List, Dict
from classes.field import Field


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
        self._all_fields = self._generate_all_fields_dict()
        self._number_of_fields_colour = num_of_fields_col

    def _generate_all_fields_dict(self):
        all_fields = {}
        for field in self._property_fields + self._special_fields:
            all_fields[field.field_id()] = field
        return all_fields

    def get_field_by_id(self, field_id):
        return self._all_fields[field_id]

    def get_fields_owner(self, field_id):
        return self._all_fields[field_id].owner()
