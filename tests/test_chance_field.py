from classes.player import Player
import classes.fields_from_json as ffjson
from classes.board import Board

CHANCE_CARDS = "database/chance_cards.json"
PROPERTY_FIELDS = "database/property_fields.json"
SPECIAL_FIELDS = "database/special_fields.json"
NUMBER_OF_COLOUR = "database/number_of_colour.json"


def test_chance_card():
    chance_cards = ffjson.chance_cards_from_json(CHANCE_CARDS)
    property_fields = ffjson.property_fields_from_json(PROPERTY_FIELDS)
    special_fields = ffjson.special_fields_from_json(SPECIAL_FIELDS)
    num_of_coulour = ffjson.number_of_colour_from_json(NUMBER_OF_COLOUR)
    board = Board(property_fields, num_of_coulour,
                  special_fields, chance_cards)
    card = board.get_new_chance_card()
    assert card.card_id() == 0
    player = Player()
    player._money = 50
    card.use_card(player)
    assert player.money() == 70
    card = board.get_new_chance_card()
    assert card.card_id() == 1
    card.use_card(player)
    assert player.money() == 20
    print(card)
