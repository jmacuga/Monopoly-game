import classes.fields_from_json as ffjson
from classes.board import Board
from classes.field import PropertyField, SpecialField
from classes.player import Player
from classes.game import Game
from classes.game_constants import GameConstants

PROPERTY_FIELDS = "database/property_fields.json"
NUM_OF_COLOUR = "database/number_of_colour.json"
SPECIAL_FIELDS = "database/special_fields.json"
CHANCE_CARDS = "database/chance_cards.json"


class TestGame:
    property_fields = ffjson.property_fields_from_json(
        PROPERTY_FIELDS)
    num_of_colour = ffjson.number_of_colour_from_json(NUM_OF_COLOUR)
    special_fields = ffjson.special_fields_from_json(SPECIAL_FIELDS)
    max_rounds_num = 20
    board = Board(property_fields, num_of_colour, special_fields)
    player1 = Player()
    player2 = Player()
    game = Game(board, [player1, player2])
    game.prepare_game()

    def test_prepare_pawns_on_start(self):
        assert self.board.get_field_by_id(0).get_players_on_ids(
        ) == [self.player1.player_id(), self.player2.player_id()]
        for p in (self.player1, self.player2):
            assert p.money() == GameConstants.INITIAL_MONEY_PP

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
        assert field.owner() is None
        assert field.current_rent() == 50

    def test_player_can_afford(self):
        price = 2000
        assert self.game.player_can_afford(price) is False
        price = 1000
        assert self.game.player_can_afford(price)

    def test_buy_current_property(self):
        field = self.game.current_field()
        assert type(field) == PropertyField
        self.game.buy_current_property()
        assert field.owner() == self.game._current_player.player_id()
        assert field.field_id() in self.game.\
            _current_player._owned_property_fields

    def test_change_player(self):
        assert self.game._cur_player_id_in_array == 0
        self.game.change_player()
        assert self.game._cur_player_id_in_array == 1
        assert self.game._current_player.player_id() ==\
            self.player2.player_id()
        assert self.game._current_player == self.player2


class TestHouseBuilding:
    property_fields = ffjson.property_fields_from_json(
        PROPERTY_FIELDS)
    num_of_colour = ffjson.number_of_colour_from_json(NUM_OF_COLOUR)
    special_fields = ffjson.special_fields_from_json(SPECIAL_FIELDS)
    max_rounds_num = 20
    board = Board(property_fields, num_of_colour, special_fields)
    player1 = Player()
    player2 = Player()
    game = Game(board, [player1, player2])
    game.prepare_game()
    test_fields_set = {5, 7}
    street_id1 = list(test_fields_set)[0]
    street_id2 = list(test_fields_set)[1]
    street1 = board.get_field_by_id(street_id1)
    street2 = board.get_field_by_id(street_id2)

    def test_can_build_house_first_house(self):
        self.player1._owned_property_fields = self.test_fields_set
        assert self.game.can_build_house(self.street_id1)

    def test_can_buid_house_uneven_houses(self):
        self.player1._owned_property_fields = self.test_fields_set
        self.board.get_field_by_id(self.street_id1).add_house()
        assert self.game.can_build_house(self.street_id1) is False
        self.board.get_field_by_id(self.street_id2).add_house()
        assert self.game.can_build_house(self.street_id1) is True

    def test_can_buid_house_fifth_house(self):
        self.player1._owned_property_fields = self.test_fields_set
        assert self.street1.houses_num() == 1
        for _ in range(0, 3):
            self.street1.add_house()
            self.street2.add_house()
        assert self.game.can_build_house(self.street_id1) is False

    def test_can_build_hotel_not_enough_houses(self):
        self.street1.remove_house()
        assert self.street1.houses_num() == 3
        assert self.street2.houses_num() == 4
        assert self.game.can_build_hotel(self.street_id1) is False

    def test_can_build_hotel_uneven_houses(self):
        assert self.game.can_build_hotel(self.street_id2) is False

    def test_can_build_hotel(self):
        self.street1.add_house()
        assert self.game.can_build_hotel(self.street_id1) is True
        assert self.game.can_build_hotel(self.street_id2) is True

    def test_can_build_hotel_second_hotel(self):
        self.street1.add_hotel()
        assert self.game.can_build_hotel(self.street_id1) is False

    def test_can_build_house_not_owned_all_of_colour(self):
        street_field_id = 6
        self.player1._owned_property_fields.add(street_field_id)
        assert self.game.can_build_house(street_field_id) is False

    def test_can_build_house_not_enough_money(self):
        self.street1.remove_hotel()
        self.street1.remove_house()
        self.street2.remove_house()
        assert self.game.can_build_house(self.street_id1)
        self.player1._money = 10
        assert self.game.can_build_house(self.street_id1) is False
