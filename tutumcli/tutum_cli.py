import argparse
import logging
import sys
import codecs

from tutumcli import parsers
from tutumcli import commands


VERSION = "0.7.2"

sys.stdout = codecs.getwriter('utf8')(sys.stdout)


logging.basicConfig()

# Main parser
parser = argparse.ArgumentParser(description="Tutum's CLI", prog="tutum")
parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + VERSION)

subparsers = parser.add_subparsers(title="Tutum's CLI commands", dest='command')

# Common options
parent_parser = argparse.ArgumentParser(add_help=False)

# Commands
parsers.add_login_parser(subparsers, parent_parser)
parsers.add_register_parser(subparsers, parent_parser)
parsers.add_search_parser(subparsers, parent_parser)
parsers.add_apps_and_containers_parser(subparsers, parent_parser)
parsers.add_images_parser(subparsers, parent_parser)


def main():
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    # Parse args
    args = parser.parse_args()
    if args.command == "login":
        commands.authenticate()
    elif args.command == "register":
        commands.register()
    elif args.command == "search":
        commands.search(args.text)
    elif args.command == "apps":
        commands.apps(args.quiet, args.status)
    elif args.command == "inspect":
        commands.details(args.identifier)
    elif args.command == "start":
        commands.start(args.identifier)
    elif args.command == "stop":
        commands.stop(args.identifier)
    elif args.command == "terminate":
        commands.terminate(args.identifier)
    elif args.command == "logs":
        commands.logs(args.identifier)
    elif args.command == "scale":
        commands.app_scale(args.identifier, args.target_num_containers)
    elif args.command == "alias":
        commands.app_alias(args.identifier, args.dns)
    elif args.command == "run":
        commands.app_run(image=args.image, name=args.name, container_size=args.container_size,
                         target_num_containers=args.target_num_containers, run_command=args.run_command,
                         entrypoint=args.entrypoint, container_ports=args.port,
                         container_envvars=args.env,
                         linked_to_application=args.link, autorestart=args.autorestart,
                         autoreplace=args.autoreplace, autodestroy=args.autodestroy, roles=args.role)
    elif args.command == "ps":
            commands.ps(args.identifier, args.quiet, args.status)
    elif args.command == "images":
        commands.images(args.quiet, args.jumpstarts, args.linux)
    elif args.command == "add":
        commands.add_image(args.repository, args.username, args.password, args.description)
    elif args.command == "remove":
        commands.remove_image(args.repository)
    elif args.command == "update":
        commands.update_image(args.repository, args.username, args.password, args.description)

if __name__ == "__main__":
    main()