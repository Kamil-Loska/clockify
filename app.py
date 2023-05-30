from ClockifyReportGenerator import ClockifyReportGenerator
from Argument_provider import ArgumentProvider


def main():
    args = ArgumentProvider().argument_parser()
    clockify = ClockifyReportGenerator()
    clockify.generate_report(args.date_from, args.date_to)


if __name__ == '__main__':
    main()
