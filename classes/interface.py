from classes.game import Game
from classes.field import PropertyField
from enum import IntEnum
from classes.game_constants import GameConstants
import os
from tabulate import tabulate


class MenuOption(IntEnum):
    SEE_ALL = 1
    SEE_YOURS = 2
    BUY_HOUSE_HOTEL = 3
    SELL_HOUSE_HOTEL = 4
    MORTGAGE = 5
    LIFT_MORTGAGE = 6
    THROW_DICE = 7


class BancruptOption(IntEnum):
    SEE_YOURS = 1
    SELL_HOUSE_HOTEL = 2
    MORTGAGE = 3


def clear():
    return os.system('clear')


def menu_values():
    return [mem.value for mem in MenuOption]


def print_welcome_text():
    print('''
$$\      $$\                                                   $$\\
$$$\    $$$ |                                                  $$ |
$$$$\  $$$$ | $$$$$$\  $$$$$$$\   $$$$$$\   $$$$$$\   $$$$$$\  $$ |$$\   $$\\
$$\$$\$$ $$ |$$  __$$\ $$  __$$\ $$  __$$\ $$  __$$\ $$  __$$\ $$ |$$ |  $$ |
$$ \$$$  $$ |$$ /  $$ |$$ |  $$ |$$ /  $$ |$$ /  $$ |$$ /  $$ |$$ |$$ |  $$ |
$$ |\$  /$$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |$$ |  $$ |
$$ | \_/ $$ |\$$$$$$  |$$ |  $$ |\$$$$$$  |$$$$$$$  |\$$$$$$  |$$ |\$$$$$$$ |
\__|     \__| \______/ \__|  \__| \______/ $$  ____/  \______/ \__| \____$$ |
                                           $$ |                    $$\   $$ |
                                           $$ |                    \$$$$$$  |
                                           \__|                     \______/
''')


def play(game: Game, resumed: bool = False):
    if not resumed:
        clear()
        print_welcome_text()
        add_players(game)
        game.prepare_game()
    while not game.win():
        game.is_win()
        current_player_info(game)
        show_menu()
        menu_option = players_input_menu()
        menu_action(menu_option, game)
        pause()
    game_over(game)


def game_over(game):
    print(f'\n\nGAME OVER. The winner is: {game.find_winner().name()}')
    print('\nFINAL RESULTS\n')
    show_final_status(game)


def show_final_status(game):
    show_all_players_status(game)


def pause():
    print('\n[Press ENTER to conntinue]')
    input()
    clear()


def add_one_player(game, names):
    name = word_input()
    while name in names:
        print('Players must have unique names. Please enter again.')
        name = word_input()
    names.append(name)
    game.add_player(name)


def add_players(game):
    names = []
    print('Enter name of first player:')
    add_one_player(game, names)
    print('Enter name of second player:')
    add_one_player(game, names)
    answer = True
    while len(game._players) < GameConstants.MAX_PLAYERS_NUM and answer:
        print('Do you want to add next player? ([Y]/n)')
        answer = bool_input()
        if answer:
            print("Enter player's name:")
            add_one_player(game, names)


def bool_input():
    try:
        answer = input().strip().lower().split()[0]
    except (IndexError):
        return True
    false_answers = ['no', 'n']
    true_answers = ['yes', 'y']
    if answer not in false_answers and \
            answer not in true_answers:
        print('Incorrect answer. Please enter yes or no')
        answer = bool_input()
    return answer in true_answers


def word_input():
    word = input().strip().split()
    if len(word) != 1:
        print('Please enter one word')
        word = word_input()
    return word[0]


def int_input():
    players_input = input().strip()
    try:
        players_input = int(players_input)
    except (ValueError):
        print('Input is incorrect. Please enter a positive integer.')
        players_input = int_input()
    if players_input < 0:
        print('Input is incorrect. Please enter a positive integer.')
        players_input = int_input()
    return players_input


