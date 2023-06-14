import csv


class UserHandler:

    def __init__(self, user_file):
        self.user_file = user_file

    def load_user_credentials_from_file(self):
        with open(self.user_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                yield row
