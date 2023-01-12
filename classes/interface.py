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
    THROW_DICE = 4


def clear():
    return os.system('clear')


def menu_values():
    return [mem.value for mem in MenuOption]


def play(game: Game):
    clear()
    add_players(game)
    game.prepare_game()
    while not game.is_win():

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
        print('Do you want to add next player? [Y/n]')
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
    print('\nDo you want to buy this property?[Y/n]')
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
            not game.player_is_owner():
        pay_rent(game)
    game.change_player()


def pay_rent(game):
    if not game.can_afford(game.current_field().current_rent()):
        print('You cannot afford to pay this rent.')
        # TODO
        game._win = True
        return
    game.pay_rent()
    print(
        f'You paid {game.current_field().current_rent()}' +
        f' to {game.get_current_field_owner_name()}')


def show_all_players_status(game):
    print(game.players_description())


def show_current_player_status(game, streets_only=False):
    print(game.show_player_status(streets_only=streets_only))


def field_input(game):
    f_id = int_input()
    if f_id == 0:
        return 0
    while not game.is_street_owner_by_id(f_id):
        print('You are not owner of this field or this field is not a Street.')
        return 0
    return f_id


def check_hotel_building_conditions(game, field_id):
    if not game.can_build_hotel(field_id):
        print('There must be 4 houses on field to build hotel.')
        return False
    if not game.hotels_build_evenly(field_id):
        print('You must build 4 houses on every field of colour to start building hotels. Choose another field')
        return False
    if not game.can_afford_hotel(field_id):
        print('You cannot afford this hotel')
        return False
    if game.is_hotel(field_id):
        print('There already is a hotel on this field.')
        return False
    return True


def check_house_building_conditions(game, field_id):
    if not game.houses_build_evenly(field_id):
        print('You must build houses evenly on every field in the same colour. Choose another field')
        return False
    if not game.can_afford_house(field_id):
        print('You cannot afford this house')
        return False
    if not game.owns_all_of_colour(field_id):
        print('You must own all fields in that colour to build a house')
        return False
    if not game.is_hotel(field_id):
        print('You cannot add any more houses or hotel to this field.')
        return False
    return True


def buy_house_hotel(game):
    print('\nYour cards:')
    show_current_player_status(game, streets_only=True)
    print(
        'Which field fo you want to develop? Type field id to choose. [Type 0 to cancel]')
    field_id = field_input(game)
    if field_id == 0:
        return
    if game.can_build_hotel(field_id) and check_hotel_building_conditions(game, field_id):
        game.build_hotel(field_id)
    elif check_house_building_conditions(game, field_id):
        game.build_house(field_id)


def menu_action(menu_option, game):
    if menu_option == MenuOption.SEE_ALL:
        show_all_players_status(game)
    elif menu_option == MenuOption.SEE_YOURS:
        show_current_player_status(game)
    elif menu_option == MenuOption.BUY_HOUSE_HOTEL:
        buy_house_hotel(game)
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
    3. Buy house/hotel
    4. Throw dice to make your move
    '''
    print(text)
