from classes.field import Field, Street
from classes.field import HousesNumError, MortgageError
from random import randint
from classes.game_constants import GameConstants
from classes.player import Player
from tabulate import tabulate


class StartFieldError(Exception):
    """Raised when player didn't pass start field, but bonus was given."""
    pass


class Game:
    """Represents game state.

    Attributes
    ----------
    _players  : list of Player
        List of players.
    _board : Board
        Board object used in game.
    _current_player_index : int
        Index of current player in players array.
    _current_dice_roll : tuple
        Current dice roll result.
    _total_moves : int
        Total number of all moves in game.
    _win : bool
        Is the game over.
    """

    def __init__(self, board, players=None):
        """Initiates object atributes.

        Parameters
        ----------
        board : Board
            Board object used in game.
        players : list of Player, optional
            List of players.
        """
        self._players = players
        if players is None:
            self._players = []
        self._board = board
        self._current_player_index = 0
        self._current_player = None
        self._current_dice_roll = None
        self._total_moves = 0
        self._win = False

    def win(self):
        """Get _win."""
        return self._win

    def player_is_owner(self, field_id: int = None) -> bool:
        """Checks if current player is owner of field with given field id.

        Parameters
        ----------
        field_id : int, optional
            Index of specified field (default is the field player
                                                is currently on).

        Returns
        -------
        bool
        """
        if field_id is None:
            return self.current_field().owner() == self._current_player
        else:
            return field_id in self._current_player.owned_property_fields()

    def prepare_game(self) -> None:
        """Prepares game to first move.

        Must be called before starting game. Puts players
        on start field, gives initial money to every player,
        sets current player to first in _players list.
        """
        self._current_player = self._players[self._current_player_index]
        for player in self._players:
            player.set_position(0)
            player.earn_money(int(GameConstants.INITIAL_MONEY_PP))

    def add_player(self, player_name: str) -> None:
        """Adds new player to game.

        Parameters
        ----------
        player_name : str
            Name of the new player.
        """
        self._players.append(Player(player_name))

    def get_round_num(self) -> int:
        """Gets number of current game round."""
        return self._total_moves // len(self._players)

    def current_player_name(self) -> str:
        """Gets name of current player."""
        return self._current_player.name()

    def dice_roll(self) -> None:
        """Generates result of of two dice roll and sets current dice roll."""
        dice1 = randint(1, 6)
        dice2 = randint(1, 6)
        self._current_dice_roll = (dice1, dice2)

    def current_dice_roll(self) -> tuple[int, int]:
        """Gets current dice roll"""
        return self._current_dice_roll

    def current_dice_sum(self) -> int:
        """Gets sum of current dice roll"""
        return sum(self._current_dice_roll)

    def move_pawn_number_of_dots(self) -> None:
        """Moves current player pawn by number of fields indicated by dice."""
        self._current_player.set_dice_roll_sum(self.current_dice_sum())
        self._current_player.move_pawn()

    def current_field(self) -> Field:
        """Gets field that current player is currently on."""
        field_id = self._current_player.current_pawn_position()
        field = self._board.get_field_by_id(field_id)
        return field

    def can_afford(self, amount: int) -> bool:
        """Checks if current player can afford given amount of money.

        Parameters
        ----------
        amount : int
            Amount of money to check if player has.

        Returns
        -------
        bool
        """
        return self._current_player.money() > amount

    def buy_current_property(self) -> None:
        """Make current player buy field that he is currently on."""
        field = self.current_field()
        self._current_player.spend_money(field.price())
        self._current_player.add_property(field.field_id())
        field.set_owner(self._current_player)

    def change_player(self) -> None:
        """Set current player to the next plkayer in players array.

        When players array is exhausted, iteration starts from the beginning.
        """
        self._current_player_index = (
            self._current_player_index + 1) % len(self._players)
        self._current_player = self._players[self._current_player_index]
        if self._current_player.is_bancrupt:
            self.change_player()
        else:
            self._total_moves += 1

    def get_field_by_id(self, field_id: int) -> Field:
        """Get field object with given field index.

        Parameters
        ----------
        field_id : int
            Index of searched field.

        Returns
        -------
        Field
        """
        return self._board.get_field_by_id(field_id)

    def owns_all_of_colour(self, field: Field) -> bool:
        """Checks if player owns all fields in the colour of given field.

        Parameters
        ----------
        field : Field
            field colour of which is searched

        Returns
        -------
        bool
        """
        colour = field.colour()
        owned_in_colour_num = 0
        for f in self._current_player.owned_property_fields():
            if self._board.get_field_by_id(f).colour() == colour:
                owned_in_colour_num += 1
        return owned_in_colour_num == \
            self._board.get_max_number_of_same_colour(
                colour)

    def houses_build_evenly(self, field: Field) -> bool:
        """Checks if houses are build evenly if you put house on given field.

        Checks if you can put house on given field, by checking condition,
        that there must not be more than one house difference between
        each field in the same colour group.

        Parameters
        ----------
        field : Field
            Field obejct that is being checked.

        Returns
        -------
        bool
        """
        for f in self._board.get_all_fields_of_colour(field.colour()):
            if field.houses_num() > f.houses_num() and not f.hotel():
                return False
        return True

    def hotels_build_evenly(self, field: Field) -> bool:
        """Checks if hotels are build evenly if you put hotel on given field.

        Checks if you can put hotel on the given field, by checking
        condition, that all fields in the same colour group
        must have four houses to build hotel on any of them.

        Parameters
        ----------
        field : Field
            Field object that is being checked.

        Returns
        -------
        bool
        """
        for f in self._board.get_all_fields_of_colour(field.colour()):
            if f.houses_num() < 4 and not f.hotel():
                return False
        return True

    def is_enough_houses(self, field: Field) -> bool:
        """Checks if given field has 4 houses.

        Parametrs
        ---------
        field : Field
            Field object that is being checked.

        Returns
        -------
        bool
        """
        return field.houses_num() == 4

    def build_house(self, field: Field) -> None:
        """Make current player build house on given field.

        Check if the current player owns the field, if houses
        on the field are build evenly, if there is not a hotel
        on the field, if player can afford the house and
        if the field is not mortgaged. If yes, make current player
        buy the house.

        Parameters
        ----------
        field : Field
            Field that house is being build on.

        Raises
        ------
        HousesNumError
            If one of the conditions to build a house is not met.
        """
        if self.owns_all_of_colour(field) \
                and self.player_is_owner(field.field_id()) \
                and self.houses_build_evenly(field) \
                and not field.hotel() \
                and self.can_afford(field.house_cost())\
                and not field.is_mortgaged():
            self._current_player.spend_money(field.house_cost())
            field.add_house()
        else:
            raise HousesNumError(
                'Not all conditions to build a house were met')

    def build_hotel(self, field: Field) -> None:
        """Make current player build a hotel on given field.

        Check if the current player owns the field, if hotels
        on the field are build evenly, if there is not a hotel
        on the field, if player can afford the hotel and
        if the field is not mortgaged. If yes, make current player
        buy the hotel.

        Parameters
        ----------
        field : Field
            Field that hotel is being build on.

        Raises
        ------
        HousesNumError
            If one of the conditions to build a house is not met.
        """
        if self.owns_all_of_colour(field) \
                and self.player_is_owner(field.field_id()) \
                and self.hotels_build_evenly(field) \
                and not field.hotel() \
                and self.can_afford(field.hotel_cost())\
                and not field.is_mortgaged()\
                and self.is_enough_houses(field):
            self._current_player.spend_money(field.hotel_cost())
            field.add_hotel()
        else:
            raise HousesNumError(
                'Not all conditions to build a hotel were met')

    def houses_removed_evenly(self, field: Field) -> bool:
        """Checks if hotels would be removed evenly.

        Checks if you can remove house of the given field, by checking
        condition, that there must not be more than one house difference
        between each field in the same colour group and there must
        not be a hotel.

        Parameters
        ----------
        field : Field
            Field object that is being checked.
        """
        if field.hotel():
            return True
        for f in self._board.get_all_fields_of_colour(field.colour()):
            if f.houses_num() > field.houses_num() or f.hotel():
                return False
        return True

    def is_house_to_sell(self, field: Field) -> bool:
        """Checks if there is a house you can sell on given field."""
        return False if type(field) is not Street else field.houses_num() > 0

    def sell_hotel(self, field: Field) -> None:
        """Makes current player sell hotel from given field.

        Checks the conditions erequired to sell a hotel from given field
        by current player, makes current player sell hotel from this field.

        Parameters
        ----------
        field : Field
            field from which hotel is sold

        Raises
        ------
        HousesNumError
            if the conditions to sell the hotel had not been met
        """
        if field.hotel() and not field.is_mortgaged() \
                and self.player_is_owner(field.field_id())\
                and type(field) is Street:
            self._current_player.earn_money(field.hotel_cost())
            field.remove_hotel()
        else:
            raise HousesNumError(
                "No hotel on this field or field is mortgaged")

    def sell_house(self, field: Field):
        """Makes current player sell house from given field.

        Checks the conditions erequired to sell a house from given field
        by current player, makes current player sell house from this field.

        Parameters
        ----------
        field : Field
            field from which house is sold

        Raises
        ------
        HousesNumError
            if the conditions to sell the house had not been met
        """
        if not field.hotel() and self.houses_removed_evenly(field)\
                and not field.is_mortgaged() \
                and self.player_is_owner(field.field_id()):
            self._current_player.earn_money(field.house_cost())
            field.remove_house()
        else:
            raise HousesNumError("You cannot remove house from this field")

    def mortgage(self, field: Field) -> None:
        """Make current player mortgaged current field.

        Check if the field hasn't got any houses on and make current
        player mortgage given field.

        Parameters
        ----------
        field : Field
            field which is being mortgaged

        Raises
        ------
        MortgageError
            if the conditions to mortgage field had not been met
        """
        if self.player_is_owner(field.field_id()) \
                and not self.is_house_to_sell(field):
            field.do_mortgage()
            self._current_player.earn_money(field.mortgage_price())
        else:
            raise MortgageError('You cannot mortgage this field')

    def lift_mortgage(self, field: Field) -> None:
        """Make current player lift mortgage from current field.

        Check if current player can afford to lift mortgage and
        lift mortgage from field.

        Parameters
        ----------
        field : Field
            mortgaged field

        Raises
        ------
        MortgageError
            If the conditions to lift mortgage from field had not been met.

        """
        amount = int(round(field.mortgage_price() * 1.1))
        if self.player_is_owner(field.field_id()) and self.can_afford(amount):
            field.lift_mortgage()
            self._current_player.spend_money(amount)
        else:
            raise MortgageError('You cannot lift mortgage from this field')

    def pay_rent(self) -> None:
        """Make current player pay rent for the current field he is on.

        Raises
        ------
        ValueError
            If the current field is owned by current player.
        """
        if self.current_field() in self._current_player._owned_property_fields:
            raise ValueError('Player cannot pay rent to himself')
        rent = self.current_field().current_rent()
        self._current_player.spend_money(rent)
        owner = self.current_field().owner()
        owner.earn_money(rent)

    def is_win(self) -> bool:
        """Check if the game is over.

        Check if the number of rounds has reached the maximum or there is only
        one non bancrupt player left.

        Returns
        -------
        bool
        """
        if self.get_round_num() > GameConstants.MAX_NUM_OF_ROUNDS:
            self._win = True
        else:
            count = sum([not p.is_bancrupt for p in self._players])
            self._win = False if count > 1 else True
        return self._win

    def find_winner(self) -> Player:
        """Find the player with hthe biggest total fortune.

        Returns
        -------
        Player
            found winner of the game
        """
        winner = None
        max_fortune = 0
        for player in self._players:
            if self.total_fortune(player) > max_fortune:
                winner = player
                max_fortune = self.total_fortune(player)
        return winner

    def players_description(self) -> str:
        """Description of every non bancrupt player in the game."""
        out_str = ''
        for player in self._players:
            if not player.is_bancrupt:
                out_str += '\n' + self.show_player_status(player=player)
        return out_str

    def show_player_status(self,
                           streets_only: bool = False,
                           player: Player = None, ) -> str:
        """Description of the player and owned fields.

        Gets description of the player and each of owned fields in form
        of tables.

        Parameters
        ----------
        streets_only : bool, default = False
            indicates if fields of type other than street may be included in
                                                             the description.
        player: Player, optional
            player whose description is returned (deafult is the current
                                                                    player)

        Returns
        -------
        str
            Description of the player.
        """
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

    def get_current_field_owner_name(self) -> str:
        """Gets the name of the owner of current field"""
        return self.current_field().owner().name()

    def start_field_bonus(self) -> None:
        """Gives current player money bonus for passing the start field.

        Raises
        ------
        StartFieldError
            If the player didn't pass the start field.
        """
        if self._current_player.passed_start_field is False:
            raise StartFieldError("Player didn't pass start field")
        self._current_player.earn_money(int(GameConstants.START_FIELD_BONUS))

    def total_fortune(self, player: Player = None) -> int:
        """Gets the sum of money and properties values of given player."""
        if player is None:
            player = self._current_player
        fortune = player._money
        for field_id in player._owned_property_fields:
            fld = self._board.get_field_by_id(field_id)
            fortune += fld.total_value()
        return fortune

    def end_game(self):
        """Ends game"""
        self._win = True

    def chance_field_action(self) -> str:
        """Get new chance card and use it on the current player.

        Returns
        -------
        str
            Description of the chance card picked from deck."""
        card = self._board.get_new_chance_card()
        card.use_card(self._current_player)
        return str(self._board.current_chance_card)

    def get_new_chance_card(self) -> None:
        """Get new chance card from the board."""
        return self._board.get_new_chance_card()

    def make_bancrupt(self) -> None:
        """Make current player get rid of all of his money and properties."""
        for field_id in self._current_player._owned_property_fields:
            fld = self._board.get_field_by_id(field_id)
            fld.return_to_bank()
        self._current_player._owned_property_fields = set()
        self._current_player._money = 0
        self._current_player.is_bancrupt = True
