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
    api_key, user_id = user_file_handler.load_user_credentials_from_file()
    clockify_api = ClockifyAPI(config_file_handler.get_workspace_id())
    clockify = ClockifyReportGenerator(config_file_handler, api_key, user_id, clockify_api)

    clockify.generate_report(args.date_from, args.date_to)


if __name__ == '__main__':
    main()
