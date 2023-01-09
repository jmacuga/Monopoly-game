from classes.game import Game
from classes.field import PropertyField
from enum import Enum, auto


class State(Enum):
    DICE_ROLL = auto()


class MenuOption(Enum):
    SEE_ALL = 1
    SEE_YOURS = 2
    BUY_HOUSE_HOTEL = 3


def play(game: Game):
    while True:
        show_menu()
        menu_option = players_input_menu()
        MAIN_MENU_OPTIONS[menu_option](game)


def players_input_bool():
    pass


def players_input_menu():
    menu_option = input()
    if menu_option not in MAIN_MENU_OPTIONS:
        print('option unavailable')
        return
    return menu_option


def show_menu():
    text = '''MAIN MENU press number key to pick option:
    1. See all players cards and money
    3. See your cards and money
    2. Buy house/hotel'''
    print(text)


def menu_action(menu_option):
    pass


def show_all_players_status():
    pass


def show_current_players_status():
    pass


def buy_house_hotel():
    pass


def dice_roll(game):
    game.dice_roll()
    game.move_pawn_dice()
    if type(game.current_field()) == PropertyField:
        if game.current_field().owner():
            game.pay_rent()
        else:
            is_transaction = players_input_bool(
                'do you want to buy')
            if is_transaction:
                game.buy_field()
    else:
        game.field_action()
        pass
    game.change_player()


MAIN_MENU_OPTIONS = {MenuOption.SEE_ALL: show_all_players_status,
                     2: show_current_players_status,
                     3: buy_house_hotel,
                     4: dice_roll}
