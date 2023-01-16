
import sys
import argparse
import pickle
from classes.board import Board
from classes.game import Game
from classes import interface
import classes.fields_from_json as ffjson
CHANCE_CARDS = "database/chance_cards.json"
PROPERTY_FIELDS = "database/property_fields.json"
SPECIAL_FIELDS = "database/special_fields.json"
NUMBER_OF_COLOUR = "database/number_of_colour.json"


def main(arguments):
    property_fields = ffjson.property_fields_from_json(
        PROPERTY_FIELDS)
    special_fields = ffjson.special_fields_from_json(SPECIAL_FIELDS)
    # chance_cards = ffjson.chance_cards_from_json(CHANCE_CARDS)
    num_of_coulour = ffjson.number_of_colour_from_json(NUMBER_OF_COLOUR)
    parser = argparse.ArgumentParser()
    parser.add_argument('--resume', help="name of file with target game")
    args = parser.parse_args()
    if args.resume is not None:
        with open(args.resume, 'rb') as pkl:
            game = pickle.load(pkl)
        interface.play(game, resumed=True)
    else:
        board = Board(property_fields, num_of_coulour, special_fields)
        game = Game(board)
        interface.play(game)


if __name__ == "__main__":
    main(sys.argv)
