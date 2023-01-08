import classes.fields_from_json as ffjson
from classes.board import Board
from classes.field import Street, PropertyField, Field, SpecialField
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
    special_fields = ffjson.special_fields_from_json(SPECIAL_FIELDS)
    board = Board(property_fields, num_of_colour, special_fields)
    player1 = Player()
    player2 = Player()
    max_rounds_num = 20
    INITIAL_MPP = 1500
    game = Game(board, [player1, player2])

    def test_prepare_pwans_on_start(self):
        assert self.board.get_field_by_id(0).get_players_on_ids(
        ) == [self.player1.player_id(), self.player2.player_id()]
        for p in (self.player1, self.player2):
            assert p.money() == self.INITIAL_MPP

    def test_dice_roll(self, monkeypatch):
        monkeypatch.setattr(Game, 'current_dice_roll', lambda s: (1, 1))
        monkeypatch.setattr(Game, 'current_dice_sum', lambda s: sum((1, 1)))
        self.game.dice_roll()
        assert self.game.current_dice_roll() == (1, 1)
        assert self.game.current_dice_sum() == 2

    def test_current_field(self, monkeypatch):
        field = self.game.current_field()
        assert field.field_id() == 0
        assert type(field) is SpecialField

    def test_move_pawn_number_of_dots(self, monkeypatch):
        monkeypatch.setattr(Game, 'current_dice_sum', lambda s: sum((1, 1)))
        self.game.dice_roll()
        self.game.move_pawn_number_of_dots()
        field = self.game.current_field()
        assert self.game._current_player.current_pawn_position() == 2
        assert self.player1.player_id() in field.get_players_on_ids()

    def test_current_field_get_rent(self, monkeypatch):
        # monkeypatch.setattr(Game, 'current_dice_sum', lambda s: sum((1, 1)))
        # self.game.dice_roll()
        # self.game.move_pawn_number_of_dots()
        field = self.game.current_field()
        assert self.game._current_player.current_pawn_position() == 2
        assert type(field) == PropertyField
        assert field.owner() == None
        assert field.current_rent() == 50

    def test_player_can_afford():
        assert False