def make_property_transaction(game):
    if not game.can_afford(game.current_field().price()):
        print('\nUnfortunately you cannot afford this property')
        return
    print('\nDo you want to buy this property? ([Y]/n)')
    answer = bool_input()
    if answer:
        game.buy_current_property()
        print(f'You paid {game.current_field().price()} ' +
              f'for {game.current_field().name()}')


def passing_start_field(game):
    game.start_field_bonus()
    print(f'\nYou earned {GameConstants.START_FIELD_BONUS}' +
          ' for passsing start field')


def make_move(game):
    game.dice_roll()
    print(f'\nYour dice roll result: {game.current_dice_roll()}')
    game.move_pawn_number_of_dots()
    print('You moved to field :\n' +
          tabulate(game.current_field().step_on_description_table(),
                   tablefmt='rounded_grid'))
    if game._current_player.passed_start_field:
        passing_start_field(game)
    if isinstance(game.current_field(), PropertyField) and \
            game.current_field().owner() is None:
        make_property_transaction(game)
    elif isinstance(game.current_field(), PropertyField) and \
            not game.player_is_owner() and \
            not game.current_field().is_mortgaged():
        pay_rent(game)
    game.change_player()


def bancrupt_menu(menu_option, game):
    if menu_option == BancruptOption.SEE_YOURS:
        show_current_player_status(game)
    elif menu_option == BancruptOption.SELL_HOUSE_HOTEL:
        sell_house_hotel(game)
    elif menu_option == BancruptOption.MORTGAGE:
        mortgage(game)


def show_bancrupt_menu():
    text = '''BANCRUPT MENU press number key to pick option:
    1. See your cards and money
    2. Sell house/ hotel
    3. Mortgage property
    4. Lift mortgage from porperty
    '''
    print(text)


def pay_rent(game):
    amount = game.current_field().current_rent()
    if not game.can_afford(amount):
        print('You cannot afford to pay this rent.')
        if game.total_fortune() > amount:
            # if game.total_fortune() > 0:
            while not game.can_afford(amount):
                print("You must sell some houses or mortgage properties.")
                show_bancrupt_menu()
                menu_option = players_input_menu()
                bancrupt_menu(menu_option, game)
                pause()
        else:
            print("You don't have any property to mortgage. You go bancrupt")
            game.end_game()
            return
    game.pay_rent()
    print(
        f'You paid {amount}' +
        f' to {game.get_current_field_owner_name()}')


def show_all_players_status(game):
    print(game.players_description())


def show_current_player_status(game, streets_only=False):
    print(game.show_player_status(streets_only=streets_only))


def street_input(game):
    f_id = int_input()
    if f_id == 0:
        return 0
    while not game.is_street_owner_by_id(f_id):
        print('You are not owner of this field or this field is not a Street.')
        return 0
    return f_id


def property_input(game):
    f_id = int_input()
    if f_id == 0:
        return 0
    while not game.player_is_owner(f_id):
        print('You are not owner of this field.')
        return 0
    return f_id


def hotel_building_conditions(game, field):
    if not game.can_build_hotel(field):
        print('There must be 4 houses on field to build hotel.')
        return False
    if not game.hotels_build_evenly(field):
        print('You must build 4 houses on every field of colour' +
              ' to start building hotels. Choose another field')
        return False
    if not game.can_afford(field.hotel_cost()):
        print('You cannot afford this hotel')
        return False
    if field.hotel():
        print('There already is a hotel on this field.')
        return False
    return True


def house_building_conditions(game, field):
    if not game.houses_build_evenly(field):
        print('You must build houses evenly on every field in the same' +
              'colour.')
        return False
    if not game.can_afford(field.house_cost()):
        print('You cannot afford this house')
        return False
    if not game.owns_all_of_colour(field):
        print('You must own all fields in that colour to build a house')
        return False
    if field.hotel():
        print('You cannot add any more houses or hotels to this field.')
        return False
    return True


