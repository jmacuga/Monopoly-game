from classes import object_generator

CHANCE_CARDS = "database/chance_cards.json"
PROPERTY_FIELDS = "database/property_fields.json"
SPECIAL_FIELDS = "database/special_fields.json"


def test_object_generating():
    property_fields = object_generator.generate_property_fields(
        PROPERTY_FIELDS)
    assert property_fields[0].field_id() == 4
    pass


if __name__ == '__main__':
    pass
