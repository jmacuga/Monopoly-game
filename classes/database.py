import json


class Database:
    def __init__(self):
        pass

    def load_cards(self, file_name):
        with open(file_name, 'r') as fp:
            json_reader = json.load(fp)


class PropertyDatabase(Database):
    def __init__(self):
        super().__init__()


class ChanceDatabase(Database):
    def __init__(self):
        super().__init__()


class CommunityChestDatabase(Database):
    def __init__(self):
        super().__init__()
