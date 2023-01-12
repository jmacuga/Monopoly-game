from classes.field import Field, PlayerError, Street
from random import randint
from classes.game_constants import GameConstants
from classes.player import Player
from typing import Tuple
from tabulate import tabulate


class Game:
    def __init__(self, board, players=None):
        self._players = players
        if players is None:
            self._players = []
        self._board = board
        self._cur_player_id_in_array = 0
        self._current_player = None
        self._current_dice_roll = None
        self._total_moves = 0

    def player_is_owner(self) -> bool:
        return self.current_field().owner() == self._current_player

    def prepare_game(self) -> None:
        self._current_player = self._players[self._cur_player_id_in_array]
        for player in self._players:
            self._board.get_field_by_id(0).put_player_on(player)
            player.set_position(0)
            player.earn_money(int(GameConstants.INITIAL_MONEY_PP))

    def add_player(self, player_name: str) -> None:
        self._players.append(Player(player_name))

    def get_round_num(self) -> int:
        return self._total_moves // len(self._players)

    def current_player_name(self) -> str:
        return self._current_player.name()

    def dice_roll(self) -> None:
        dice1 = randint(1, 6)
        dice2 = randint(1, 6)
        self._current_dice_roll = (dice1, dice2)

    def current_dice_roll(self) -> Tuple[int, int]:
        return self._current_dice_roll

    def current_dice_sum(self) -> int:
        return sum(self._current_dice_roll)

    def move_pawn_number_of_dots(self) -> None:
        self.current_field().take_player_from(self._current_player)
        self._current_player.set_dice_roll_sum(self.current_dice_sum())
        self._current_player.move_pawn()
        self.current_field().put_player_on(self._current_player)

    def current_field(self) -> Field:
        field_id = self._current_player.current_pawn_position()
        field = self._board.get_field_by_id(field_id)
        return field

    def can_afford(self, amount: int) -> bool:
        return self._current_player.money() > amount

    def buy_current_property(self) -> None:
        field = self.current_field()
        self._current_player.spend_money(field.price())
        self._current_player.add_property(field.field_id())
        field.set_owner(self._current_player)

    def change_player(self) -> None:
        self._total_moves += 1
        self._cur_player_id_in_array = (
            self._cur_player_id_in_array + 1) % len(self._players)
        self._current_player = self._players[self._cur_player_id_in_array]

    def owns_all_of_colour(self, field_id: int) -> bool:
        field = self._board.get_field_by_id(field_id)
        colour = field.colour()
        owned_in_colour_num = 0
        for f in self._current_player.owned_property_fields():
            if self._board.get_field_by_id(f).colour() == colour:
                owned_in_colour_num += 1
        return owned_in_colour_num == \
            self._board.get_max_number_of_same_colour(
                colour)

    def is_street_owner_by_id(self, field_id: int) -> bool:
        if type(self._board.get_field_by_id(field_id)) != Street:
            return False
        return field_id in self._current_player.owned_property_fields()

    def is_street_by_id(self, field_id: int) -> bool:
        return type(self._board.get_field_by_id(field_id)) == Street

    def houses_build_evenly(self, field_id: Field) -> bool:
        field = self._board.get_field_by_id(field_id)
        for f in self._board.get_all_fields_of_colour(field.colour()):
            if field.houses_num() > f.houses_num() and not f.hotel():
                return False
        return True

    def hotels_build_evenly(self, field_id: int) -> bool:
        field = self._board.get_field_by_id(field_id)
        for f in self._board.get_all_fields_of_colour(field.colour()):
            if f.houses_num() < 4:
                return False
        return True

    def can_build_hotel(self, field_id):
        return self._board.get_field_by_id(field_id).houses_num() == 4

    def can_afford_house(self, field_id):
        return self.can_afford(self._board.get_field_by_id(field_id).house_cost())

    def can_afford_hotel(self, field_id):
        return self.can_afford(self._board.get_field_by_id(field_id).hotel_cost())

    def is_hotel(self, field_id):
        return self._board.get_field_by_id(field_id).hotel()

    # def can_build_house(self, field_id: int) -> bool:
    #     # if field_id not in self._current_player.owned_property_fields():
    #     #     return False
    #     field = self._board.get_field_by_id(field_id)
    #     for f in self._board.get_all_fields_of_colour(field.colour()):
    #         if field.houses_num() > f.houses_num() and not f.hotel():
    #             return False
    #     return False if field.houses_num() == 4 else \
    #         self.owns_all_of_colour(
    #             field) and self.player_can_afford(field.house_cost())

    # def can_build_hotel(self, field_id: int) -> bool:
    #     # if field_id not in self._current_player.owned_property_fields():
    #     #     return False
    #     field = self._board.get_field_by_id(field_id)
    #     for f in self._board.get_all_fields_of_colour(field.colour()):
    #         if f.houses_num() < 4:
    #             return False
    #     return False if field.hotel() else self.owns_all_of_colour(field) and \
    #         self.player_can_afford(field.hotel_cost())

    def build_house(self, field_id: int) -> None:
        field = self._board.get_field_by_id(field_id)
        self._current_player.spend_money(field.house_cost())
        field.add_house()

    def build_hotel(self, field_id: int) -> None:
        field = self._board.get_field_by_id(field_id)
        self._current_player.spend_money(field.hotel_cost())
        field.add_hotel()

    def pay_rent(self) -> None:
        if self.current_field() in self._current_player._owned_property_fields:
            raise ValueError('Player cannot pay rent to himself')
        rent = self.current_field().current_rent()
        self._current_player.spend_money(rent)
        # NOtAffordableError -> mortgage, selling properties
        owner = self.current_field().owner()
        owner.earn_money(rent)

    def is_win(self) -> bool:
        if self.get_round_num() > GameConstants.MAX_NUM_OF_ROUNDS:
            return True
        for player in self._players:
            if player.is_bancrupt():
                return True
        return False

    def find_winner(self) -> Player:
        winner = None
        max_fortune = 0
        for player in self._players:
            if self.total_fortune(player) > max_fortune:
                winner = player
        return winner

    def players_description(self) -> str:
        out_str = ''
        for player in self._players:
            out_str += '\n' + self.show_player_status(player=player)
        return out_str

    def show_player_status(self, streets_only: bool = False, player: Player = None, ) -> str:
        if not player:
            player = self._current_player
        out_str = str(player)
        for field_id in player.owned_property_fields():
            field = self._board.get_field_by_id(field_id)
            if streets_only and type(field) != Street:
                continue
            if player != self._current_player:
                out_str += '\n' + tabulate(field.description_table(),
                                           tablefmt='rounded_grid')
            else:
                out_str += '\n' + tabulate(field.full_description_table(),
                                           tablefmt='rounded_grid')
        return out_str

    def get_player_by_id(self, player_id: int) -> str:
        for player in self._players:
            if player.player_id() == player_id:
                return player

    def get_current_field_owner_name(self) -> str:
        return self.current_field().owner().name()

    def start_field_bonus(self) -> None:
        if self._current_player.passed_start_field is False:
            raise PlayerError("Player didn't pass start field")
        self._current_player.earn_money(int(GameConstants.START_FIELD_BONUS))

    def total_fortune(self, player) -> int:
        fortune = player._money
        for field_id in player._owned_property_fields:
            fld = self._board.get_field_by_id(field_id)
            fortune += fld.total_value()
        return fortune
