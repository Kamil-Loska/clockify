from ClockifyReportGenerator import ClockifyReportGenerator
from Argument_provider import ArgumentProvider
from ConfigFileHandler import ConfigFileHandler
from UsersFileHandler import UserHandler


def main():
    argument_provider = ArgumentProvider()
    args = argument_provider.arguments_provider()

    config_file_handler = ConfigFileHandler('config.ini')
    user_file_handler = UserHandler('Users.csv')

    clockify = ClockifyReportGenerator(config_file_handler, user_file_handler)
    clockify.generate_report(args.date_from, args.date_to)


if __name__ == '__main__':
    main()
