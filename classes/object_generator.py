import json
from .field import PropertyField, Street


class DoubleFieldIdError:
    pass


def load_from_file(file_name):
    with open(file_name, 'r') as fp:
        return json.load(fp)


def generate_property_fields(filename):
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
        if field_type == "street":
            other_rents = field_elem["other_rents"]
            prices = field_elem['prices']
            field_item = Street(field_id, field_name, colour,
                                rent, other_rents, prices)
        else:
            field_item = PropertyField(field_id, field_name, colour, rent)
        fields.append(field_item)
    return fields


def generate_number_of_colour(filename):
    number_of_colour = load_from_file(filename)
    return number_of_colour


def generate_special_fields(filename):
    pass


def generate_chance_cards(filename):
    pass
