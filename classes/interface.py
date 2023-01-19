from classes.game import Game
from classes.field import PropertyField, SpecialField, Street
from classes.game_constants import GameConstants, ChanceFieldAction
from enum import IntEnum
import os
import sys
import pickle
from tabulate import tabulate


class MenuOption(IntEnum):
    """Enum class containing available main menu options."""
    THROW_DICE = 1
    SEE_ALL = 2
    SEE_YOURS = 3
    BUY_HOUSE_HOTEL = 4
    SELL_HOUSE_HOTEL = 5
    MORTGAGE = 6
    LIFT_MORTGAGE = 7
    SAVE_AND_EXIT = 8


class BancruptOption(IntEnum):
    """Enum class containing available bancrupt menu options.

    Enum class containing otpions available in the menu shown
                            when player canot afford rent."""
    SEE_YOURS = 1
    SELL_HOUSE_HOTEL = 2
    MORTGAGE = 3


def clear():
    """Clears the terminal window."""
    return os.system('clear')


def menu_values():
    """Gets list of values of the ManuOption variables."""
    return [mem.value for mem in MenuOption]


def print_welcome_text():
    """Shows "Monopoly" banner and game instructions"""
    banner = '''
$$\\      $$\\                                                   $$\\
$$$\\    $$$ |                                                  $$ |
$$$$\\  $$$$ | $$$$$$\\  $$$$$$$\\   $$$$$$\\   $$$$$$\\   $$$$$$\\  $$ ''' +\
        '''|$$\\   $$\\
$$\\$$\\$$ $$ |$$  __$$\\ $$  __$$\\ $$  __$$\\ $$  __$$\\ $$  __$$\\''' +\
        ''' $$ |$$ |  $$ |
$$ \\$$$  $$ |$$ /  $$ |$$ |  $$ |$$ /  $$ |$$ /  $$ |$$ /  $$ |$$ |$$ |  $$ |
$$ |\\$  /$$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |$$ |  $$ |
$$ | \\_/ $$ |\\$$$$$$  |$$ |  $$ |\\$$$$$$  |$$$$$$$  |\\$$$$$$  |$$ |''' +\
        '''\\$$$$$$$ |
\\__|     \\__| \\______/ \\__|  \\__| \\______/ $$  ____/  \\______/''' +\
        ''' \\__| \\____$$ |
                                           $$ |                    $$\\   $$ |
                                           $$ |                    \\$$$$$$  |
                                           \\__|                     \\______/
'''
    text = "\nWelcome to the Monopoly Game.\nYou may add up to " +\
        f"{GameConstants.MAX_PLAYERS_NUM} players. " +\
        f"The game ends when you reach {GameConstants.MAX_NUM_OF_ROUNDS}" +\
        " rounds. \nRemember you can do your property menagement only" +\
        " before you thow dice. \nThe winner is the last player who isn't" +\
        " bancrupt, or the player who accumulates \nthe biggest fortune" +\
        " in cash and property. "

    print(banner + text)


def play(game: Game, resumed: bool = False) -> None:
    """Plays the game.

    Main game loop, adds players, sets up the game, shows main menu
    in the loop and picks menu option based on player input.

    Parameters
    ----------
    game : Game
        game object that contains current game state.
    resumed : bool, defaul= False
        inidcates wether game is loaded form file.
    """
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


def game_over(game: Game) -> None:
    """Prints final results, the winner and all players status. """
    print(f'\n\nGAME OVER. The winner is: {game.find_winner().name()}')
    print('\nFINAL RESULTS\n')
    show_all_players_status(game)


def pause() -> None:
    """Waits for player input to clear the terminal window."""
    print('\n[Press ENTER to conntinue]')
    input()
    clear()


def add_one_player(game: Game, names: list[str]) -> None:
    """Asks player for the name of the new player and adds him to the game."""
    name = word_input()
    while name in names:
        print('Players must have unique names. Please enter again.')
        name = word_input()
    names.append(name)
    game.add_player(name)


