import classes.fields_from_json as ffjson
from classes.board import Board
from classes.field import PropertyField, SpecialField, Street
from classes.field import HousesNumError, MortgageError
from classes.player import Player
from classes.game import Game, StartFieldError
from classes.game_constants import GameConstants
import pytest

PROPERTY_FIELDS = "database/property_fields.json"
NUM_OF_COLOUR = "database/number_of_colour.json"
SPECIAL_FIELDS = "database/special_fields.json"
CHANCE_CARDS = "database/chance_cards.json"


class TestGame:
    property_fields = ffjson.property_fields_from_json(
        PROPERTY_FIELDS)
    num_of_colour = ffjson.number_of_colour_from_json(NUM_OF_COLOUR)
    special_fields = ffjson.special_fields_from_json(SPECIAL_FIELDS)
    board = Board(property_fields, num_of_colour, special_fields)
    player1 = Player()
    player2 = Player()
    game = Game(board, [player1, player2])
    game.prepare_game()

    def test_prepare_pawns_on_start(self):
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
        assert self.game._current_player.current_pawn_position() == 2

    def test_current_field_get_rent(self):
        field = self.game.current_field()
        assert self.game._current_player.current_pawn_position() == 2
        assert type(field) == PropertyField
        assert field.owner() is None
        assert field.current_rent() == 25

    def test_player_can_afford(self):
        price = 2000
        assert self.game.can_afford(price) is False
        price = 1000
        assert self.game.can_afford(price)

    def test_buy_current_property(self):
        field = self.game.current_field()
        assert type(field) == PropertyField
        self.game.buy_current_property()
        assert field.owner() == self.game._current_player
        assert field.field_id() in self.game.\
            _current_player._owned_property_fields

    def test_change_player(self):
        assert self.game._current_player_index == 0
        self.game.change_player()
        assert self.game._current_player_index == 1
        assert self.game._current_player == self.player2
        assert self.game._current_player == self.player2

    def test_pay_rent(self):
        self.game._current_player = self.player1
        self.player1.set_position(6)
        self.game.buy_current_property()
        self.game._current_player = self.player2
        self.player2.set_position(6)
        money_before1 = self.player1.money()
        money_before2 = self.player2.money()
        self.game.pay_rent()
        assert money_before1 < self.player1.money()
        assert money_before2 > self.player2.money()

    def test_change_player_bancrupt(self):
        self.game._current_player == self.player1
        self.player2.is_bancrupt = True
        self.game.change_player()
        assert self.game._current_player == self.player1


class TestHouseBuilding:
    property_fields = ffjson.property_fields_from_json(
        PROPERTY_FIELDS)
    num_of_colour = ffjson.number_of_colour_from_json(NUM_OF_COLOUR)
    special_fields = ffjson.special_fields_from_json(SPECIAL_FIELDS)
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

    def test_owns_all_of_colour(self):
        self.player1._owned_property_fields = self.test_fields_set
        assert self.game.owns_all_of_colour(self.street1)

    def test_houses_build_evenly(self):
        self.player1._owned_property_fields = self.test_fields_set
        self.board.get_field_by_id(self.street_id1).add_house()
        assert self.game.houses_build_evenly(self.street1) is False
        self.board.get_field_by_id(self.street_id2).add_house()
        assert self.game.houses_build_evenly(self.street1) is True

    def test_build_fifth_house(self):
        self.player1._owned_property_fields = self.test_fields_set
        assert self.street1.houses_num() == 1
        for _ in range(0, 3):
            self.street1.add_house()
            self.street2.add_house()
        with pytest.raises(HousesNumError):
            self.game.build_house(self.street1)

    def test_is_enough_houses(self):
        self.street1.remove_house()
        assert self.street1.houses_num() == 3
        assert self.street2.houses_num() == 4
        assert not self.game.is_enough_houses(self.street1)

    def test_hotels_build_evenly(self):
        assert self.game.hotels_build_evenly(self.street2) is False

    def test_can_build_hotel(self):
        self.street1.add_house()
        assert self.street1.houses_num() == 4
        assert self.street2.houses_num() == 4

        self.game.build_hotel(self.street1)
        self.game.build_hotel(self.street2)

    def test_build_second_hotel(self):
        with pytest.raises(HousesNumError):
            self.street1.add_hotel()

    def test_build_house_not_owned_all_of_colour(self):
        street_field_id = 6
        self.player1._owned_property_fields.add(street_field_id)
        f = self.board.get_field_by_id(street_field_id)
        with pytest.raises(HousesNumError):
            self.game.build_house(f)

    def test_build_house_not_enough_money(self):
        self.street1.remove_hotel()
        self.street1.remove_house()
        assert self.street1.houses_num() == 3
        self.game.build_house(self.street1)
        self.player1._money = 10
        with pytest.raises(HousesNumError):
            self.game.build_house(self.street1)

    def test_houses_removed_evenly_hotel(self):
        assert self.street1.houses_num() == 4
        assert self.street2.hotel()
        assert self.game.houses_removed_evenly(self.street2)
        assert not self.game.houses_removed_evenly(self.street1)

    def test_houses_removed_evenly_houses(self):
        self.street2.remove_hotel()
        assert self.street2.houses_num() == 4
        assert self.street1.houses_num() == 4
        assert self.game.houses_removed_evenly(self.street1)
        assert self.game.houses_removed_evenly(self.street2)
        self.street1.remove_house()
        assert self.street1.houses_num() == 3
        assert not self.game.houses_removed_evenly(self.street1)
        assert self.game.houses_removed_evenly(self.street2)

    def test_sell_hotel(self):
        self.street1.add_house()
        self.street2.add_hotel()
        self.game.sell_hotel(self.street2)


