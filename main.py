"""main"""
from os import system, name as system_name
import time
from inventory import Inventory
from json_reader import JsonHandler
import operations


class Main:
    running = True
    json_reader = JsonHandler('games.json')
    database = None
    inventory = None

    def __init__(self):
        pass

    def module_start(self):
        self.database = self.json_reader.read_json()
        self.inventory = Inventory(self.database)
        self.main_run()

    def main_run(self):
        self.clear_console()
        print('WELCOME SYSTEMIC!')
        while self.running:
            print('Please choose one of the options below:')
            option = input(
                '''
1- Add new game.
2- Search a game
3- Rent a game.
4- Return a game.
5- delete a game.
6- exit program.

Option: '''
            )

            if option == '1':
                self.create_game()
            elif option == '2':
                self.search_game()
            elif option == '3':
                self.rent_game()
            elif option == '4':
                self.return_game()
            elif option == '5':
                self.delete_game()
            elif option == '6':
                self.exit_program()
            else:
                print('Choose an option between 1 and 6.')
                self.clear_console()

    def create_game(self):
        title, price = operations.get_game_creation_inputs(self.clear_console)

        try:
            code = operations.gen_game_code(title, self.inventory.count_games())
            self.inventory.insert(title, price, code)
            self.json_reader.write_json(self.database)
        except Exception as e:
            print(f'Unexpected error: {e}')

    def search_game(self):
        loop = True
        while loop:
            self.clear_console()
            print('Please choose one of the options below:')
            option = input(
                '''
    1- By code.
    2- By title.
    3- Go back.

    Option: '''
                )
            if option == "1":
                code = operations.get_game_code_input()
                self.inventory.search_game_by_code(code)
            elif option == "2":
                title = operations.get_game_title_input()
                self.inventory.search_game_by_title(title)
            elif option == "3":
                loop = False
            else:
                print('Choose an option between 1 and 3.')

    def rent_game(self):
        code = operations.get_game_code_input()
        if self.inventory.rent_game(code):
            self.json_reader.write_json(self.database)

    def return_game(self):
        code = operations.get_game_code_input()
        if self.inventory.return_game(code):
            self.json_reader.write_json(self.database)

    def delete_game(self):
        code = operations.get_game_code_input()
        if self.inventory.delete_game(code):
            self.json_reader.write_json(self.database)

    def exit_program(self):
        self.running = False
        print('See you soon systemic!')

    @staticmethod
    def clear_console():
        time.sleep(2)
        # for windows
        if system_name == 'nt':
            _ = system('cls')

        # for mac and linux(here, os.name is 'posix')
        else:
            _ = system('clear')


if __name__ == '__main__':
    main = Main()
    main.module_start()
