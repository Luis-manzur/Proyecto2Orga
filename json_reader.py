"""Txt reader"""
import json


class JsonHandler:
    def __init__(self, file: str):
        self.file: str = file

    def read_json(self):
        """load the data"""
        database = {"codes": {}, "titles_index": {}}
        try:
            with open(self.file, "r") as f:
                database = json.load(f)

        except FileNotFoundError:
            print('File not found, empty database will be initialized')

        finally:
            return database
    
    def write_json(self, database):
        with open(self.file, "w") as f:
            json.dump(database, f)
