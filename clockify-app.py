import argparse
import requests
from datetime import datetime
import csv
import os
import configparser

class ClockifyApp:

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        self.API_KEY = ''
        self.USER_ID = ''

        self.BASE_URL = 'https://api.clockify.me/api/v1/'

    def get_time_entries_per_user(self, start_date, end_date):
        workspace_id = self.config['Clockify'].get('WORKSPACE_ID')
        endpoint = f'workspaces/{workspace_id}/user/{self.USER_ID}/time-entries'
        params = {
            'start': f'{start_date}T00:00:00Z',
            'end': f'{end_date}T23:59:59Z',
        }
        all_data = []
        page = 1

        while True:
            params['page'] = page
            response = self.send_get_request(endpoint, params)
            if len(response) == 0:
                break

            all_data.extend(response)
            page += 1

        return all_data

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

    def generate_raport(self, date_from='', date_to=''):
        self.validate_date_format(date_from, date_to)

        users = self.get_users_from_file()
        for user_id, api_key in users.items():
                self.API_KEY = api_key
                self.USER_ID = user_id

                get_data = self.get_time_entries_per_user(date_from, date_to)
                get_user_id, get_user_name = self.get_user_data()

                for data in get_data:
                    create_date = data['timeInterval']['start'][:10]
                    duration = data['timeInterval']['duration']
                    name = data['description']
                    if name == "":
                        name = "In progress..."

                    if data['userId'] == get_user_id and date_from <= create_date <= date_to:
                        member_name = get_user_name

                        report_data = {
                            'Fullname': " ".join(member_name.split(" ")[::-1]),
                            'Date': create_date,
                            'Duration time': self.format_duration(duration),
                            'Task description': name,
                        }
                        report_data = {self.translation_mapper().get(key, key): value for key, value in
                                          report_data.items()}

                        print(report_data)


    def translation_mapper(self):
        translation_mapping = {
            'Fullname': 'Imie i nazwisko',
            'Date': 'Data',
            'Duration time': 'Czas trwania',
            'Task description': 'Opis zadania',
        }
        return translation_mapping
    def format_duration(self, duration):
        if duration != None:
            duration = duration[2:]
            hours = ""
            minutes = ""
            seconds = ""

            if "H" in duration:
                hours, duration = duration.split("H")
                hours += "H "
            if "M" in duration:
                minutes, duration = duration.split("M")
                minutes += "M "
            if "S" in duration:
                seconds, _ = duration.split("S")
                seconds += "S"

            formatted_duration = hours + minutes + seconds
            return formatted_duration.strip()

    def send_get_request(self, endpoint, params=None):
        headers = {
            'X-Api-Key': self.API_KEY,
            'Content-Type': 'application/json'
        }
        url = self.BASE_URL + endpoint
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        return data

    def get_user_data(self):
        endpoint = f'user'
        get_user_data = self.send_get_request(endpoint)
        return get_user_data['id'], get_user_data['name']

    def validate_date_format(self, first_date, second_date):
        try:
            datetime.strptime(first_date, '%Y-%m-%d')
            datetime.strptime(second_date, '%Y-%m-%d')
        except ValueError:
            msg = "Invalid date format!".format((first_date, second_date))
            raise argparse.ArgumentTypeError(msg)

    def create_report(self, report_data):
        filename = 'report.csv'

        is_empty = os.stat(filename).st_size == 0
        if not is_empty:
            with open(filename, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row == report_data:
                        return

        with open(filename, 'a', newline='') as csvfile:
            fieldnames = ['Imie i nazwisko', 'Data', 'Czas trwania', 'Opis zadania']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if is_empty:
                writer.writeheader()

            report_data_en = {self.translation_mapper().get(key, key): value for key, value in report_data.items()}
            writer.writerow(report_data_en)

        with open(filename, 'r') as csvfile:
            if csvfile.read().strip() == '':
                print(filename)
                return

