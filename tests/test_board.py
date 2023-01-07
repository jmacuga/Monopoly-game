import classes.fields_from_json as ffjson
from classes.board import Board
from classes.field import Street, PropertyField
from classes.player import Player


class TestBoard:
    PROPERTY_FIELDS = "database/property_fields.json"
    NUM_OF_COLOUR = "database/number_of_colour.json"
    SPECIAL_FIELDS = "database/special_fields.json"
    CHANCE_CARDS = "database/chance_cards.json"
    property_fields = ffjson.property_fields_from_json(
        PROPERTY_FIELDS)
    num_of_colour = ffjson.number_of_colour_from_json(NUM_OF_COLOUR)
    special_fields = ffjson.special_fields_from_json(SPECIAL_FIELDS)

    def test_board_get_field_by_id(self):
        board = Board(self.property_fields, self.num_of_colour)
        assert type(board.get_field_by_id(1)) == PropertyField
        assert type(board.get_field_by_id(6)) == Street
        assert board.get_field_by_id(6).colour() == 'blue'

    def test_get_fields_owner(self):
        board = Board(self.property_fields, self.num_of_colour)
        player = Player()
        board.get_field_by_id(4).set_owner(player)
        assert board.get_fields_owner(4) == player

    def test_special_fields(self):
        board = Board(self.property_fields,
                      self.num_of_colour, self.special_fields)
        assert board.get_field_by_id(0).name() == 'start'
