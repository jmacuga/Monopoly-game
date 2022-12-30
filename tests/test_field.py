from classes.field import PropertyField, Street, HousesNumError, HotelError
from classes.player import Player
import pytest


class TestField:
    field = PropertyField(0, 'start', 'blue', 50)

    def test_set_rent(self):
        assert self.field.base_rent() == 50
        assert self.field.current_rent() == 50
        self.field.set_current_rent(100)
        assert self.field.current_rent() == 100

    def test_set_rent_exception(self):
        with pytest.raises(ValueError):
            self.field.set_current_rent(-10)

    def test_set_owner(self):
        player = Player()
        assert self.field.owner() is None
        self.field.set_owner(player)
        assert self.field.owner() == player


class TestStreetField:
    field_id = 1
    name = 'west avenue'
    colour = 'green'
    rent = 100
    other_rents = {
        "w_one_house": 30,
        "w_two_houses": 90,
        "w_three_houses": 180,
        "w_four_houses": 320,
        "w_hotel": 550,
        "mortgage": 30
    }
    prices = {
        "house_cost": 50,
        "hotel_cost": 50
    }

    def test_add_house(self):
        street = Street(self.field_id, self.name, self.colour,
                        self.rent, self.other_rents, self.prices)
        assert street.houses_num() == 0
        street.add_house()
        assert street.houses_num() == 1
        street.add_house()
        assert street.houses_num() == 2

    def test_add_fifth_house(self):
        street = Street(self.field_id, self.name, self.colour,
                        self.rent, self.other_rents, self.prices)
        street.add_house()
        street.add_house()
        street.add_house()
        street.add_house()
        with pytest.raises(HousesNumError):
            street.add_house()

    def test_add_hotel(self):
        street = Street(self.field_id, self.name, self.colour,
                        self.rent, self.other_rents, self.prices)
        street.add_house()
        street.add_house()
        street.add_house()
        street.add_house()
        street.add_hotel()
        assert street.hotels_num() == 1

    def test_second_hotel_error(self):
        street = Street(self.field_id, self.name, self.colour,
                        self.rent, self.other_rents, self.prices)
        street.add_house()
        street.add_house()
        street.add_house()
        street.add_house()
        street.add_hotel()
        with pytest.raises(HotelError):
            street.add_hotel()

    def test_too_many_houses(self):
        street = Street(self.field_id, self.name, self.colour,
                        self.rent, self.other_rents, self.prices)
        street.add_house()
        street.add_house()
        with pytest.raises(HotelError):
            street.add_hotel()

    def test_update_rent(self):
        street = Street(self.field_id, self.name, self.colour,
                        self.rent, self.other_rents, self.prices)
        assert street.current_rent() == self.rent
        street.add_house()
        assert street.current_rent() == self.other_rents['w_one_house']
        street.add_house()
        assert street.current_rent() == self.other_rents['w_two_houses']
        street.add_house()
        assert street.current_rent() == self.other_rents['w_three_houses']
        street.add_house()
        assert street.current_rent() == self.other_rents['w_four_houses']
        street.add_hotel()
        assert street.current_rent() == self.other_rents['w_hotel']

    def test_house_cost_hotel_cost(self):
        street = Street(self.field_id, self.name, self.colour,
                        self.rent, self.other_rents, self.prices)
        assert street.house_cost() == self.prices['house_cost']
        assert street.hotel_cost() == self.prices['hotel_cost']
