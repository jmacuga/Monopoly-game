from classes.field import Field
from random import randint
INITIAL_MPP = 1500


class Game:
    def __init__(self, board, players, max_rounds_num=20):
        self._players = players
        self._max_rounds_num = max_rounds_num
        self._board = board
        self._cur_players_array_id = 0
        self._current_player = self._players[self._cur_players_array_id]
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

    def current_field(self) -> Field:
        field_id = self._current_player.current_pawn_position()
        field = self._board.get_field_by_id(field_id)
        return field

    def player_can_afford(self, amount):
        return self._current_player.money() > amount

    def buy_current_property(self):
        field = self.current_field()
        self._current_player.spend_money(field.current_rent())
        self._current_player.buy_property(field.field_id())
        field.set_owner(self._current_player.player_id())

    def change_player(self):
        self._cur_players_array_id = (
            self._cur_players_array_id + 1) % len(self._players)
        self._current_player = self._players[self._cur_players_array_id]

# TODO test
    def owns_all_of_colour(self, field):
        colour = field.colour()
        owned_in_colour_num = 0
        for f in self._current_player.owned_property_fields():
            if self._board.get_field_by_id(f).colour() == colour:
                owned_in_colour_num += 1
        return owned_in_colour_num == \
            self._board.get_max_number_of_same_colour(
                colour)
# TODO test

    def can_build_house(self, field_id):
        field = self._board.get_field_by_id(field_id)
        for f in self._board.get_all_fields_of_colour(field.colour()):
            if field.houses_num() > f.houses_num() and not f.hotel():
                return False
        return False if field.houses_num() == 4 else self.owns_all_of_colour(field) and \
            self._current_player.money() >= field.house_cost()

    def can_build_hotel(self, field_id):
        field = self._board.get_field_by_id(field_id)
        for f in self._board.get_all_fields_of_colour(field.colour()):
            if f.houses_num() < 4:
                return False
        return False if field.hotel() else self.owns_all_of_colour(field) and \
            self._current_player.money() >= field.hotel_cost()

    def make_move(self):
        pass

    def find_winner(self):
        pass

    def buid_hotel(self):
        pass

    def build_house(self):
        pass
