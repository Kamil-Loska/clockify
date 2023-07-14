from ClockifyReportGenerator import ClockifyReportGenerator
from argument_provider import ArgumentProvider
from ConfigFileHandler import ConfigFileHandler
from FieldMapper import FieldMapper
from UsersFileHandler import UserHandler
from ClockifyAPI import ClockifyAPI
from ReportStrategyFactory import ReportStrategyFactory
from ReportGenerator import ReportGenerator


def main():
    config_file_handler = ConfigFileHandler('config.ini')
    user_file_handler = UserHandler('Users.csv')

    clockify_api = ClockifyAPI(config_file_handler.get_workspace_id())
    users = user_file_handler.load_user_credentials_from_file()
    argument_provider = ArgumentProvider()
    args = argument_provider.get_arguments()
    field_mapper = FieldMapper(config_file_handler)
    strategy_factory = ReportStrategyFactory(field_mapper)
    strategy = strategy_factory.get_strategy(args.output_format)
    clockify_generator = ClockifyReportGenerator(clockify_api)

    report_entries = clockify_generator.generate_report(users, args.date_from, args.date_to)
    report_generator = ReportGenerator(strategy)
    report_generator.write_report(report_entries)


if __name__ == "__main__":
    main()
