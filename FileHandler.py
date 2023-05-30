import configparser
import csv


class FileHandler:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

    def get_users_from_file(self):
        users = {}
        with open('Users.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            fieldnames = reader.fieldnames
            for row in reader:
                for fieldname in fieldnames:
                    if fieldname.startswith('User'):
                        user_id = row[fieldname]
                    elif fieldname.startswith('API'):
                        api_key = row[fieldname]
                users[user_id] = api_key
            return users

    def translation_mapper(self):
        field_mappings = self.config['FIELDINFO']
        translation_mapping = {value: field_mappings.get(key) for key, value in field_mappings.items()}
        return translation_mapping
