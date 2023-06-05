import csv
import os


class ClockifyReportGenerator:
    def __init__(self, config_handler, api_key):
        self.config_handler = config_handler
        self.api_key = api_key

    def generate_report(self, user_name, time_entries, date_from, date_to):

        for data in time_entries:
            create_date = data['timeInterval']['start'][:10]
            duration = data['timeInterval']['duration']
            description = data['description']
            if description == "":
                description = "In progress..."

            if date_from <= create_date <= date_to:

                report_data = {
                    'Fullname': "-".join(user_name.split(" ")[::-1]),
                    'Date': create_date,
                    'Duration-time': self.format_duration(duration),
                    'Task-description': description,
                }

                report_date = {self.config_handler.translation_mapper().get(key, key): value for key, value in
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
