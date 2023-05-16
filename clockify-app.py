import requests
import datetime
import sys
import csv
import os

class ClockifyApp:

    def __init__(self):
        self.API_KEY = 'API_KEY'
        self.BASE_URL = 'https://api.clockify.me/api/v1/'


    def generate_raport(self):
        workspace_id = 'WORKSPACE_ID'
        user_id = 'USER_ID'
        endpoint = f'workspaces/{workspace_id}/user/{user_id}/time-entries'
        get_data = self.send_get_request(endpoint)

        if len(sys.argv) != 3:
            print("Invalid number of arguments. Please provide two dates as arguments")
            return
        date_from = sys.argv[1]
        date_to = sys.argv[2]

        if not self.validate_date_format(date_from, date_to):
            print("Invalid date format. Please provide dates in the format 'YYYY-MM-DD'. ")
            return

        for data in get_data:
            create_date = data['timeInterval']['start'][:10]
            duration = data['timeInterval']['duration']
            name = data['description']
            if name == "":
                name = "In progres..."

            if data['userId'] == self.get_user_id() and date_from <= create_date <= date_to:
                member_name = self.get_name()

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
            return formatted_duration


    def send_get_request(self, endpoint):
        headers = {
            'X-Api-Key': self.API_KEY,
            'Content-Type': 'application/json'
        }
        url = self.BASE_URL + endpoint
        response = requests.get(url, headers=headers)
        data = response.json()

        return data

    def get_user_id(self):
        endpoint = f'user'
        user_id = self.send_get_request(endpoint)

        return user_id['id']


    def get_name(self):
        endpoint = f'user'
        names = self.send_get_request(endpoint)
        return names['name']

    def validate_date_format(self, first_date, second_date):
        try:
            first_date = datetime.datetime.strptime(first_date, '%Y-%m-%d')
            second_date = datetime.datetime.strptime(second_date, '%Y-%m-%d')
            if first_date > second_date:
                print("First date can't be greater than second one.")
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

raport = ClockifyApp()
raport.generate_raport()
