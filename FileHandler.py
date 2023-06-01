import configparser
import csv


class FileHandler:

    def __init__(self, config_file):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def get_users_from_file(self):
        users = {}
        with open('Users.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user_id = row['User_ID']
                api_key = row['API_KEY']
                users[user_id] = api_key
        return users

    def translation_mapper(self):
        field_mappings = self.config['FIELDINFO']
        translation_mapping = {value: field_mappings.get(key) for key, value in field_mappings.items()}
        return translation_mapping
