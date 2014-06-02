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
subparsers = parser.add_subparsers(title="Tutum's CLI commands", dest='cmd')


# Command Parsers
parsers.add_apps_parser(subparsers)
parsers.add_build_parser(subparsers)
parsers.add_containers_parser(subparsers)
parsers.add_images_parser(subparsers)
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
    if args.cmd == 'login':
        commands.login()
    if args.cmd == 'build':
        commands.build(args.tag, args.directory, args.quiet, args.no_cache)
    elif args.cmd == 'app':
        if args.subcmd == 'alias':
            commands.apps_alias(args.identifier, args.dns)
        elif args.subcmd == 'inspect':
            commands.apps_inspect(args.identifier)
        elif args.subcmd == 'logs':
            commands.apps_logs(args.identifier)
        elif args.subcmd == 'open':
            commands.apps_open()
        elif args.subcmd == 'ps':
            commands.apps_ps(args.quiet, args.status)
        elif args.subcmd == 'redeploy':
            commands.apps_redeploy(args.identifier, args.tag)
        elif args.subcmd == 'run':
            commands.apps_run(image=args.image, name=args.name, container_size=args.container_size,
                              target_num_containers=args.target_num_containers, run_command=args.run_command,
                              entrypoint=args.entrypoint, container_ports=args.port, container_envvars=args.env,
                              links=args.link, autorestart=args.autorestart,
                              autoreplace=args.autoreplace, autodestroy=args.autodestroy, roles=args.role,
                              sequential=args.sequential)
        elif args.subcmd == 'scale':
            commands.apps_scale(args.identifier, args.target_num_containers)
        elif args.subcmd == 'set':
            commands.apps_set(args.autorestart, args.autoreplace, args.autodestroy, args.identifier)
        elif args.subcmd == 'start':
            commands.apps_start(args.identifier)
        elif args.subcmd == 'stop':
            commands.apps_stop(args.identifier)
        elif args.subcmd == 'terminate':
            commands.apps_terminate(args.identifier)
    elif args.cmd == 'container':
        if args.subcmd == 'inspect':
            commands.containers_inspect(args.identifier)
        elif args.subcmd == 'logs':
            commands.containers_logs(args.identifier)
        elif args.subcmd == 'ps':
            commands.containers_ps(args.identifier, args.quiet, args.status)
        elif args.subcmd == 'start':
            commands.containers_start(args.identifier)
        elif args.subcmd == 'stop':
            commands.containers_stop(args.identifier)
        elif args.subcmd == 'terminate':
            commands.containers_terminate(args.identifier)
    elif args.cmd == 'image':
        if args.subcmd == 'list':
            commands.images_list(args.quiet, args.jumpstarts, args.linux)
        elif args.subcmd == 'register':
            commands.images_register(args.image_name, args.description)
        elif args.subcmd == 'push':
            commands.images_push(args.name, args.public)
        elif args.subcmd == 'rm':
            commands.images_rm(args.image_name)
        elif args.subcmd == 'search':
            commands.images_search(args.query)
        elif args.subcmd == 'update':
            commands.images_update(args.image_name, args.username, args.password, args.description)


if __name__ == '__main__':
    main()