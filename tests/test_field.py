from classes.field import PropertyField, Street
from classes.field import PlayerError
from classes.player import Player
import pytest


class TestField:
    field = PropertyField(0, 'start', 'blue', 50, {
                          "base_price": 100}, {"mortgage": 50})
    other_field = PropertyField(
        20, 'train station', 'green', 50, {"base_price": 100}, {"mortgage": 50})

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

    def test_put_player_on_field(self):
        player = Player()
        self.field.put_player_on(player)
        assert player.player_id() in self.field.get_players_on_ids()

    def test_put_player_on_exception(self):
        player = Player()
        self.field.put_player_on(player)
        with pytest.raises(PlayerError):
            self.field.put_player_on(player)

    def test_take_player_from_field(self):
        player = Player()
        self.other_field.put_player_on(player)
        assert player.player_id() in self.other_field.get_players_on_ids()
        self.other_field.take_player_from(player)
        assert player.player_id() not in self.other_field.get_players_on_ids()

    def test_take_player_from_exception(self):
        player = Player()
        with pytest.raises(PlayerError):
            self.field.take_player_from(player)


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
        "base_price": 100,
        "house_cost": 50,
        "hotel_cost": 50
    }

    def test_add_house(self):
        street = Street(self.field_id, self.name, self.colour,
                        self.rent, self.prices, self.other_rents)
        assert street.houses_num() == 0
        street.add_house()
        assert street.houses_num() == 1
        street.add_house()
        assert street.houses_num() == 2

    def test_add_fifth_house(self):
        street = Street(self.field_id, self.name, self.colour,
                        self.rent, self.prices, self.other_rents)
        street.add_house()
        street.add_house()
        street.add_house()
        street.add_house()
        with pytest.raises(ValueError):
            street.add_house()

    def test_add_hotel(self):
        street = Street(self.field_id, self.name, self.colour,
                        self.rent, self.prices, self.other_rents)
        street.add_house()
        street.add_house()
        street.add_house()
        street.add_house()
        street.add_hotel()
        assert street.hotel() is True

    def test_second_hotel_error(self):
        street = Street(self.field_id, self.name, self.colour,
                        self.rent, self.prices, self.other_rents)
        street.add_house()
        street.add_house()
        street.add_house()
        street.add_house()
        street.add_hotel()
        with pytest.raises(ValueError):
            street.add_hotel()

    def test_too_many_houses(self):
        street = Street(self.field_id, self.name, self.colour,
                        self.rent, self.prices, self.other_rents)
        street.add_house()
        street.add_house()
        with pytest.raises(ValueError):
            street.add_hotel()

    def test_update_rent(self):
        street = Street(self.field_id, self.name, self.colour,
                        self.rent, self.prices, self.other_rents)
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
                        self.rent, self.prices, self.other_rents)
        assert street.house_cost() == self.prices['house_cost']
        assert street.hotel_cost() == self.prices['hotel_cost']
