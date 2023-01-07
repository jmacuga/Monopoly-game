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
        self.prepare_game()
        self._current_dice_roll = (0, 0)

    def prepare_game(self):
        for player in self._players:
            self._board.get_field_by_id(0).put_player_on(player)
            player.earn_money(INITIAL_MPP)

    def dice_roll(self):
        dice1 = randint(1, 6)
        dice2 = randint(1, 6)
        self.current_dice_roll = (dice1, dice2)

    def current_dice_roll(self):
        return self._current_dice_roll

    def current_dice_sum(self):
        return sum(self._current_dice_roll)

    def move_pawn_dice(self):
        self._current_player.current_dice_roll_sum = self.current_dice_sum()
        self._current_player.move_pawn()

    def make_move(self):
        pass

    def current_field(self) -> Field:
        pass

    def change_player(self):
        pass
