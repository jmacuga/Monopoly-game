from classes.board import Board
from classes.game import Game
from classes import interface
import classes.fields_from_json as ffjson
CHANCE_CARDS = "database/chance_cards.json"
PROPERTY_FIELDS = "database/property_fields.json"
SPECIAL_FIELDS = "database/special_fields.json"
NUMBER_OF_COLOUR = "database/number_of_colour.json"


def test_bancupt_menu():
    property_fields = ffjson.property_fields_from_json(
        PROPERTY_FIELDS)
    special_fields = ffjson.special_fields_from_json(SPECIAL_FIELDS)
    # chance_cards = ffjson.chance_cards_from_json(CHANCE_CARDS)
    num_of_coulour = ffjson.number_of_colour_from_json(NUMBER_OF_COLOUR)
    board = Board(property_fields, num_of_coulour, special_fields)
    game = Game(board)
    field_1 = board.get_field_by_id(1)
    field_2 = board.get_field_by_id(2)
    game.add_player('Mati')
    game.add_player('Julia')
    game.prepare_game()
    game._current_player.add_property(1)
    field_1.set_owner(game._current_player)
    game.change_player()
    game._current_player.add_property(2)
    field_2.set_owner(game._current_player)
    game._current_player._money = 20
    game._current_player.set_position(1)
    interface.pay_rent(game)
    # interface.play(game)


if __name__ == '__main__':
    test_bancupt_menu()
