from __future__ import annotations
from classes.field import Field, PropertyField, SpecialField
from classes.chance_card import ChanceCard
from itertools import cycle


class ColourError(Exception):
    """Raised when requested colour does't exist on the board."""
    pass


class Board:
    """Class representing game board and containing all its field objects.

    Attributes
    ----------
    _property_fields : list of Property
        List of ProprertyField obejcts on the board.
    _special_fields : list of SpecialField
        List of SpecialField objects on the board.
    _chance_cards : itertools.cycle
        Iterator providing chance cards selected on the chance field.
    _all_fields : dict of int to Field
        Dictionary of field indices, containing instances of Field objects values
    _number_of_fields_colour : dict of str to int
        Dictioary assigning colour names to number of fields in that colour group.
    current_chance_card : ChanceCard
        ChanceCard object representing currently selected chance card.
    """

    def __init__(self, property_fields: list[PropertyField],
                 num_of_fields_col: dict[str, int],
                 special_fields: list[SpecialField] = None,
                 chance_cards: list[ChanceCard] = None):
        """Initiates Board object attributes.

        Parameters
        ----------
        property_fields : list of Fields
            List of ProprertyField obejcts on the board.
        number_of_fields_col : dict of str to int
            Dictionary assigning colour names to number of fields in that
                                                                colour group.
        special_fields : list of SpecialField, optional
            List of SpecialField objects on the board.
        chance_cards : list of ChanceCard, optional
            List od ChanceCard objects available on the chance field.
        """
        self._property_fields = property_fields
        if special_fields is None:
            special_fields = []
        self._special_fields = special_fields
        if chance_cards is None:
            chance_cards = []
        self._chance_cards = cycle(chance_cards)
        self._all_fields = self._generate_all_fields_dict()
        self._number_of_fields_colour = num_of_fields_col
        self.current_chance_card = None

    def current_chance_card(self):
        """Get current chance card."""
        return self.current_chance_card

    def _generate_all_fields_dict(self) -> dict[int, Field]:
        """Generate dictionary assigning indices to te Fields of all fields."""
        all_fields = {}
        for field in self._property_fields + self._special_fields:
            all_fields[field.field_id()] = field
        return all_fields

    def get_field_by_id(self, field_id: int) -> Field:
        """Get field by given id."""
        return self._all_fields[field_id]

    def get_fields_owner(self, field_id: int) -> int:
        """Get the player who owns filed with given index."""
        return self._all_fields[field_id].owner()

    def get_max_number_of_same_colour(self, colour: str) -> int:
        """Get the number of fields in given colour.

        Parameters
        ----------
        colour : str
            The searched colour

        Returns
        -------
        int
            Number of fields in the colour goup.
        """
        return self._number_of_fields_colour[colour]

    def get_all_fields_of_colour(self, colour: str) -> list[PropertyField]:
        """Get the list of fields in the given colour.

        Parameters
        ----------
        colour : str
            The searched colour

        Returns
        -------
        list of PropertyField
            The list of PropertyField instances in the colour group.

        Raises
        ------
        ColourError
            If the colour does not exist on the board.
        """
        same_colour = []
        for f in self._property_fields:
            if f.colour() == colour:
                same_colour.append(f)
        if len(same_colour) == 0:
            raise ColourError("Colour doesn't exist")
        return same_colour

    def get_new_chance_card(self):
        """Get next chance card from deck."""
        self.current_chance_card = next(self._chance_cards)
        return self.current_chance_card
