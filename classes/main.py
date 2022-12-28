from board import Board
from game_state import GameState
from player import Player, Players
from field import Field
import object_generator as obj_gen

CHANCE_CARDS = "database/chance_cards.json"
PROPERTY_FIELDS = "database/property_fields.json"
SPECIAL_FIELDS = "database/special_fields.json"


def main():
    property_fields = obj_gen.generate_property_fields(
        PROPERTY_FIELDS)
    special_fields = obj_gen.generate_street_fields(SPECIAL_FIELDS)
    chance_cards = obj_gen.generate_chance_cards(CHANCE_CARDS)
    board = Board(property_fields, special_fields, chance_cards)
    player1 = Player("Marek")
    player2 = Player("Adam")
    players = Players(player1, player2)
    game_state = GameState(board, players)


if __name__ == "__main__":
    main()