def add_players(game: Game) -> None:
    """Adds all game player objects based on the input."""
    names = []
    print('\nEnter the name of the first player:')
    add_one_player(game, names)
    print('Enter the name of second player:')
    add_one_player(game, names)
    answer = True
    while len(game._players) < GameConstants.MAX_PLAYERS_NUM and answer:
        print('Do you want to add next player? ([Y]/n)')
        answer = bool_input()
        if answer:
            print("Enter player's name:")
            add_one_player(game, names)


def bool_input() -> bool:
    """Asks player for yes/no input until he enters correct value.

    If input is not provided, chooses 'yes'.
    """
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


def word_input() -> str:
    """Asks player for char sequence input until he enters correct value.

    Does not protect from characters other than letters of alphabet.
    """
    word = input().strip().split()
    if len(word) != 1:
        print('Please enter one word')
        word = [word_input()]
    return word[0]


def int_input() -> int:
    """Asks player for positive integer input until he enters correct value."""
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


def make_property_transaction(game: Game) -> None:
    """Ask player if he wants to buy the property and makes the transaction.

    Doesn't ask the player if he wants to buy the field if he can't afford it.
    Shows the message with the amount of money payed and name of the field.
    """
    if not game.can_afford(game.current_field().price()):
        print('\nUnfortunately you cannot afford this property')
        return
    print('\nDo you want to buy this property? ([Y]/n)')
    answer = bool_input()
    if answer:
        game.buy_current_property()
        print(f'You paid {game.current_field().price()} ' +
              f'for {game.current_field().name()}')


def passing_start_field(game: Game) -> None:
    """Give player start field bonus and print the message with the amouint."""
    game.start_field_bonus()
    print(f'\nYou earned {GameConstants.START_FIELD_BONUS}' +
          ' for passsing start field')


def chance_field_action(game: Game) -> None:
    """Show the chance card description and use it.

    Get new chance card, and use it on the player. If the player can't afford
    to pay the amount shown on the chance card, the bancrupt menu is shown.
    """
    card = game.get_new_chance_card()
    print(card)
    if card.action() == ChanceFieldAction.PAY.value:
        if not game.can_afford(card.money()):
            print('You cannot afford to pay.')
            if not make_money_from_properties(game, card.money()):
                return
    game.chance_field_action()


def make_move(game: Game) -> None:
    """Makes whole players move and change player.

    Gets new dice roll and moves player on the board. Shows dice roll result
    and field table of the field taht player lands on. Chooses different
     actions depending on the field type and changes player.
    """
    game.dice_roll()
    print(f'\nYour dice roll result: {game.current_dice_roll()}')
    game.move_pawn_number_of_dots()
    field = game.current_field()
    print('You moved to field :\n' +
          tabulate(field.step_on_description_table(),
                   tablefmt='rounded_grid'))
    if game._current_player.passed_start_field:
        passing_start_field(game)
    if isinstance(field, PropertyField) and \
            field.owner() is None:
        make_property_transaction(game)
    elif isinstance(field, PropertyField) and \
            not game.player_is_owner() and \
            not field.is_mortgaged():
        pay_rent(game)
    elif type(field) == SpecialField and field.name() == 'chance':
        chance_field_action(game)
    game.change_player()


def bancrupt_menu(menu_option: int, game: Game) -> None:
    """Picks menu action from the bancrupt menu."""
    if menu_option == BancruptOption.SEE_YOURS:
        show_current_player_status(game)
    elif menu_option == BancruptOption.SELL_HOUSE_HOTEL:
        sell_house_hotel(game)
    elif menu_option == BancruptOption.MORTGAGE:
        mortgage(game)


def show_bancrupt_menu():
    """Prints menu showt to the player when he cannot affors to pay."""
    text = '''BANCRUPT MENU press number key to pick option:
    1. See your cards and money
    2. Sell house/ hotel
    3. Mortgage property
    4. Lift mortgage from porperty
    '''
    print(text)


