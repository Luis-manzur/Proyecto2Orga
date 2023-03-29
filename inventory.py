"""Inventory"""
from json_reader import JsonHandler


class Inventory:
    primary_group_capacity = 3
    overflow_group_capacity = 6

    def __init__(self, database):
        self.database = database

    @staticmethod
    def hash_code(code):
        return hash(code) % 3

    def insert(self, title, price, code):
        """Insert the game in the database"""
        if code in self.database["codes"]:
            print("Error, the game is already registered.")
            return True

        if title in self.database['titles_index']:
            print("Error, the game is already registered.")
            return False

        game = {"code": code, "title": title, "price": price, "status": "AVAILABLE"}

        group_index = self.hash_code(code)
        group = self.database["codes"].setdefault(group_index, [])
        if len(group) < self.primary_group_capacity:
            group.append(game)
        else:
            overflow_index = 0
            while overflow_index < 6:
                overflow_group = group.setdefault(str(overflow_index), [])
                if len(overflow_group) < self.overflow_group_capacity:
                    overflow_group.append(game)
                    break
                overflow_index += 1
            else:
                print("Error: No hay espacio en la base de datos para registrar el nuevo juego.")
                return

        self.database["titles_index"][title] = code

        print("Game registered successfully.")
        return True

    def search_game_by_code(self, code):
        """Look up game by code"""
        group_index = self.hash_code(code)
        group = self.database["codes"].get(group_index, [])
        for game in group:
            if game["code"] == code:
                print(game)
                return game
        for overflow_group in group:
            for game in overflow_group:
                if game["code"] == code:
                    print(game)
                    return game
        print('Game code not found')
        return None

    def search_game_by_title(self, title):
        """Look up game by title"""
        code = self.database["titles_index"].get(title)
        if code is not None:
            return self.search_game_by_code(code)
        else:
            print('Game title Not Found')
            return None

    def rent_game(self, code):
        """Alquilar un juego."""
        game = self.search_game_by_code(code)
        if game is None:
            return False
        elif game["status"] == "RENTED":
            print("Error: The game is already rented")
            return False
        else:
            game["status"] = "RENTED"
            print(f'{game["title"]} has been rented')
            return True

    def return_game(self, code):
        """Return a game."""
        game = self.search_game_by_code(code)
        if game is None:
            print("Error: The game code is not registered in the database.")
            return False
        elif game["status"] == "AVAILABLE":
            print("Error: The game is already in stock.")
            return False
        else:
            game["status"] = "AVAILABLE"
            print(f'{game["title"]} has been returned')
            return True

    def delete_game(self, code):
        game = self.search_game_by_code(code)

        if game is None:
            return False
        group_index = self.hash_code(code)
        group = self.database["codes"].get(group_index, [])
        if game in group:
            group.remove(game)
        else:
            for overflow_group in group:
                if game in overflow_group:
                    overflow_group.remove(game)
                    break
            else:
                # The game was not found in the database
                print("Error: The game code is not registered in the database.")
                return False
        del self.database["titles_index"][game["title"]]
        self.compact_groups()

        return True

    def count_games(self):
        """Count the number of games in the database."""
        count = 0
        for group in self.database["codes"].values():
            count += len(group)
        return count

    def compact_groups(self):
        """Compact the primary and overflow groups to keep them as compact as possible."""
        for group_index, group in self.database["codes"].items():
            overflow_groups = [overflow_group for overflow_group in group.values() if len(overflow_group) == 0]
            for overflow_group in overflow_groups:
                del group[overflow_group]
            if len(group) == 0:
                del self.database["codes"][group_index]
            elif len(group) == 1 and len(overflow_groups) > 0:
                overflow_group = overflow_groups[0]
                group[overflow_group] = self.database["codes"][group_index][overflow_group]
                del self.database["codes"][group_index][overflow_group]