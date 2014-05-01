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


# Commands
parsers.add_apps_parser(subparsers)
parsers.add_containers_parser(subparsers)
parsers.add_images_parser(subparsers)
parsers.add_login_parser(subparsers)


def main():
    if len(sys.argv) == 1:
        sys.argv.append('-h')
    elif len(sys.argv) == 2 and sys.argv[1] in ['apps', 'containers', 'images']:
        sys.argv.append('-h')
    elif len(sys.argv) == 3:
        if sys.argv[1] == 'apps' and sys.argv[2] in ['alias', 'inspect', 'logs', 'redeploy', 'run', 'scale', 'set',
                                                     'start', 'stop', 'terminate']:
            sys.argv.append('-h')
        elif sys.argv[1] == 'containers' and sys.argv[2] in ['inspect', 'logs', 'start', 'stop', 'terminate']:
            sys.argv.append('-h')
        elif sys.argv[1] == 'images' and sys.argv[2] in ['build', 'register', 'push', 'rm', 'search', 'update']:
            sys.argv.append('-h')


    # dispatch commands
    args = parser.parse_args()
    if args.cmd == 'login':
        commands.authenticate()
    elif args.cmd == 'apps':
        if args.subcmd == 'alias':
            commands.apps_alias(args.identifier, args.dns)
        elif args.subcmd == 'inspect':
            commands.inspect(args.identifier)
        elif args.subcmd == 'logs':
            commands.logs(args.identifier)
        elif args.subcmd == 'open':
            commands.apps_open()
        elif args.subcmd == 'ps':
            commands.apps_ps(args.quiet, args.status, args.remote, args.local)
        elif args.subcmd == 'redeploy':
            commands.apps_redeploy(args.identifier, args.tag)
        elif args.subcmd == 'run':
            commands.apps_run(image=args.image, name=args.name, container_size=args.container_size,
                             target_num_containers=args.target_num_containers, run_command=args.run_command,
                             entrypoint=args.entrypoint, container_ports=args.port,
                             container_envvars=args.env,
                             linked_to_applications=args.link, autorestart=args.autorestart,
                             autoreplace=args.autoreplace, autodestroy=args.autodestroy, roles=args.role,
                             local=args.local,
                             parallel=args.parallel)
        elif args.subcmd == 'scale':
            commands.apps_scale(args.identifier, args.target_num_containers)
        elif args.subcmd == 'set':
            commands.apps_set(args.autorestart, args.autoreplace, args.autodestroy, args.identifier)
        elif args.subcmd == 'start':
            commands.start(args.identifier)
        elif args.subcmd == 'stop':
            commands.stop(args.identifier)
        elif args.subcmd == 'terminate':
            commands.terminate(args.identifier)
    elif args.cmd == 'containers':
        if args.subcmd == 'inspect':
            commands.inspect(args.identifier)
        elif args.subcmd == 'logs':
            commands.logs(args.identifier)
        elif args.subcmd == 'ps':
            commands.ps(args.identifier, args.quiet, args.status, args.remote, args.local)
        elif args.subcmd == 'start':
            commands.start(args.identifier)
        elif args.subcmd == 'stop':
            commands.stop(args.identifier)
        elif args.subcmd == 'terminate':
            commands.terminate(args.identifier)
    elif args.cmd == 'images':
        if args.subcmd == 'build':
            commands.images_build(args.name, args.directory, args.quiet, args.nocache)
        elif args.subcmd == 'list':
            commands.images_list(args.quiet, args.jumpstarts, args.linux, args.local, args.remote)
        elif args.subcmd == 'register':
            commands.images_register(args.repository, args.username, args.password, args.description)
        elif args.subcmd == 'push':
            commands.images_push(args.name, args.public)
        elif args.subcmd == 'rm':
            commands.images_remove(args.repository)
        elif args.subcmd == 'search':
            commands.images_search(args.text)
        elif args.subcmd == 'update':
            commands.images_update(args.repository, args.username, args.password, args.description)


if __name__ == '__main__':
    main()