def buy_house_hotel(game):
    print('\nYour cards:')
    show_current_player_status(game, streets_only=True)
    print(
        'Which field fo you want to develop? Type field id to choose.'
        ' [Type 0 to cancel]')
    field_id = street_input(game)
    if field_id == 0:
        return
    field = game.get_field_by_id(field_id)
    if game.is_enough_houses(field) and hotel_building_conditions(
            game, field):
        game.build_hotel(field)
        print(f'You paid {field.hotel_cost()} for a hotel on {field.name()} ')
    elif house_building_conditions(game, field):
        game.build_house(field)
        print(f'You paid {field.house_cost()} for a house on {field.name()} ')


def house_selling_conditions(game, field):
    if not game.is_house_to_sell(field):
        print("There is no house to sell  from that field")
        return False
    if not game.houses_removed_evenly(field):
        print("You must sell houses evenly from all fields in that colour.")
        return False
    return True


def sell_house_hotel(game):
    print('\nYour cards:')
    show_current_player_status(game, streets_only=True)
    print(
        'On which field fo you want to sell house/hotel?' +
        ' Type field id to choose.'
        ' [Type 0 to cancel]')
    field_id = street_input(game)
    if field_id == 0:
        return
    field = game.get_field_by_id(field_id)
    if field.hotel():
        game.sell_hotel(field)
        print(f'You earned {field.hotel_cost()}' +
              f' for selling hotel from {field.name()}')
    elif house_selling_conditions(game, field):
        game.sell_house(field)
        print(f'You earned {field.house_cost()}' +
              f' for selling house from {field.name()}')


def mortgage_conditions(game, field):
    if game.houses_on_street(field):
        print("You must sell all houses and hotels from field to mortgage.")
        return False
    if field.is_mortgaged():
        print("This field is already mortgaged")
        return False
    return True


def mortgage(game):
    # TODO if mortgage already done
    print('\nYour cards:')
    show_current_player_status(game)
    print(
        'On which field fo you want to mortgage? Type field id to choose.'
        ' [Type 0 to cancel]')
    field_id = property_input(game)
    if field_id == 0:
        return
    field = game.get_field_by_id(field_id)
    if mortgage_conditions(game, field):
        game.mortgage(field)
        print(
            f'You earned {field.mortgage_price()}' +
            f' for mortage of {field.name()}')


def lift_mortgage_conditions(game, field):
    if not field.is_mortgaged():
        print('You can lift mortage only from mortaged fields.')
        return False
    return True


def lift_mortgage(game):
    print('\nYour mortaged cards:')
    show_current_player_status(game)
    print('To lift mortgage you have to pay additional 10% of'
          ' mortgage price. Type field id to choose.'
          ' [Type 0 to cancel]')
    field_id = property_input(game)
    if field_id == 0:
        return
    field = game.get_field_by_id(field_id)
    if lift_mortgage_conditions(game, field):
        game.lift_mortgage(field)
        print(
            f'You have spend {round(field.mortgage_price() * 1.1)} on lifting'
            f'mortgage of {field.name()}')


def menu_action(menu_option, game):
    if menu_option == MenuOption.SEE_ALL:
        show_all_players_status(game)
    elif menu_option == MenuOption.SEE_YOURS:
        show_current_player_status(game)
    elif menu_option == MenuOption.BUY_HOUSE_HOTEL:
        buy_house_hotel(game)
    elif menu_option == MenuOption.SELL_HOUSE_HOTEL:
        sell_house_hotel(game)
    elif menu_option == MenuOption.MORTGAGE:
        mortgage(game)
    elif menu_option == MenuOption.LIFT_MORTGAGE:
        lift_mortgage(game)
    elif menu_option == MenuOption.THROW_DICE:
        make_move(game)


def players_input_menu():
    menu_option = int_input()
    if menu_option not in menu_values():
        print('Option unavailable')
        return
    return menu_option


def current_player_info(game):
    print(f'\nCURRENT PLAYER: { game.current_player_name()} ')


def show_menu():
    text = '''MAIN MENU press number key to pick option:
    1. See all players cards and money
    2. See your cards and money
    3. Buy house/ hotel
    4. Sell house/ hotel
    5. Mortgage property
    6. Lift mortgage from porperty
    7. Throw dice to make your move
    '''
    print(text)
