import csv

class UserHandler:

    def __init__(self, user_file):
        self.user_file = user_file

    def load_user_credentials_from_file(self):
        with open('Users.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user_id = row.get('User_ID')
                api_key = row.get('API_KEY')
                if user_id and api_key:
                    return api_key, user_id
