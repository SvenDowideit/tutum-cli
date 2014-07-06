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
parsers.add_cluster_parser(subparsers)
parsers.add_build_parser(subparsers)
parsers.add_container_parser(subparsers)
parsers.add_image_parser(subparsers)
parsers.add_login_parser(subparsers)


def main():
    if len(sys.argv) == 1:
        sys.argv.append('-h')
    elif len(sys.argv) == 2 and sys.argv[1] in ['cluster', 'build', 'container', 'image', ]:
        sys.argv.append('-h')
    elif len(sys.argv) == 3:
        if sys.argv[1] == 'cluster' and sys.argv[2] in ['alias', 'inspect', 'logs', 'redeploy', 'run', 'scale', 'set',
                                                    'start', 'stop', 'terminate']:
            sys.argv.append('-h')
        elif sys.argv[1] == 'container' and sys.argv[2] in ['inspect', 'logs', 'redeploy', 'run', 'start', 'stop',
                                                            'terminate']:
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
    elif args.cmd == 'cluster':
        if args.subcmd == 'alias':
            commands.cluster_alias(args.identifier, args.dns)
        elif args.subcmd == 'inspect':
            commands.cluster_inspect(args.identifier)
        elif args.subcmd == 'logs':
            commands.cluster_logs(args.identifier)
        elif args.subcmd == 'open':
            commands.cluster_open()
        elif args.subcmd == 'ps':
            commands.cluster_ps(args.quiet, args.status)
        elif args.subcmd == 'redeploy':
            commands.cluster_redeploy(args.identifier, args.tag)
        elif args.subcmd == 'run':
            commands.cluster_run(image=args.image, name=args.name, container_size=args.container_size,
                             target_num_containers=args.target_num_containers, run_command=args.run_command,
                             entrypoint=args.entrypoint, container_ports=args.port, container_envvars=args.env,
                             linked_to_cluster=args.link_cluster, linked_to_container=args.link_container,
                             autorestart=args.autorestart,
                             autoreplace=args.autoreplace, autodestroy=args.autodestroy, roles=args.role,
                             sequential=args.sequential, web_public_dns=args.web_public_dns)
        elif args.subcmd == 'scale':
            commands.cluster_scale(args.identifier, args.target_num_containers)
        elif args.subcmd == 'set':
            commands.cluster_set(args.autorestart, args.autoreplace, args.autodestroy, args.identifier)
        elif args.subcmd == 'start':
            commands.cluster_start(args.identifier)
        elif args.subcmd == 'stop':
            commands.cluster_stop(args.identifier)
        elif args.subcmd == 'terminate':
            commands.cluster_terminate(args.identifier)
    elif args.cmd == 'container':
        if args.subcmd == 'inspect':
            commands.container_inspect(args.identifier)
        elif args.subcmd == 'logs':
            commands.container_logs(args.identifier)
        elif args.subcmd == 'ps':
            commands.container_ps(args.identifier, args.quiet, args.status)
        elif args.subcmd == 'redeploy':
            commands.container_redeploy(args.identifier, args.tag)
        elif args.subcmd == 'run':
            commands.container_run(image=args.image, name=args.name, container_size=args.container_size,
                             run_command=args.run_command, entrypoint=args.entrypoint, container_ports=args.port,
                             container_envvars=args.env,
                             linked_to_cluster=args.link_cluster, linked_to_container=args.link_container,
                             autorestart=args.autorestart,autoreplace=args.autoreplace, autodestroy=args.autodestroy,
                             roles=args.role, web_public_dns=args.web_public_dns)
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