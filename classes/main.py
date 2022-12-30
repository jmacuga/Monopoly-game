from .board import Board
from .game_state import GameState
from .player import Player
from . import fields_from_json as ffjson

CHANCE_CARDS = "database/chance_cards.json"
PROPERTY_FIELDS = "database/property_fields.json"
SPECIAL_FIELDS = "database/special_fields.json"
NUMBER_OF_COLOUR = "database/number_of_colour.json"


def main():
    property_fields = ffjson.property_fields_from_json(
        PROPERTY_FIELDS)
    special_fields = ffjson.special_fields_from_json(SPECIAL_FIELDS)
    chance_cards = ffjson.chance_cards_from_json(CHANCE_CARDS)
    board = Board(property_fields, special_fields, chance_cards)
    player1 = Player("Marek")
    player2 = Player("Adam")
    game_state = GameState(board, [player1, player2])
    game_state


if __name__ == "__main__":
    main()
