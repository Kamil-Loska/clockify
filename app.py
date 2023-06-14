from ClockifyReportGenerator import ClockifyReportGenerator
from Argument_provider import ArgumentProvider
from ConfigFileHandler import ConfigFileHandler
from UsersFileHandler import UserHandler
from ClockifyAPI import ClockifyAPI
from ReportWriterFactory import ReportWriterFactory
from CompositeReportWriter import ReportComposite
from ConsoleReportWriter import ConsoleReportWriter
from CsvReportWriter import CsvReportWriter
from XmlReportWriter import XmlReportWriter


def main():

    argument_provider = ArgumentProvider()
    args = argument_provider.get_arguments()
    config_file_handler = ConfigFileHandler('config.ini')
    user_file_handler = UserHandler('Users.csv')
    factory = ReportWriterFactory(config_file_handler)
    clockify_api = ClockifyAPI(config_file_handler.get_workspace_id())
    users = user_file_handler.load_user_credentials_from_file()
    clockify_generator = ClockifyReportGenerator(config_file_handler, clockify_api)

    composite_writer = ReportComposite()
    composite_writer.add_component(ConsoleReportWriter())
    composite_writer.add_component(CsvReportWriter(config_file_handler))
    composite_writer.add_component(XmlReportWriter())

    all_report_entries = []
    for user in users:
        report_entries = clockify_generator.generate_report(user, args.date_from, args.date_to)
        all_report_entries.extend(report_entries)

    report_writer = factory.create_report_writer(args.output_format)
    report_writer.write(all_report_entries)


if __name__ == "__main__":
    main()
