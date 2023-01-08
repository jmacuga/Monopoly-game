from classes.field import Field
from classes.player import Player
from classes.board import Board
from random import randint
INITIAL_MPP = 1500


class Game:
    def __init__(self, board, players, max_rounds_num=20):
        self._players = players
        self._max_rounds_num = max_rounds_num
        self._board = board
        self._current_player = self._players[0]
        self._winner = None
        self._prepare_game()
        self._current_dice_roll = None

    def _prepare_game(self):
        for player in self._players:
            self._board.get_field_by_id(0).put_player_on(player)
            player.set_position(0)
            player.earn_money(INITIAL_MPP)

    def dice_roll(self):
        dice1 = randint(1, 6)
        dice2 = randint(1, 6)
        self._current_dice_roll = (dice1, dice2)

    def current_dice_roll(self):
        return self._current_dice_roll

    def current_dice_sum(self):
        return sum(self._current_dice_roll)

    def move_pawn_number_of_dots(self):
        self._current_player.set_dice_roll_sum(self.current_dice_sum())
        self._current_player.move_pawn()
        self.current_field().put_player_on(self._current_player)

    def make_move(self):
        pass

    def current_field(self) -> Field:
        field_id = self._current_player.current_pawn_position()
        field = self._board.get_field_by_id(field_id)
        return field

    def change_player(self):
        pass

    def player_can_afford(self, amount):
        return self._current_player.money() > amount

    def buy_property(self, property_id):
        field = self.board.get_field_by_id(property_id)
        self._current_player.spend_money(field.current_rent())
        self._current_player.buy_property(property_id)
