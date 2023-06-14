from ClockifyReportGenerator import ClockifyReportGenerator
from Argument_provider import ArgumentProvider
from ConfigFileHandler import ConfigFileHandler
from UsersFileHandler import UserHandler
from ClockifyAPI import ClockifyAPI
from ReportWriterFactory import ReportWriterFactory
from CompositeReportWriter import ReportComposite


def main():
    argument_provider = ArgumentProvider()
    args = argument_provider.get_arguments()
    config_file_handler = ConfigFileHandler('config.ini')
    user_file_handler = UserHandler('Users.csv')
    clockify_api = ClockifyAPI(config_file_handler.get_workspace_id())
    users = user_file_handler.load_user_credentials_from_file()
    clockify_generator = ClockifyReportGenerator(config_file_handler, clockify_api)
    report_entries = clockify_generator.generate_report(users, args.date_from, args.date_to)

    report_writer_factory = ReportWriterFactory(config_file_handler)

    composite_writer = ReportComposite()

    composite_writer.add_component(report_writer_factory.create_report_writer(args.output_format))

    composite_writer.write(report_entries)


if __name__ == "__main__":
    main()
