import requests
import datetime
import sys
import csv
import os

class ClockifyApp:

    def __init__(self):
        self.API_KEY = 'API_KEY'
        self.BASE_URL = 'https://api.clockify.me/api/v1/'


    def get_time_entries_per_user(self, start_date, end_date):
        workspace_id = 'WORKSPACE_ID'
        user_id = 'USER_ID'
        endpoint = f'workspaces/{workspace_id}/user/{user_id}/time-entries?start={start_date}T00:00:00Z&end={end_date}T23:59:59Z'
        users_data = self.send_get_request(endpoint)

        return users_data

    def generate_raport(self):
        if len(sys.argv) != 3:
            print("Invalid number of arguments. Please provide two dates as arguments")
            return
        date_from = sys.argv[1]
        date_to = sys.argv[2]

        get_data = self.get_time_entries_per_user(date_from, date_to)
        get_user_id, get_name_user = self.get_user_data()

        if not self.validate_date_format(date_from, date_to):
            print("Invalid date format. Please provide dates in the format 'YYYY-MM-DD'. ")
            return

        for data in get_data:
            create_date = data['timeInterval']['start'][:10]
            duration = data['timeInterval']['duration']
            name = data['description']
            if name == "":
                name = "In progres..."

            if data['userId'] == get_user_id and date_from <= create_date <= date_to:
                member_name = get_name_user

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


    def send_get_request(self, endpoint):
        headers = {
            'X-Api-Key': self.API_KEY,
            'Content-Type': 'application/json'
        }
        url = self.BASE_URL + endpoint
        response = requests.get(url, headers=headers)
        data = response.json()

        return data


    def get_user_data(self):
        endpoint = f'user'
        get_user_data = self.send_get_request(endpoint)

        return get_user_data['id'], get_user_data['name']

    def validate_date_format(self, first_date, second_date):
        try:
            first_date = datetime.datetime.strptime(first_date, '%Y-%m-%d')
            second_date = datetime.datetime.strptime(second_date, '%Y-%m-%d')

            if first_date > second_date:
                print("First date can't be greater than second one.")
                return False
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
