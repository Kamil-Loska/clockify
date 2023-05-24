import requests
import datetime
import csv
import os

class ClockifyApp:

    def __init__(self):
        self.API_KEY = 'API_KEY'
        self.WORKSPACE_ID = 'WORKSPACE_ID'
        self.USER_ID = 'USER_ID'
        self.BASE_URL = 'https://api.clockify.me/api/v1/'
    def get_time_entries_per_user(self, start_date, end_date):

        endpoint = f'workspaces/{self.WORKSPACE_ID}/user/{self.USER_ID}/time-entries'
        params = {
            'start': f'{start_date}T00:00:00Z',
            'end': f'{end_date}T23:59:59Z',
        }
        users_data = self.send_get_request(endpoint, params)

        return users_data

    def generate_raport(self, date_from='', date_to=''):
        if not self.validate_date_format(date_from, date_to):
            print("Invalid date format. Please provide dates in the format 'YYYY-MM-DD'. ")
            return

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
                    'Imię i nazwisko': " ".join(member_name.split(" ")[::-1]),
                    'Data': create_date,
                    'Czas trwania': self.format_duration(duration),
                    'Opis zadania': name,
                }
                print(report_data)

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
            datetime.datetime.strptime(first_date, '%Y-%m-%d')
            datetime.datetime.strptime(second_date, '%Y-%m-%d')
            return True
        except ValueError:
            return False

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
            fieldnames = ['Imię i nazwisko', 'Data', 'Czas trwania', 'Opis zadania']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if is_empty:
                writer.writeheader()
            writer.writerow(report_data)

        with open(filename, 'r') as csvfile:
            if csvfile.read().strip() == '':
                print(filename)
                return