class TestGameWinThreePlayes:
    property_fields = ffjson.property_fields_from_json(
        PROPERTY_FIELDS)
    num_of_colour = ffjson.number_of_colour_from_json(NUM_OF_COLOUR)
    special_fields = ffjson.special_fields_from_json(SPECIAL_FIELDS)
    board = Board(property_fields, num_of_colour, special_fields)
    player1 = Player()
    player2 = Player()
    player3 = Player()
    game = Game(board, [player1, player2, player3])
    game.prepare_game()

    def test_is_win_max_rounds(self):
        self.game._total_moves = (GameConstants.MAX_NUM_OF_ROUNDS + 1) * \
            len(self.game._players)
        assert self.game.is_win()

    def test_total_fortune(self):
        self.game._total_moves = 0
        fld5 = self.board.get_field_by_id(5)
        fld7 = self.board.get_field_by_id(7)
        self.player1.set_position(5)
        assert type(fld5) == Street
        self.game.buy_current_property()
        self.player1.set_position(7)
        self.game.buy_current_property()
        self.game.build_house(fld5)
        self.player1._money = 1000
        assert self.game.total_fortune() == 1000 + fld5.house_cost() + \
            fld5.price() / 2 + fld7.price()/2

    def test_make_bancrupt(self):
        self.player1.set_position(6)
        self.game.buy_current_property()
        fld6 = self.board.get_field_by_id(6)
        self.game.mortgage(fld6)
        self.game.make_bancrupt()
        assert self.player1.money() == 0
        assert self.game.total_fortune() == 0
        assert fld6.is_mortgaged() is False
        assert fld6.owner() is None

    def test_is_win_bancrupcy(self):
        assert not self.game.is_win()
        self.game.change_player()
        self.game.make_bancrupt()
        assert self.player2.is_bancrupt
        assert self.game.is_win()

    def test_find_winner_ony_player(self):
        assert self.game.find_winner() == self.player3

    def test_find_winner_by_total_fortune(self):
        self.player2.is_bancrupt = False
        self.player2.add_property(8)
        self.player2.add_property(1)
        self.player2._money = 1500
        self.player2._money = 1500
        assert self.game.find_winner() == self.player2
        self.player3._money = 10000
        assert self.game.find_winner() == self.player3


class TestGameOtherMethods:
    property_fields = ffjson.property_fields_from_json(
        PROPERTY_FIELDS)
    num_of_colour = ffjson.number_of_colour_from_json(NUM_OF_COLOUR)
    special_fields = ffjson.special_fields_from_json(SPECIAL_FIELDS)
    board = Board(property_fields, num_of_colour, special_fields)
    player1 = Player()
    game = Game(board, [player1])
    game.prepare_game()

    def test_add_player(self):
        self.game.add_player('')
        assert len(self.game._players) == 2

    def test_get_round_num(self):
        assert self.game.get_round_num() == 0
        self.game.change_player()
        assert self.game.get_round_num() == 0
        self.game.change_player()
        assert self.game.get_round_num() == 1

    def test_current_player_name(self):
        assert self.game.current_player_name() == ''
        self.player1._name = 'Monika'
        assert self.game.current_player_name() == 'Monika'

    def test_start_field_bonus(self, monkeypatch):

        monkeypatch.setattr(Game, 'current_dice_sum',
                            lambda s: GameConstants.MAX_FIELD_ID + 2)
        self.game.move_pawn_number_of_dots()
        self.game.start_field_bonus()

    def test_start_field_bonus_player_error(self, monkeypatch):
        monkeypatch.setattr(Game, 'current_dice_sum',
                            lambda s: 1)
        self.game.move_pawn_number_of_dots()
        with pytest.raises(StartFieldError):
            self.game.start_field_bonus()


class TestMortgage:
    property_fields = ffjson.property_fields_from_json(
        PROPERTY_FIELDS)
    num_of_colour = ffjson.number_of_colour_from_json(NUM_OF_COLOUR)
    special_fields = ffjson.special_fields_from_json(SPECIAL_FIELDS)
    board = Board(property_fields, num_of_colour, special_fields)
    player1 = Player()
    player2 = Player()
    game = Game(board, [player1, player2])
    game.prepare_game()
    id5 = 5
    id7 = 7
    fld5 = game.get_field_by_id(id5)
    fld7 = game.get_field_by_id(id7)
    player1.set_position(id5)
    game.buy_current_property()

    def test_mortgage(self):
        m = self.player1.money()
        self.game.mortgage(self.fld5)
        assert self.fld5.is_mortgaged()
        assert self.player1.money() - m == self.fld5.mortgage_price()

    def test_lift_mortgage(self):
        self.game.lift_mortgage(self.fld5)

    def test_lift_mortgage_house_exception(self):
        self.player1.set_position(self.id7)
        self.game.buy_current_property()
        self.game.build_house(self.fld5)
        with pytest.raises(MortgageError):
            self.game.mortgage(self.fld5)
