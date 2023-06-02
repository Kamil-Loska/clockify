import csv


class UserHandler:

    def __init__(self, user_file):
        self.user_file = user_file

    def load_user_credentials_from_file(self):
        users = {}
        with open('Users.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user_id = row['User_ID']
                api_key = row['API_KEY']
                users[user_id] = api_key
        return users
