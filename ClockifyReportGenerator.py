
class ClockifyReportGenerator:
    def __init__(self, config_handler, clockify_api):
        self.config_handler = config_handler
        self.clockify_api = clockify_api

    def generate_report(self, user_credentials, date_from, date_to):
        time_entries = self.clockify_api.get_time_entries_per_user(user_credentials, date_from, date_to)
        user_name = self.clockify_api.get_user_name(user_credentials)

        report_entries = []
        for data in time_entries:
            create_date = data['timeInterval']['start'][:10]
            duration = data['timeInterval']['duration']
            description = data['description']
            if description == "":
                description = "In progress..."
            if date_from <= date_to:
                report_data = {
                    'Fullname': user_name,
                    'Date': create_date,
                    'Duration-time': self.format_duration(duration),
                    'Task-description': description,
                }

                report_entries.append(report_data)

        return report_entries

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
