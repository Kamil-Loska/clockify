import csv
from typing import List


class UserHandler:

    def __init__(self, user_file: str):
        self.user_file = user_file

    def load_user_credentials_from_file(self) -> List[str]:
        users = []
        with open(self.user_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                users.append(row)
        return users
