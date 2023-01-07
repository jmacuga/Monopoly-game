import classes.fields_from_json as ffjson
from classes.field import Street, SpecialField


class TestFieldsFromJson:
    PROPERTY_FIELDS = "database/property_fields.json"
    NUM_OF_COLOUR = "database/number_of_colour.json"
    SPECIAL_FIELDS = "database/special_fields.json"
    CHANCE_CARDS = "database/chance_cards.json"
    property_f_len = 6
    num_of_grey = 1
    num_of_black = 1
    num_of_blue = 2
    num_of_yellow = 2

    def test_porperty_f_from_json(self):
        property_fields = ffjson.property_fields_from_json(
            self.PROPERTY_FIELDS)
        assert type(property_fields[4]) == Street
        assert property_fields[0].field_id() == 1
        assert property_fields[3].current_rent() == 2
        assert len(property_fields) == self.property_f_len

    def test_number_of_colour_from_json(self):
        num_of_colour = ffjson.number_of_colour_from_json(self.NUM_OF_COLOUR)
        assert num_of_colour['grey'] == self.num_of_grey
        assert num_of_colour['blue'] == self.num_of_blue
        assert num_of_colour['black'] == self.num_of_black
        assert num_of_colour['yellow'] == self.num_of_yellow

    def test_special_fields_from_json(self):
        special_fields = ffjson.special_fields_from_json(self.SPECIAL_FIELDS)
        assert type(special_fields[0]) == SpecialField
        assert special_fields[0].name() == 'start'
        assert special_fields[3].field_id() == 9
