import argparse
import tutum

import commands


TEST_BASE_URL = "https://app-test.tutum.co/api/v1/"


if __name__ == "__main__":
    tutum.base_url = TEST_BASE_URL

    # Main parser
    parser = argparse.ArgumentParser(description="Tutum's CLI")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.6.3.4')

    subparsers = parser.add_subparsers(title="Tutum's CLI commands", help="commands", dest='command')

    # Common options
    parent_parser = argparse.ArgumentParser(add_help=False)

    # Commands
    login_parser = subparsers.add_parser('login', help='Login into Tutum', parents=[parent_parser])

    apps_parser = subparsers.add_parser('apps', help='List all applications', parents=[parent_parser])

    app_parser = subparsers.add_parser('app', help='Get application details', parents=[parent_parser])
    app_parser.add_argument("uuid", help="Application's uuid")

    # Parse args
    args = parser.parse_args()
    if args.command == "login":
        commands.authenticate()
    elif args.command == "apps":
        commands.apps()
    elif args.command == "app":
        commands.app_details(args.uuid)