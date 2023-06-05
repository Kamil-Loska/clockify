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
    users = user_file_handler.load_user_credentials_from_file()
    clockify_api = ClockifyAPI(config_file_handler.get_workspace_id())

    for api_key, user_id in users:
        user_name = clockify_api.get_user_name(api_key)
        time_entries = clockify_api.get_time_entries_per_user(api_key, user_id, args.date_from, args.date_to)
        clockify = ClockifyReportGenerator(config_file_handler, api_key)
        clockify.generate_report(user_name, time_entries, args.date_from, args.date_to)


if __name__ == '__main__':
    main()
