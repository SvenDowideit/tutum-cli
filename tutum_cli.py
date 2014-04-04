import argparse
import tutum
import logging

import commands


TEST_BASE_URL = "https://app-test.tutum.co/api/v1/"


if __name__ == "__main__":
    tutum.base_url = TEST_BASE_URL
    logging.basicConfig()

    # Main parser
    parser = argparse.ArgumentParser(description="Tutum's CLI")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.6.3.4')

    subparsers = parser.add_subparsers(title="Tutum's CLI commands", dest='command')

    # Common options
    parent_parser = argparse.ArgumentParser(add_help=False)

    # Commands
    login_parser = subparsers.add_parser('login', help='Login into Tutum', parents=[parent_parser])

    apps_parser = subparsers.add_parser('apps', help='List all applications', parents=[parent_parser])

    app_parser = subparsers.add_parser('app', help='Get application details', parents=[parent_parser])
    app_subparsers = app_parser.add_subparsers(title="App commands", dest='app_command')
    inspect_app_parser = app_subparsers.add_parser('inspect', help='Inspect an application', parents=[parent_parser])
    start_app_parser = app_subparsers.add_parser('start', help='Start an application', parents=[parent_parser])
    stop_app_parser = app_subparsers.add_parser('stop', help='Stop an application', parents=[parent_parser])
    terminate_app_parser = app_subparsers.add_parser('terminate', help='Terminate an application', parents=[parent_parser])
    update_app_parser = app_subparsers.add_parser('update', help='Update an application', parents=[parent_parser])
    app_parser.add_argument("identifier", help="Application's uuid (either long or short) or name")
    update_app_parser.add_argument("--target_num_containers", help="target number of containers to scale this application to", type=int)
    update_app_parser.add_argument("--web_public_dns", help="custom domain to use for this web application")


    # Parse args
    args = parser.parse_args()
    if args.command == "login":
        commands.authenticate()
    elif args.command == "apps":
        commands.apps()
    elif args.command == "app":
        if args.app_command == "inspect":
            commands.app_details(args.identifier)
        elif args.app_command == "start":
            commands.app_start(args.identifier)
        elif args.app_command == "stop":
            commands.app_stop(args.identifier)
        elif args.app_command == "terminate":
            commands.app_terminate(args.identifier)
        elif args.app_command == "update":
            commands.app_update(args.identifier, args.target_num_containers, args.web_public_dns)