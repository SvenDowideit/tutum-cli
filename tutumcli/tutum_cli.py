import argparse
import logging
import copy
import sys
import codecs
import tutum
import requests
from . import __version__
from tutumcli import parsers
from tutumcli import commands
from tutumcli.exceptions import InternalError

requests.packages.urllib3.disable_warnings()

sys.stdout = codecs.getwriter('utf8')(sys.stdout)

logging.basicConfig()

tutum.user_agent = "tutum-cli/%s" % __version__


def initialize_parser():
    # Top parser
    parser = argparse.ArgumentParser(description="Tutum's CLI", prog='tutum')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)
    parser.add_argument('--debug', action='store_true', help=argparse.SUPPRESS)
    subparsers = parser.add_subparsers(title="Tutum's CLI commands", dest='cmd')
    # Command Parsers
    parsers.add_action_parser(subparsers)
    parsers.add_build_parser(subparsers)
    parsers.add_container_parser(subparsers)
    parsers.add_event_parser(subparsers)
    parsers.add_exec_parser(subparsers)
    parsers.add_image_parser(subparsers)
    parsers.add_login_parser(subparsers)
    parsers.add_node_parser(subparsers)
    parsers.add_nodecluster_parser(subparsers)
    parsers.add_push_parser(subparsers)
    parsers.add_run_parser(subparsers)
    parsers.add_service_parser(subparsers)
    parsers.add_stack_parser(subparsers)
    parsers.add_tag_parser(subparsers)
    parsers.add_volume_parser(subparsers)
    parsers.add_volumegroup_parser(subparsers)
    parsers.add_trigger_parser(subparsers)
    parsers.add_up_parser(subparsers)
    return parser


def patch_help_option(argv=sys.argv):
    args = copy.copy(argv)

    if not args:
        raise InternalError("Wrong argument is set, cannot be empty")
    debug = False
    if len(args) >= 2 and args[1] == '--debug':
        debug = True
        args.pop(1)

    if len(args) == 1:
        args.append('-h')
    elif len(args) == 2 and args[1] in ['action', 'service', 'build', 'container', 'image', 'exec', 'node',
                                        'nodecluster', 'tag', 'volume', 'volumegroup', 'trigger',
                                        'stack', 'push', 'run']:
        args.append('-h')
    elif len(args) == 3:
        if args[1] == 'action' and args[2] in ['inspect', 'logs', 'cancel', 'retry']:
            args.append('-h')
        elif args[1] == 'service' and args[2] in ['create', 'env', 'inspect', 'logs', 'redeploy', 'run', 'scale', 'set',
                                                  'start', 'stop', 'terminate']:
            args.append('-h')
        elif args[1] == 'container' and args[2] in ['exec', 'inspect', 'logs', 'redeploy', 'start', 'stop',
                                                    'terminate']:
            args.append('-h')
        elif args[1] == 'image' and args[2] in ['register', 'push', 'rm', 'search', 'tag', 'update', 'inspect']:
            args.append('-h')
        elif args[1] == 'node' and args[2] in ['inspect', 'rm', 'upgrade', 'healthcheck']:
            args.append('-h')
        elif args[1] == 'nodecluster' and args[2] in ['create', 'inspect', 'rm', 'scale', 'upgrade']:
            args.append('-h')
        elif args[1] == 'tag' and args[2] in ['add', 'list', 'rm', 'set']:
            args.append('-h')
        elif args[1] == 'trigger' and args[2] in ['create', 'list', 'rm']:
            args.append('-h')
        elif args[1] == 'volume' and args[2] in ['inspect']:
            args.append('-h')
        elif args[1] == 'volumegroup' and args[2] in ['inspect']:
            args.append('-h')
        elif args[1] == 'stack' and args[2] in ['inspect', 'redeploy', 'terminate', 'start', 'stop', 'update',
                                                'export']:
            args.append('-h')
    elif len(args) == 4:
        if args[1] == 'service' and args[2] == 'env':
            if args[3] in ['add', 'remove', 'update']:
                args.append('-h')
        if args[1] == 'image' and args[2] == 'tag':
            if args[3] in ['inspect', 'build']:
                args.append('-h')
    if debug:
        args.insert(1, '--debug')
    return args[1:]


