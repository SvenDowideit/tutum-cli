import argparse
import logging
import sys
import codecs

from . import __version__
from tutumcli import parsers
from tutumcli import commands


sys.stdout = codecs.getwriter('utf8')(sys.stdout)

logging.basicConfig()

# Top parser
parser = argparse.ArgumentParser(description="Tutum's CLI", prog='tutum')
parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
parser.add_argument('--debug', action='store_true', help=argparse.SUPPRESS)
subparsers = parser.add_subparsers(title="Tutum's CLI commands", dest='cmd')


# Command Parsers
parsers.add_app_parser(subparsers)
parsers.add_build_parser(subparsers)
parsers.add_container_parser(subparsers)
parsers.add_image_parser(subparsers)
parsers.add_login_parser(subparsers)


def main():
    if len(sys.argv) == 1:
        sys.argv.append('-h')
    elif len(sys.argv) == 2 and sys.argv[1] in ['app', 'build', 'container', 'image', ]:
        sys.argv.append('-h')
    elif len(sys.argv) == 3:
        if sys.argv[1] == 'app' and sys.argv[2] in ['alias', 'inspect', 'logs', 'redeploy', 'run', 'scale', 'set',
                                                    'start', 'stop', 'terminate']:
            sys.argv.append('-h')
        elif sys.argv[1] == 'container' and sys.argv[2] in ['inspect', 'logs', 'start', 'stop', 'terminate']:
            sys.argv.append('-h')
        elif sys.argv[1] == 'image' and sys.argv[2] in ['register', 'push', 'rm', 'search', 'update']:
            sys.argv.append('-h')

    # dispatch commands
    args = parser.parse_args()
    if args.debug:
        requests_log = logging.getLogger("python-tutum")
        requests_log.setLevel(logging.INFO)
    if args.cmd == 'login':
        commands.login()
    if args.cmd == 'build':
        commands.build(args.tag, args.directory, args.quiet, args.no_cache)
    elif args.cmd == 'app':
        if args.subcmd == 'alias':
            commands.app_alias(args.identifier, args.dns)
        elif args.subcmd == 'inspect':
            commands.app_inspect(args.identifier)
        elif args.subcmd == 'logs':
            commands.app_logs(args.identifier)
        elif args.subcmd == 'open':
            commands.app_open()
        elif args.subcmd == 'ps':
            commands.app_ps(args.quiet, args.status)
        elif args.subcmd == 'redeploy':
            commands.app_redeploy(args.identifier, args.tag)
        elif args.subcmd == 'run':
            commands.app_run(image=args.image, name=args.name, container_size=args.container_size,
                              target_num_containers=args.target_num_containers, run_command=args.run_command,
                              entrypoint=args.entrypoint, container_ports=args.port, container_envvars=args.env,
                              links=args.link, autorestart=args.autorestart,
                              autoreplace=args.autoreplace, autodestroy=args.autodestroy, roles=args.role,
                              sequential=args.sequential)
        elif args.subcmd == 'scale':
            commands.app_scale(args.identifier, args.target_num_containers)
        elif args.subcmd == 'set':
            commands.app_set(args.autorestart, args.autoreplace, args.autodestroy, args.identifier)
        elif args.subcmd == 'start':
            commands.app_start(args.identifier)
        elif args.subcmd == 'stop':
            commands.app_stop(args.identifier)
        elif args.subcmd == 'terminate':
            commands.app_terminate(args.identifier)
    elif args.cmd == 'container':
        if args.subcmd == 'inspect':
            commands.container_inspect(args.identifier)
        elif args.subcmd == 'logs':
            commands.container_logs(args.identifier)
        elif args.subcmd == 'ps':
            commands.container_ps(args.identifier, args.quiet, args.status)
        elif args.subcmd == 'start':
            commands.container_start(args.identifier)
        elif args.subcmd == 'stop':
            commands.container_stop(args.identifier)
        elif args.subcmd == 'terminate':
            commands.container_terminate(args.identifier)
    elif args.cmd == 'image':
        if args.subcmd == 'list':
            commands.image_list(args.quiet, args.jumpstarts, args.linux)
        elif args.subcmd == 'register':
            commands.image_register(args.image_name, args.description)
        elif args.subcmd == 'push':
            commands.image_push(args.name, args.public)
        elif args.subcmd == 'rm':
            commands.image_rm(args.image_name)
        elif args.subcmd == 'search':
            commands.image_search(args.query)
        elif args.subcmd == 'update':
            commands.image_update(args.image_name, args.username, args.password, args.description)


if __name__ == '__main__':
    main()