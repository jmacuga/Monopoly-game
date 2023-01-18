import classes.fields_from_json as ffjson
from classes.board import Board, ColourError
from classes.field import Street, PropertyField, Field
from classes.player import Player
import pytest


class TestBoard:
    PROPERTY_FIELDS = "database/property_fields.json"
    NUM_OF_COLOUR = "database/number_of_colour.json"
    SPECIAL_FIELDS = "database/special_fields.json"
    CHANCE_CARDS = "database/chance_cards.json"
    property_fields = ffjson.property_fields_from_json(
        PROPERTY_FIELDS)
    num_of_colour = ffjson.number_of_colour_from_json(NUM_OF_COLOUR)
    special_fields = ffjson.special_fields_from_json(SPECIAL_FIELDS)
    chance_cards = ffjson.chance_cards_from_json(CHANCE_CARDS)

    colour = 'deep blue'
    colour_num = num_of_colour[colour]

    def test_board_get_field_by_id(self):
        board = Board(self.property_fields, self.num_of_colour)
        assert type(board.get_field_by_id(1)) == PropertyField
        assert type(board.get_field_by_id(6)) == Street
        assert board.get_field_by_id(6).colour() == 'yellow'

    def test_get_fields_owner(self):
        board = Board(self.property_fields, self.num_of_colour)
        player = Player()
        board.get_field_by_id(6).set_owner(player)
        assert board.get_fields_owner(6) == player

    def test_special_fields(self):
        board = Board(self.property_fields,
                      self.num_of_colour, self.special_fields)
        assert board.get_field_by_id(0).name() == 'start'

    def test_get_max_number_of_same_colour(self):
        board = Board(self.property_fields,
                      self.num_of_colour, self.special_fields)
        assert board.get_max_number_of_same_colour(
            self.colour) == self.colour_num

    def test_get_all_fields_of_colour(self):
        board = Board(self.property_fields,
                      self.num_of_colour, self.special_fields)
        result = board.get_all_fields_of_colour(self.colour)
        assert len(result) == self.colour_num
        assert isinstance(result[0], Field)
        assert result[0].colour() == self.colour

    def test_get_all_fields_of_colour_exception(self):
        board = Board(self.property_fields,
                      self.num_of_colour, self.special_fields)
        with pytest.raises(ColourError):
            board.get_all_fields_of_colour('turqoise')

    def test_get_new_chance_card(self):
        board = Board(self.property_fields,
                      self.num_of_colour,
                      self.special_fields,
                      self.chance_cards)
        assert board.get_new_chance_card() == self.chance_cards[0]
        assert board.get_new_chance_card() == self.chance_cards[1]
