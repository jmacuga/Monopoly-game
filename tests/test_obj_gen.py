from classes.fields_from_json import property_fields_from_json

CHANCE_CARDS = "database/chance_cards.json"
PROPERTY_FIELDS = "database/property_fields.json"
SPECIAL_FIELDS = "database/special_fields.json"


def test_object_generating():
    property_fields = property_fields_from_json(
        PROPERTY_FIELDS)
    assert property_fields[0].field_id() == 4


if __name__ == '__main__':
    pass
