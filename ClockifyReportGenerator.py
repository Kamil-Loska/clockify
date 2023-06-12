import csv
from xml.dom import minidom

from ReportComposite import ReportComposite
from ReportLeaf import ReportLeaf


class ClockifyReportGenerator:
    def __init__(self, config_handler, clockify_api):
        self.config_handler = config_handler
        self.clockify_api = clockify_api

    def generate_report(self, user_credentials, date_from, date_to, format):
        time_entries = self.clockify_api.get_time_entries_per_user(user_credentials, date_from, date_to)
        user_name = self.clockify_api.get_user_name(user_credentials)

        report_entries = ReportComposite()
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

                leaf = ReportLeaf(report_data)
                report_entries.add_component(leaf)

        if format == 'csv':
            return self.generate_csv_report(report_entries.generate_report())
        elif format == 'xml':
            return self.generate_xml_report(report_entries.generate_report())
        else:
            return self.generate_console_report(report_entries.generate_report())

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

    def generate_csv_report(self, report_entries):
        filename = 'report.csv'

        with open(filename, 'w', newline='', encoding='UTF8') as csvfile:
            fieldnames = list(report_entries[0].keys())

            translated_fieldnames = [self.config_handler.translation_mapper().get(fieldname, fieldname)
                                     for fieldname in fieldnames]

            writer = csv.DictWriter(csvfile, fieldnames=translated_fieldnames)

            for report_data in report_entries:
                translated_data = {translated_fieldnames[i]: value for i, (key, value) in
                                   enumerate(report_data.items())}
                writer.writerow(translated_data)

        print(csvfile.name)

    def generate_xml_report(self, report_entries):
        root = minidom.Document()
        xml = root.createElement('root')
        root.appendChild(xml)
        for report_data in report_entries:
            productChild = root.createElement('ClockifyReport')
            productChild.setAttribute('Fullname', f'{report_data["Fullname"]}')
            productChild.setAttribute('Date', f'{report_data["Date"]}')
            productChild.setAttribute('Duration-time', f'{report_data["Duration-time"]}')
            productChild.setAttribute('Task-description', f'{report_data["Task-description"]}')
            xml.appendChild(productChild)

        xml_str = root.toprettyxml(indent='\t')
        save_to_file = 'report.xml'
        with open(save_to_file, 'w') as xmlFile:
            xmlFile.write(xml_str)
        print(xmlFile.name)

    def generate_console_report(self, report_entries):
        for report_data in report_entries:
            print(report_data)
