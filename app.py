from ClockifyReportGenerator import ClockifyReportGenerator
from Argument_provider import ArgumentProvider
from ConfigFileHandler import ConfigFileHandler
from UsersFileHandler import UserHandler
from ClockifyAPI import ClockifyAPI


def main():
    argument_provider = ArgumentProvider()
    args = argument_provider.get_arguments()

    config_file_handler = ConfigFileHandler('config.ini')
    user_file_handler = UserHandler('Users.csv')
    clockify_api = ClockifyAPI(config_file_handler.get_workspace_id())
    users = user_file_handler.load_user_credentials_from_file()
    for api_key, user_id in users:
        clockify_generator = ClockifyReportGenerator(config_file_handler, api_key)
        report_entries = clockify_generator.generate_report(clockify_api, user_id, args.date_from, args.date_to)
        for report in report_entries:
            print(report)



if __name__ == '__main__':
    main()
