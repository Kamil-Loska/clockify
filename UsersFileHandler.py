import csv
from User import User


class UserHandler:
    def __init__(self, user_file: str):
        self.user_file = user_file

    def load_user_credentials_from_file(self) -> list[User]:
        users = []
        with open(self.user_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user = User(row['User_ID'], row['API_KEY'], row['Department'])
                users.append(user)

        return users
