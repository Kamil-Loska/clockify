from ClockifyAPI import ClockifyAPI


class ClockifyReportGenerator:
    def __init__(self, clockify_api: ClockifyAPI):
        self.clockify_api = clockify_api

    def generate_report(self, users: list[dict[str, str]], date_from: str, date_to: str) -> list[dict[str, str]]:
        report_entries = []
        for user_credentials in users:
            time_entries = self.clockify_api.get_time_entries_per_user(user_credentials, date_from, date_to)
            user_name = self.clockify_api.get_user_name(user_credentials)
            for data in time_entries:
                create_date = data['timeInterval']['start'][:10]
                duration = data['timeInterval']['duration']
                description = data['description']
                if description == "":
                    description = "In progress..."
                report_data = {
                    'fullName': user_name,
                    'date': create_date,
                    'durationTime': self.format_duration(duration),
                    'taskDescription': description,
                }
                report_entries.append(report_data)
        return report_entries

    def format_duration(self, duration: str) -> str:
        if duration is not None:
            duration = duration[2:]
            hours, minutes, seconds = 0, 0, 0

            if "H" in duration:
                hours, duration = duration.split("H")
            if "M" in duration:
                minutes, duration = duration.split("M")
            if "S" in duration:
                seconds, _ = duration.split("S")

            formatted_duration = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
            return formatted_duration.strip()
