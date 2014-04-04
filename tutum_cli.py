import argparse
import tutum
import logging
import parsers

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
    parsers.add_login_parser(subparsers, parent_parser)
    parsers.add_apps_parser(subparsers, parent_parser)
    parsers.add_app_parser(subparsers, parent_parser)


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
        elif args.app_command == "create":
            commands.app_create(image=args.image, name=args.name, container_size=args.container_size,
                                target_num_containers=args.target_num_containers, run_command=args.run_command,
                                entrypoint=args.entrypoint, container_ports=args.container_ports,
                                container_envvars=args.container_envvars,
                                linked_to_application=args.linked_to_application, autorestart=args.autorestart,
                                autoreplace=args.autoreplace, autodestroy=args.autodestroy, roles=args.roles)