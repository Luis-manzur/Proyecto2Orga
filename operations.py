"""Extra operations"""
import time


def gen_game_code(title: str, games_counter):
    title = title.upper()

    games_counter_str = '0' + str(games_counter + 1) if games_counter + 1 < 10 else str(games_counter + 1)

    return title[0:6] + games_counter_str


def get_game_code_input():
    code = input('Game code: ')
    return code


def get_game_title_input():
    title = input('Game title: ')
    return title


def get_game_creation_inputs(clear_console):
    loop = True
    title = None
    price = None
    while loop:
        clear_console()
        print('To add a new game please fill the form:')

        try:
            title = input('Title: ')
            if len(title) < 6:
                raise Exception('The title must have at least 6 alphanumeric characters.')
            elif len(title) > 10:
                raise Exception('The title has a maximum length of 10 characters')
        except Exception as e:
            print(f'Title error: {e}')
            continue

        try:
            price = int(input('price: '))
            if price < 0 or price > 999:
                raise Exception('The value is less than 0 or greater than 999.')
        except Exception as e:
            print('The number must be an integer number between 0 and 999. Please try again.')
            print(f'Explicit error: {e}')
            continue

        return title, price
