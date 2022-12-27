from board import Board
from game_state import GameState
from player import Player, Players
from field import Field
from database import Database


CHANCE_CARDS = "/home/jmacuga/pipr_sem3/monopoly/database/chance_cards.json"
PROPERTY_FIELDS = "/home/jmacuga/pipr_sem3/monopoly/database/property_cards.json"
STREET_FIELDS = "/home/jmacuga/pipr_sem3/monopoly/database/street_fields.json"


def main():
    database = Database()
    properties = database.generate_properties(PROPERTY_FIELDS)
    streets = database().generate_streets(STREET_FIELDS)
    chance_cards = database().generate_chance_cards(CHANCE_CARDS)

    board = Board(properties, streets, chance_cards)
    player1 = Player("Marek")
    player2 = Player("Adam")
    players = Players(player1, player2)
    game_state = GameState(board, players)


if __name__ == "__main__":
    main()