def dispatch_cmds(args):
    if args.debug:
        requests_log = logging.getLogger("python-tutum")
        requests_log.setLevel(logging.INFO)
        cli_log = logging.getLogger("cli")
        cli_log.setLevel(logging.DEBUG)
    if args.cmd == 'login':
        commands.login(args.username, args.password)
    elif args.cmd == 'action':
        if args.subcmd == 'inspect':
            commands.action_inspect(args.identifier)
        elif args.subcmd == 'list':
            commands.action_list(args.quiet, args.last)
        elif args.subcmd == 'logs':
            commands.action_logs(args.identifier, args.tail, args.follow)
        elif args.subcmd == 'cancel':
            commands.action_cancel(args.identifier)
        elif args.subcmd == 'retry':
            commands.action_retry(args.identifier)
    elif args.cmd == 'build':
        commands.build(args.tag, args.directory, args.sock)
    elif args.cmd == 'event':
        commands.event()
    elif args.cmd == 'exec':
        commands.container_exec(args.identifier, args.command)
    elif args.cmd == 'push':
        commands.image_push(args.name, args.public)
    elif args.cmd == 'run':
        commands.service_run(image=args.image, name=args.name, cpu_shares=args.cpushares,
                             memory=args.memory, privileged=args.privileged,
                             target_num_containers=args.target_num_containers, run_command=args.run_command,
                             entrypoint=args.entrypoint, expose=args.expose, publish=args.publish, envvars=args.env,
                             envfiles=args.env_file,
                             tag=args.tag, linked_to_service=args.link_service,
                             autorestart=args.autorestart, autodestroy=args.autodestroy,
                             autoredeploy=args.autoredeploy, roles=args.role,
                             sequential=args.sequential, volume=args.volume, volumes_from=args.volumes_from,
                             deployment_strategy=args.deployment_strategy, sync=args.sync, net=args.net, pid=args.pid)
    elif args.cmd == 'service':
        if args.subcmd == 'create':
            commands.service_create(image=args.image, name=args.name, cpu_shares=args.cpushares,
                                    memory=args.memory, privileged=args.privileged,
                                    target_num_containers=args.target_num_containers, run_command=args.run_command,
                                    entrypoint=args.entrypoint, expose=args.expose, publish=args.publish,
                                    envvars=args.env, envfiles=args.env_file,
                                    tag=args.tag, linked_to_service=args.link_service,
                                    autorestart=args.autorestart, autodestroy=args.autodestroy,
                                    autoredeploy=args.autoredeploy, roles=args.role,
                                    sequential=args.sequential, volume=args.volume, volumes_from=args.volumes_from,
                                    deployment_strategy=args.deployment_strategy, sync=args.sync, net=args.net,
                                    pid=args.pid)
        elif args.subcmd == 'inspect':
            commands.service_inspect(args.identifier)
        elif args.subcmd == 'logs':
            commands.service_logs(args.identifier, args.tail, args.follow)
        elif args.subcmd == 'ps':
            commands.service_ps(args.quiet, args.status, args.stack)
        elif args.subcmd == 'redeploy':
            commands.service_redeploy(args.identifier, args.not_reuse_volumes, args.sync)
        elif args.subcmd == 'run':
            commands.service_run(image=args.image, name=args.name, cpu_shares=args.cpushares,
                                 memory=args.memory, privileged=args.privileged,
                                 target_num_containers=args.target_num_containers, run_command=args.run_command,
                                 entrypoint=args.entrypoint, expose=args.expose, publish=args.publish, envvars=args.env,
                                 envfiles=args.env_file,
                                 tag=args.tag, linked_to_service=args.link_service,
                                 autorestart=args.autorestart, autodestroy=args.autodestroy,
                                 autoredeploy=args.autoredeploy, roles=args.role,
                                 sequential=args.sequential, volume=args.volume, volumes_from=args.volumes_from,
                                 deployment_strategy=args.deployment_strategy, sync=args.sync, net=args.net,
                                 pid=args.pid)
        elif args.subcmd == 'scale':
            commands.service_scale(args.identifier, args.target_num_containers, args.sync)
        elif args.subcmd == 'set':
            commands.service_set(args.identifier, image=args.image, cpu_shares=args.cpushares,
                                 memory=args.memory, privileged=args.privileged,
                                 target_num_containers=args.target_num_containers, run_command=args.run_command,
                                 entrypoint=args.entrypoint, expose=args.expose, publish=args.publish, envvars=args.env,
                                 envfiles=args.env_file,
                                 tag=args.tag, linked_to_service=args.link_service,
                                 autorestart=args.autorestart, autodestroy=args.autodestroy,
                                 autoredeploy=args.autoredeploy, roles=args.role,
                                 sequential=args.sequential, redeploy=args.redeploy,
                                 volume=args.volume, volumes_from=args.volumes_from,
                                 deployment_strategy=args.deployment_strategy, sync=args.sync, net=args.net,
                                 pid=args.pid)
        elif args.subcmd == 'start':
            commands.service_start(args.identifier, args.sync)
        elif args.subcmd == 'stop':
            commands.service_stop(args.identifier, args.sync)
        elif args.subcmd == 'terminate':
            commands.service_terminate(args.identifier, args.sync)
        elif args.subcmd == 'env':
            if args.envsubcmd == 'add':
                commands.service_env_add(args.identifier, envvars=args.env, envfiles=args.env_file,
                                         redeploy=args.redeploy, sync=args.sync)
            elif args.envsubcmd == 'list':
                commands.service_env_list(args.identifier, args.quiet, args.user, args.image, args.tutum)
            elif args.envsubcmd == 'remove':
                commands.service_env_remove(args.identifier, names=args.name, redeploy=args.redeploy, sync=args.sync)
            elif args.envsubcmd == 'set':
                commands.service_env_set(args.identifier, envvars=args.env, envfiles=args.env_file,
                                         redeploy=args.redeploy, sync=args.sync)
            elif args.envsubcmd == 'update':
                commands.service_env_update(args.identifier, envvars=args.env, envfiles=args.env_file,
                                            redeploy=args.redeploy, sync=args.sync)
    elif args.cmd == 'container':
        if args.subcmd == 'exec':
            commands.container_exec(args.identifier, args.command)
        elif args.subcmd == 'inspect':
            commands.container_inspect(args.identifier)
        elif args.subcmd == 'logs':
            commands.container_logs(args.identifier, args.tail, args.follow)
        elif args.subcmd == 'redeploy':
            commands.container_redeploy(args.identifier, args.not_reuse_volumes, args.sync)
        elif args.subcmd == 'ps':
            commands.container_ps(args.quiet, args.status, args.service, args.no_trunc)
        elif args.subcmd == 'start':
            commands.container_start(args.identifier, args.sync)
        elif args.subcmd == 'stop':
            commands.container_stop(args.identifier, args.sync)
        elif args.subcmd == 'terminate':
            commands.container_terminate(args.identifier, args.sync)
    elif args.cmd == 'image':
        if args.subcmd == 'list':
            commands.image_list(args.quiet, args.jumpstarts, args.private, args.user, args.all, args.no_trunc)
        elif args.subcmd == 'register':
            commands.image_register(args.image_name, args.description, args.username, args.password, args.sync)
        elif args.subcmd == 'push':
            commands.image_push(args.name, args.public)
        elif args.subcmd == 'rm':
            commands.image_rm(args.image_name, args.sync)
        elif args.subcmd == 'search':
            commands.image_search(args.query)
        elif args.subcmd == 'update':
            commands.image_update(args.image_name, args.username, args.password, args.description, args.sync)
        elif args.subcmd == 'inspect':
            commands.image_inspect(args.identifier)
        elif args.subcmd == 'tag':
            if args.imagetagsubcmd == 'list':
                commands.image_tag_list(args.jumpstarts, args.private, args.user, args.all, args.identifier)
            elif args.imagetagsubcmd == 'inspect':
                commands.image_tag_inspect(args.identifier)
            elif args.imagetagsubcmd == 'build':
                commands.image_tag_build(args.identifier, args.sync)
    elif args.cmd == 'node':
        if args.subcmd == 'inspect':
            commands.node_inspect(args.identifier)
        elif args.subcmd == 'list':
            commands.node_list(args.quiet)
        elif args.subcmd == 'rm':
            commands.node_rm(args.identifier, args.sync)
        elif args.subcmd == 'upgrade':
            commands.node_upgrade(args.identifier, args.sync)
        elif args.subcmd == 'byo':
            commands.node_byo()
        elif args.subcmd == 'healthcheck':
            commands.node_healthcheck(args.identifier)
    elif args.cmd == 'nodecluster':
        if args.subcmd == 'create':
            commands.nodecluster_create(args.target_num_nodes, args.name, args.provider, args.region, args.nodetype,
                                        args.sync, args.disk, args.tag, args.aws_vpc_id, args.aws_vpc_subnet,
                                        args.aws_vpc_security_group, args.aws_iam_instance_profile_name)
        elif args.subcmd == 'inspect':
            commands.nodecluster_inspect(args.identifier)
        elif args.subcmd == 'list':
            commands.nodecluster_list(args.quiet)
        elif args.subcmd == 'provider':
            commands.nodecluster_show_providers(args.quiet)
        elif args.subcmd == 'region':
            commands.nodecluster_show_regions(args.provider)
        elif args.subcmd == 'nodetype':
            commands.nodecluster_show_types(args.provider, args.region)
        elif args.subcmd == 'rm':
            commands.nodecluster_rm(args.identifier, args.sync)
        elif args.subcmd == 'az':
            commands.nodecluster_az(args.quiet)
        elif args.subcmd == 'scale':
            commands.nodecluster_scale(args.identifier, args.target_num_nodes, args.sync)
        elif args.subcmd == 'upgrade':
            commands.nodecluster_upgrade(args.identifier, args.sync)
    elif args.cmd == 'tag':
        if args.subcmd == 'add':
            commands.tag_add(args.identifier, args.tag)
        elif args.subcmd == 'list':
            commands.tag_list(args.identifier, args.quiet)
        elif args.subcmd == 'rm':
            commands.tag_rm(args.identifier, args.tag)
        elif args.subcmd == 'set':
            commands.tag_set(args.identifier, args.tag)
    elif args.cmd == 'volume':
        if args.subcmd == 'list':
            commands.volume_list(args.quiet)
        if args.subcmd == 'inspect':
            commands.volume_inspect(args.identifier)
    elif args.cmd == 'volumegroup':
        if args.subcmd == 'list':
            commands.volumegroup_list(args.quiet)
        if args.subcmd == 'inspect':
            commands.volumegroup_inspect(args.identifier)
    elif args.cmd == 'trigger':
        if args.subcmd == 'create':
            commands.trigger_create(args.identifier, args.name, args.operation)
        elif args.subcmd == 'list':
            commands.trigger_list(args.identifier, args.quiet)
        elif args.subcmd == 'rm':
            commands.trigger_rm(args.identifier, args.trigger)
    elif args.cmd == 'stack':
        if args.subcmd == 'create':
            commands.stack_create(args.name, args.file, args.sync)
        elif args.subcmd == 'inspect':
            commands.stack_inspect(args.identifier)
        elif args.subcmd == 'list':
            commands.stack_list(args.quiet)
        elif args.subcmd == 'redeploy':
            commands.stack_redeploy(args.identifier, args.not_reuse_volumes, args.sync)
        elif args.subcmd == 'start':
            commands.stack_start(args.identifier, args.sync)
        elif args.subcmd == 'stop':
            commands.stack_stop(args.identifier, args.sync)
        elif args.subcmd == 'terminate':
            commands.stack_terminate(args.identifier, args.sync)
        elif args.subcmd == 'up':
            commands.stack_up(args.name, args.file, args.sync)
        elif args.subcmd == 'update':
            commands.stack_update(args.identifier, args.file, args.sync)
        elif args.subcmd == 'export':
            commands.stack_export(args.identifier, args.file)
    elif args.cmd == 'up':
        commands.stack_up(args.name, args.file, args.sync)


def main():
    parser = initialize_parser()
    argv = patch_help_option(sys.argv)
    args = parser.parse_args(argv)
    commands.verify_auth(args)
    dispatch_cmds(args)


if __name__ == '__main__':
    main()