def make_money_from_properties(game: Game, amount: int) -> bool:
    """Makes player sell his belongings, until he is able to pay given amount.

    If the player's fortune is worth less than given amount, makes the player
    bancrupt.Else prints bancrupt menu and makes him sell houses, hotels and
    mortgage fields until he gets enough of cash.

    Parameters
    ----------
    game : Game
        game object representing game state.
    amount : int
        amount debt

    Returns
    -------
    bool
        Indicates if the player got the required amount.
    """
    if game.total_fortune() > amount:
        while not game.can_afford(amount):
            print("You must sell some houses or mortgage properties.")
            show_bancrupt_menu()
            menu_option = players_input_menu()
            bancrupt_menu(menu_option, game)
            pause()
        return True
    else:
        print("You don't have any property to mortgage. You go bancrupt")
        game.make_bancrupt()
        return False


def pay_rent(game: Game) -> None:
    """Makes player pay rent and shows him the message how much he payed.

    If the player doesn't have enough money to pay, makes him get cash
    from porperty or makes bancrupt.
    """
    amount = game.current_field().current_rent()
    if not game.can_afford(amount):
        print('You cannot afford to pay this rent.')
        if not make_money_from_properties(game, amount):
            return
    game.pay_rent()
    print(
        f'You paid {amount}' +
        f' to {game.get_current_field_owner_name()}')


def show_all_players_status(game: Game) -> None:
    """Prints description tables of each player."""
    print(game.players_description())


def show_current_player_status(game: Game, streets_only: bool = False) -> None:
    """SHows full description tables of the current player and his fields"""
    print(game.show_player_status(streets_only=streets_only))


def street_input(game: Game) -> int:
    """Gets input of the index of property field that is Street.

    Returns 0 if the input is equal to 0 or incorrect
    """
    f_id = int_input()
    if f_id == 0:
        return 0
    elif f_id not in range(1, GameConstants.MAX_FIELD_ID + 1):
        print("Field doesn't exist")
        return 0
    elif not game.player_is_owner(f_id) \
            and type(game.get_field_by_id(f_id)) is not Street:
        print('You are not owner of this field or this field is not a Street.')
        return 0
    return f_id


def property_input(game: Game) -> int:
    """Gets input of the index of porperty field.

    Returns 0 if the input is equal to 0 or incorrect.
    """
    f_id = int_input()
    if f_id == 0:
        return 0
    elif f_id not in range(1, GameConstants.MAX_FIELD_ID + 1):
        print("Field doesn't exist")
        return 0
    elif not game.player_is_owner(f_id):
        print('You are not owner of this field.')
        return 0
    return f_id


def hotel_building_conditions(game: Game, field: Street) -> bool:
    """Checks if the conditions to build a hotel on given field are met.

    Shows appropriate communicate and returns the result of the check.

    Parameters
    ----------
    game: Game
        game object representing game state.
    field : Street
        field that the hous is meant to be build on.

    Returns
    -------
    bool
        indicator if the hotel can be build
    """
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


def house_building_conditions(game: Game, field: Street) -> bool:
    """Checks if the conditions to build a house on given field are met.

    Shows appropriate communicate and returns the result of the check.

    Parameters
    ----------
    game: Game
        game object representing game state.
    field : Street
        field that the hous is meant to be build on.

    Returns
    -------
    bool
        indicator if the house can be build
    """
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


def buy_house_hotel(game: Game) -> None:
    """Shows player his cards and builds house/hotel on chosen street.

    Asks player to choose the field he wants to upgrade. After transaction
    shows the message how much money did he spend. Cancels when input is
    equal to 0.
    """
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


