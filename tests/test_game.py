import classes.fields_from_json as ffjson
from classes.board import Board
from classes.field import Street, PropertyField
from classes.player import Player
from classes.game import Game


class TestGame:
    PROPERTY_FIELDS = "database/property_fields.json"
    NUM_OF_COLOUR = "database/number_of_colour.json"
    SPECIAL_FIELDS = "database/special_fields.json"
    CHANCE_CARDS = "database/chance_cards.json"
    property_fields = ffjson.property_fields_from_json(
        PROPERTY_FIELDS)
    num_of_colour = ffjson.number_of_colour_from_json(NUM_OF_COLOUR)
    special_fields = ffjson.special_fields_form_json(SPECIAL_FIELDS)
    board = Board(property_fields, num_of_colour, special_fields)
    player1 = Player()
    player2 = Player()
    max_rounds_num = 20
    INITIAL_MPP = 1500

    def test_prepare_pwans_on_start(self):
        Game(self.board, [self.player1, self.player2])
        assert self.board.get_field_by_id(0).get_players_on_ids(
        ) == [self.player1.player_id(), self.player2.player_id()]
        for p in (self.player1, self.player2):
            assert p.money() == self.INITIAL_MPP
