from ClockifyReportGenerator import ClockifyReportGenerator
from argument_provider import ArgumentProvider
from ConfigFileHandler import ConfigFileHandler
from UsersFileHandler import UserHandler
from ClockifyAPI import ClockifyAPI
from ReportStrategyFactory import ReportStrategyFactory
from ReportGenerator import ReportGenerator
from ConsoleReportWriter import ConsoleReportWriter
from XmlReportWriter import XmlReportWriter
from CsvReportWriter import CsvReportWriter

def main():
    argument_provider = ArgumentProvider()
    args = argument_provider.get_arguments()
    config_file_handler = ConfigFileHandler('config.ini')
    user_file_handler = UserHandler('Users.csv')
    clockify_api = ClockifyAPI(config_file_handler.get_workspace_id())
    users = user_file_handler.load_user_credentials_from_file()
    clockify_generator = ClockifyReportGenerator(config_file_handler, clockify_api)
    report_entries = clockify_generator.generate_report(users, args.date_from, args.date_to)

    strategy_factory = ReportStrategyFactory(config_file_handler)

    strategy = strategy_factory.get_strategy(args.output_format)

    report_generator = ReportGenerator()

    report_generator.strategy = ReportGenerator(strategy)

    report_generator.write_report(report_entries)


if __name__ == "__main__":
    main()
