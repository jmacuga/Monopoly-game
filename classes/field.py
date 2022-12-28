class Field:
    def __init__(self, field_id, name):
        self._field_id = field_id
        self.name = name

    def field_id(self):
        return self._field_id


class PropertyField(Field):
    def __init__(self, field_id, name, colour, rent):
        super().__init__(field_id, name)
        self._colour = colour
        self._rent = rent
        self._same_colour_field_ids = []


class Street(PropertyField):
    def __init__(self, field_id, name, colour, rent, other_rents, prices):
        super().__init__(field_id, name, colour, rent)
        self._other_rents = other_rents
        self._prices = prices


class Station(PropertyField):
    def __init__(self, field_id, name, colour, rent):
        super().__init__(field_id, name, colour, rent)


class ChanceField(Field):
    def __init__(self):
        super.__init__()


class CommunityChestField(Field):
    def __init__(self):
        super().__init__()


class IncomeTaxField(Field):
    def __init__(self):
        super().__init__()


class JailField(Field):
    def __init__(self):
        super().__init__()


class FreeParkingField(Field):
    def __init__(self):
        super().__init__()
