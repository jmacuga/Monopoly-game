from classes.game import Game
from classes.field import PropertyField
from enum import IntEnum
from classes.game_constants import GameConstants
import os


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
    while not game.win():
        current_player_info(game)
        show_menu()
        menu_option = players_input_menu()
        menu_action(menu_option, game)


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
    print('Do you want to add next player? [Y/n]')
    answer = bool_input()
    while answer and len(game._players) < GameConstants.MAX_PLAYERS_NUM:
        print("Enter player's name:")
        add_one_player(game, names)
        print('Do you want to add next player? [Y/n]')
        answer = bool_input()


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
        print('Input is incorrect. Please enter an integer.')
        players_input = int_input()
    return players_input


def make_property_transaction(game):
    if not game.player_can_afford(game.current_field().price()):
        print('\nUnfortunately you cannot afford this property')
        return
    print('\nDo you want to buy this property?[Y/n')
    answer = bool_input()
    if answer:
        game.buy_current_property()
        print(f'You paid {game.current_field().price()} ' +
              f'for {game.current_field().name()}')


def make_move(game):
    game.dice_roll()
    print(f'\nYour dice roll result: {game.current_dice_roll()}')
    game.move_pawn_number_of_dots()
    print(f'You moved to field :\t {game.current_field()}')
    if isinstance(game.current_field(), PropertyField) and \
            game.current_field().owner() is None:
        make_property_transaction(game)
    elif isinstance(game.current_field(), PropertyField) and \
            not game.player_is_owner():
        pay_rent(game)
    game.change_player()


def pay_rent(game):
    if not game.player_can_afford(game.current_field().current_rent()):
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


def show_current_player_status():
    pass


def buy_house_hotel():
    pass


def menu_action(menu_option, game):
    clear()
    if menu_option == MenuOption.SEE_ALL:
        show_all_players_status(game)
    elif menu_option == MenuOption.SEE_YOURS:
        show_current_player_status()
    elif menu_option == MenuOption.BUY_HOUSE_HOTEL:
        buy_house_hotel()
    elif menu_option == MenuOption.THROW_DICE:
        make_move(game)


def players_input_bool():
    pass


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
