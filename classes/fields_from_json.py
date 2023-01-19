import json
from classes.field import PropertyField, Street, SpecialField
from classes.chance_card import ChanceCard


class DoubleFieldIdError:
    """Raised when two fields with the same field id are loaded"""
    pass


def load_from_file(file_name: str) -> list[dict]:
    """Open json file and return json object.

    Parameters
    ----------
    file_name: str
        target file name

    Returns
    -------
    json object
        list of dictionaries containing fields data.
    """
    with open(file_name, 'r') as fp:
        return json.load(fp)


def property_fields_from_json(filename: str) -> list[PropertyField]:
    """Load and parse property fields from json file.

    Parameters
    ---------
    fielname : str
        target file name

    Returns
    -------
    list of PropertyField type obejcts
    """
    fields_collection = load_from_file(filename)
    fields = []
    for field_elem in fields_collection:
        field_id = field_elem["field_id"]
        if field_id in [field.field_id() for field in fields]:
            raise DoubleFieldIdError

        field_type = field_elem['type']
        colour = field_elem['colour']
        field_name = field_elem['name']
        rent = field_elem['rent']
        prices = field_elem['prices']
        other_rents = field_elem["other_rents"]

        if field_type == "street":
            field_item = Street(field_id, field_name, colour,
                                rent, prices, other_rents)
        else:
            field_item = PropertyField(
                field_id, field_name, colour, rent, prices, other_rents)
        fields.append(field_item)
    return fields


def number_of_colour_from_json(filename: str) -> dict[str, int]:
    """Load json file with the dicitionary with numbers of colour fields.

    Parameters
    ---------
    filename : str
        name of json file

    Returns
    -------
    dict of str to int
        dictionary assigning colour names to the number of fields
    """
    number_of_colour = load_from_file(filename)
    return number_of_colour[0]


def special_fields_from_json(filename: str) -> list[SpecialField]:
    """Load and parse special fields from json file.

    Parameters
    ---------
    fielname : str
        target file name

    Returns
    -------
    list of SpecialField type obejcts
    """
    fields_collection = load_from_file(filename)
    fields = []
    for field_elem in fields_collection:
        field_id = field_elem['field_id']
        if field_id in [field.field_id() for field in fields]:
            raise DoubleFieldIdError
        field_name = field_elem['name']
        field = SpecialField(field_id, field_name)
        fields.append(field)
    return fields


def chance_cards_from_json(filename: str) -> list[ChanceCard]:
    """Load and parse chance cards from json file.

    Parameters
    ---------
    fielname : str
        target file name

    Returns
    -------
    list of ChanceCard type obejcts
    """
    cards_collection = load_from_file(filename)
    cards = []
    for card in cards_collection:
        card_id = card['card_id']
        if card_id in [card.card_id() for card in cards]:
            raise DoubleFieldIdError
        description = card['description']
        action = card['action']
        money = card['money']
        field = ChanceCard(card_id, description, action, money)
        cards.append(field)
    return cards
