from ClockifyAPI import ClockifyAPI
import csv
import os
from Argument_provider import ArgumentProvider
from FileHandler import FileHandler


class ClockifyReportGenerator:

    def generate_report(self, date_from, date_to):

        file_handler = FileHandler('config.ini')
        workspace_id = file_handler.config['Clockify'].get('WORKSPACE_ID')
        users = file_handler.get_users_from_file()

        for user_id, api_key in users.items():
            clockify_api = ClockifyAPI(workspace_id, api_key, user_id)
            time_entries = clockify_api.get_time_entries_per_user(date_from, date_to)
            user_name = clockify_api.get_user_name()

            for data in time_entries:
                create_date = data['timeInterval']['start'][:10]
                duration = data['timeInterval']['duration']
                description_name = data['description']
                if description_name == "":
                    description_name = "In progress..."

                if data['userId'] == user_id and date_from <= create_date <= date_to:

                    report_data = {
                        'Fullname': " ".join(user_name.split(" ")[::-1]),
                        'Date': create_date,
                        'Duration time': self.format_duration(duration),
                        'Task description': description_name,
                    }

                    report_date = {file_handler.translation_mapper().get(key, key): value for key, value in
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

    def create_report(self, report_data, file_handler):
        filename = 'report.csv'

        is_empty = os.stat(filename).st_size == 0
        if not is_empty:
            with open(filename, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row == report_data:
                        return

        with open(filename, 'a', newline='') as csvfile:
            fieldnames = list(file_handler.translation_mapper().values())
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if is_empty:
                writer.writeheader()

            report_data_en = {file_handler.translation_mapper().get(key, key): value for key, value in
                              report_data.items()}
            writer.writerow(report_data_en)

        with open(filename, 'r') as csvfile:
            if csvfile.read().strip() == '':
                print(filename)
                return
