import Argument_provider
from ClockifyAPI import ClockifyAPI
from FileHandler import FileHandler
from Argument_provider import ArgumentProvider
import csv
import os


class ClockifyReportGenerator:

    def __init__(self):
        self.file_handler = FileHandler()
        self.clockify_api = ClockifyAPI()
        self.argument_provider = ArgumentProvider()

    def generate_report(self, date_from, date_to):
        self.argument_provider.validate_date_format(date_from, date_to)

        users = self.file_handler.get_users_from_file()
        for user_id, api_key in users.items():
            self.clockify_api.API_KEY = api_key
            self.clockify_api.USER_ID = user_id

            get_data = self.clockify_api.get_time_entries_per_user(date_from, date_to)
            get_user_id, get_user_name = self.clockify_api.get_user_data()

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

                    report_date = {self.file_handler.translation_mapper().get(key, key): value for key, value in
                                   report_data.items()}

                    print(report_date)

    def format_duration(self, duration):
        if duration is not None:
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
            fieldnames = list(self.file_handler.translation_mapper().values())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if is_empty:
                writer.writeheader()

            report_data_en = {self.file_handler.translation_mapper().get(key, key): value for key, value in
                              report_data.items()}
            writer.writerow(report_data_en)

        with open(filename, 'r') as csvfile:
            if csvfile.read().strip() == '':
                print(filename)
                return