def house_selling_conditions(game: Game, field: Street) -> bool:
    """Checks if the conditions to sell a house on given field are met.

    Shows appropriate communicate and returns the result of the check.

    Parameters
    ----------
    game: Game
        game object representing game state.
    field : Street
        field that the house is meant to be sold.

    Returns
    -------
    bool
        indicator if the house can be sold.
    """
    if not game.is_house_to_sell(field):
        print("There is no house to sell  from that field")
        return False
    if not game.houses_removed_evenly(field):
        print("You must sell houses evenly from all fields in that colour.")
        return False
    return True


def sell_house_hotel(game):
    """Shows the player his cards and sells house/hotel from chosen one.

    Asks player to choose the field he wants to downgrade. After transaction
    shows the message how much money did he earn. Cancels when input is
    equal to 0.
    """
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


def mortgage_conditions(game: Game, field: PropertyField) -> bool:
    """Checks if the conditions to mortgage a property were met.

    Shows appropriate communicate and returns the result of the check.

    Parameters
    ----------
    game: Game
        game object representing game state.
    field : PropertyField
        field that is meant to be mortgaged.

    Returns
    -------
    bool
        indicator if the property can be mortgaged.
    """
    if game.is_house_to_sell(field):
        print("You must sell all houses and hotels from field to mortgage.")
        return False
    if field.is_mortgaged():
        print("This field is already mortgaged")
        return False
    return True


def mortgage(game: Game) -> None:
    """Shows the player his cards and mortgages chosen one.

    Asks player to choose the field he wants to mortgage. After transaction
    shows the message how much money did he earn. Cancels when input is
    equal to 0.
    """
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


def lift_mortgage_conditions(game: Game, field: PropertyField) -> bool:
    """Checks if the conditions to lift mortgage a property were met.

    Shows appropriate communicate and returns the result of the check.

    Parameters
    ----------
    game: Game
        game object representing game state.
    field : PropertyField
        field that mortgage is lifted.

    Returns
    -------
    bool
        indicator taht the mortgage can be lifted.
    """
    if not field.is_mortgaged():
        print('You can lift mortage only from mortaged fields.')
        return False
    return True


def lift_mortgage(game):
    """Shows the player his cards and lifts mortgage on chosen one.

    Asks player to choose the field he wants to lift mortgage. After
    transaction shows the message how much money did he spend. Cancels
    when input is equal to 0.
    """
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


def save_and_exit(game: Game) -> None:
    """Asks for the file name and saves the game object to pickle format."""
    print('Enter the name of file:')
    filename = word_input()
    with open(filename, 'wb') as pkl:
        pickle.dump(game, pkl)
    sys.exit(f'GAME SAVED TO {filename}')


def menu_action(menu_option, game):
    """Call function equivalent to the given menu option."""
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
    elif menu_option == MenuOption.SAVE_AND_EXIT:
        save_and_exit(game)


def players_input_menu() -> any:
    """Get players input and return if it's valid main menu option."""
    menu_option = int_input()
    if menu_option not in menu_values():
        print('Option unavailable')
        return
    return menu_option


def current_player_info(game: Game) -> None:
    """Print the name of current player."""
    print(f'\nCURRENT PLAYER: { game.current_player_name()} ')


def show_menu():
    """Print Main menu."""
    text = '''MAIN MENU press number key to pick option:
    1. Throw dice to make your move
    2. See all players cards and money
    3. See your cards and money
    4. Buy house/ hotel
    5. Sell house/ hotel
    6. Mortgage property
    7. Lift mortgage from porperty
    8. Save and exit
    '''
    print(text)


def load_game(filename: str) -> None:
    """Load game object from pickle file,

    Parameters
    ----------
    filename : str
        name of the pickle file with teh game object

    Raises:
    TypeError
        when loaded object is not Game instance.
    """
    try:
        with open(filename, 'rb') as pkl:
            game = pickle.load(pkl)
        if type(game) is not Game:
            raise TypeError('Type of loaded object is not Game')
        play(game, resumed=True)
    except FileNotFoundError as e:
        print(e)
