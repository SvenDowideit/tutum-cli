import argparse


def add_login_parser(subparsers):
    # tutum login
    login_parser = subparsers.add_parser('login', help='Login into Tutum', description='Login into Tutum')
    login_parser.add_argument('-u', '--username', help='Tutum username')
    login_parser.add_argument('-p', '--password', help='Tutum password')


def add_build_parser(subparsers):
    # tutum build
    build_parser = subparsers.add_parser('build', help='Build an image using tutum/builder',
                                         description='Build an image using tutum/builder')
    build_parser.add_argument('-t', '--tag', help='repository name (and optionally a tag) to be applied '
                                                  'to the resulting image in case of success')
    build_parser.add_argument('directory', help='working directory')
    build_parser.add_argument('-s', '--sock', help='docker unix sock address. Default: "/var/run/docker.sock"')


def add_event_parser(subparsers):
    # tutum event
    subparsers.add_parser('event', help='Get real time tutum events',
                          description='Get real time tutum events')


def add_push_parser(subparsers):
    # tutum push
    push_parser = subparsers.add_parser('push', help='Deprecated. Please use "docker push" instead',
                                        description='Deprecated. Please use "docker push" instead')
    push_parser.add_argument('name', help='name of the image to push')
    push_parser.add_argument('--public', help='push image to public registry', action='store_true')


def add_run_parser(subparsers):
    # tutum run
    run_parser = subparsers.add_parser('run', help='Create and run a new service',
                                       description='Create and run a new service', )
    run_parser.add_argument('image', help='the name of the image used to deploy this service')
    run_parser.add_argument('-n', '--name', help='a human-readable name for the service '
                                                 '(default: image_tag without namespace)')
    run_parser.add_argument('--cpushares', help='Relative weight for CPU Shares', type=int)
    run_parser.add_argument('--memory', help='RAM memory hard limit in MB', type=int)
    run_parser.add_argument('--privileged', help='Give extended privileges to this container', action='store_true')
    run_parser.add_argument('-t', '--target-num-containers',
                            help='the number of containers to run for this service (default: 1)', type=int)
    run_parser.add_argument('-r', '--run-command',
                            help='the command used to start the service containers '
                                 '(default: as defined in the image)')
    run_parser.add_argument('--entrypoint',
                            help='the command prefix used to start the service containers '
                                 '(default: as defined in the image)')
    run_parser.add_argument('-p', '--publish', help="Publish a container's port to the host. "
                                                    "Format: [hostPort:]containerPort[/protocol], i.e. \"80:80/tcp\"",
                            action='append')
    run_parser.add_argument('--expose', help='Expose a port from the container without publishing it to your host',
                            action='append', type=int)
    run_parser.add_argument('-e', '--env',
                            help='set environment variables i.e. "ENVVAR=foo" '
                                 '(default: as defined in the image, plus any link- or role-generated variables)',
                            action='append')
    run_parser.add_argument('--env-file', help='read in a line delimited file of environment variables',
                            action='append')
    run_parser.add_argument('--tag', help="the tag name being added to the service", action='append')
    run_parser.add_argument('--link-service',
                            help="Add link to another service (name:alias) or (uuid:alias)", action='append')
    run_parser.add_argument('--autodestroy', help='whether the containers should be terminated if '
                                                  'they stop (default: OFF)',
                            choices=['OFF', 'ON_FAILURE', 'ALWAYS'])
    run_parser.add_argument('--autoredeploy', help="whether the containers should be auto redeployed."
                                                   " It only applies to services that use an image stored in Tutum's "
                                                   "registry", action='store_true')
    run_parser.add_argument('--autorestart', help='whether the containers should be restarted if they stop '
                                                  '(default: OFF)', choices=['OFF', 'ON_FAILURE', 'ALWAYS'])
    run_parser.add_argument('--role', help='Tutum API roles to grant the service, '
                                           'i.e. "global" (default: none, possible values: "global")', action='append')
    run_parser.add_argument('--sequential', help='whether the containers should be launched and scaled sequentially',
                            action='store_true')
    run_parser.add_argument('-v', '--volume', help='Bind mount a volume (e.g., from the host: -v /host:/container, '
                                                   'from Docker: -v /container)', action='append')
    run_parser.add_argument('--volumes-from', help='Mount volumes from the specified service(s)', action='append')
    run_parser.add_argument('--deployment-strategy', help='Container distribution strategy among nodes',
                            choices=['EMPTIEST_NODE', 'HIGH_AVAILABILITY', 'EVERY_NODE'])
    run_parser.add_argument('--sync', help='block the command until the async operation has finished',
                            action='store_true')
    run_parser.add_argument('--net', help='Set the Network mode for the container')
    run_parser.add_argument('--pid', help="PID namespace to use")


def add_up_parser(subparsers):
    # tutum up
    up_parser = subparsers.add_parser('up', help='Create and deploy a stack',
                                      description='Create and deploy a stack')
    up_parser.add_argument('-n', '--name', help='The name of the stack, which wil be shown in tutum')
    up_parser.add_argument('-f', '--file', help="the name of the Stackfile")
    up_parser.add_argument('--sync', help='block the command until the async operation has finished',
                           action='store_true')


def add_exec_parser(subparsers):
    # tutum exec
    exec_parser = subparsers.add_parser('exec', help='Run a command in a running container',
                                        description='Run a command in a running container')
    exec_parser.add_argument('identifier', help="container's UUID (either long or short) or name")
    exec_parser.add_argument('command', help="the command to run (default: sh)", nargs=argparse.REMAINDER)


def add_action_parser(subparsers):
    # tutum action
    action_parser = subparsers.add_parser('action', help='Action-related operations',
                                          description='Action-related operations')
    action_subparser = action_parser.add_subparsers(title='tutum action commands', dest='subcmd')

    # tutum action inspect
    inspect_parser = action_subparser.add_parser('inspect', help="Get all details from an action",
                                                 description="Get all details from an action")
    inspect_parser.add_argument('identifier', help="action's UUID (either long or short)", nargs='+')

    # tutum action list
    list_parser = action_subparser.add_parser('list', help='List actions', description='List actions')
    list_parser.add_argument('-q', '--quiet', help='print only action uuid', action='store_true')
    list_parser.add_argument('-l', '--last', help='Output the last number of actions (default:25)', type=int)

    # tutum action logs
    logs_parser = action_subparser.add_parser('logs', help='Get logs from an action',
                                              description='Get logs from an action')
    logs_parser.add_argument('identifier', help="service's UUID (either long or short)", nargs='+')
    logs_parser.add_argument('-f', '--follow', help='follow log output', action='store_true')
    logs_parser.add_argument('-t', '--tail', help='Output the specified number of lines at the end of logs '
                                                  '(defaults: 300)', type=int)

    # tutum action cancel
    inspect_parser = action_subparser.add_parser('cancel', help="Cancel an action in Pending or In progress state",
                                                 description="Cancels an action in Pending or In progress state")
    inspect_parser.add_argument('identifier', help="action's UUID (either long or short)", nargs='+')

    # tutum action retry
    inspect_parser = action_subparser.add_parser('retry', help="Retries an action in Success, Failed or Canceled state",
                                                 description="Retries an action in Success, Failed or Canceled state")
    inspect_parser.add_argument('identifier', help="action's UUID (either long or short)", nargs='+')


def add_service_parser(subparsers):
    def str2bool(v):
        return v.lower() in ("yes", "true", "t", "1", "y")

    # tutum service
    service_parser = subparsers.add_parser('service', help='Service-related operations',
                                           description='Service-related operations')
    service_subparser = service_parser.add_subparsers(title='tutum service commands', dest='subcmd')

    # tutum service run
    create_parser = service_subparser.add_parser('create', help='Create a new service',
                                                 description='Create a new service', )
    create_parser.add_argument('image', help='the name of the image used to deploy this service')
    create_parser.add_argument('-n', '--name', help='a human-readable name for the service '
                                                    '(default: image_tag without namespace)')
    create_parser.add_argument('--cpushares', help='Relative weight for CPU Shares', type=int)
    create_parser.add_argument('--memory', help='RAM memory hard limit in MB', type=int)
    create_parser.add_argument('--privileged', help='Give extended privileges to this container', action='store_true')
    create_parser.add_argument('-t', '--target-num-containers',
                               help='the number of containers to run for this service (default: 1)', type=int)
    create_parser.add_argument('-r', '--run-command',
                               help='the command used to start the service containers '
                                    '(default: as defined in the image)')
    create_parser.add_argument('--entrypoint',
                               help='the command prefix used to start the service containers '
                                    '(default: as defined in the image)')
    create_parser.add_argument('-p', '--publish', help="Publish a container's port to the host. "
                                                       "Format: [hostPort:]containerPort[/protocol], i.e. '80:80/tcp'",
                               action='append')
    create_parser.add_argument('--expose', help='Expose a port from the container without publishing it to your host',
                               action='append', type=int)
    create_parser.add_argument('-e', '--env',
                               help='set environment variables i.e. "ENVVAR=foo" '
                                    '(default: as defined in the image, plus any link- or role-generated variables)',
                               action='append')
    create_parser.add_argument('--env-file', help='read in a line delimited file of environment variables',
                               action='append')
    create_parser.add_argument('--tag', help="the tag name being added to the service", action='append')
    create_parser.add_argument('--link-service',
                               help="Add link to another service (name:alias) or (uuid:alias)", action='append')
    create_parser.add_argument('--autodestroy', help='whether the containers should be terminated if '
                                                     'they stop (default: OFF)',
                               choices=['OFF', 'ON_SUCCESS', 'ALWAYS'])
    create_parser.add_argument('--autoredeploy', help="whether the containers should be auto redeployed."
                                                      " It only applies to services that use an image stored"
                                                      " in Tutum's registry", action='store_true')
    create_parser.add_argument('--autorestart', help='whether the containers should be restarted if they stop '
                                                     '(default: OFF)', choices=['OFF', 'ON_FAILURE', 'ALWAYS'])
    create_parser.add_argument('--role', help='Tutum API roles to grant the service, '
                                              'i.e. "global" (default: none, possible values: "global")',
                               action='append')
    create_parser.add_argument('--sequential', help='whether the containers should be launched and scaled sequentially',
                               action='store_true')
    create_parser.add_argument('-v', '--volume', help='Bind mount a volume (e.g., from the host: -v /host:/container, '
                                                      'from Docker: -v /container)', action='append')
    create_parser.add_argument('--volumes-from', help='Mount volumes from the specified service(s)', action='append')

    create_parser.add_argument('--deployment-strategy', help='Container distribution strategy among nodes',
                               choices=['EMPTIEST_NODE', 'HIGH_AVAILABILITY', 'EVERY_NODE'])
    create_parser.add_argument('--sync', help='block the command until the async operation has finished',
                               action='store_true')
    create_parser.add_argument('--net', help='Set the Network mode for the container')
    create_parser.add_argument('--pid', help="PID namespace to use")

    # tutum service env
    env_parser = service_subparser.add_parser('env', help="Service environment variables related operations",
                                              description="Service environment variables related operations")
    env_subparser = env_parser.add_subparsers(title='tutum service env commands', dest='envsubcmd')

    # tutum service env add
    env_add_parser = env_subparser.add_parser('add', help='Add new environment variables',
                                              description='Add new environment variables')
    env_add_parser.add_argument('identifier', help="service's UUID (either long or short) or name[.stack_name]",
                                nargs='+')
    env_add_parser.add_argument('-e', '--env',
                                help='set environment variables i.e. "ENVVAR=foo" '
                                     '(default: as defined in the image, plus any link- or role-generated variables)',
                                action='append')
    env_add_parser.add_argument('--env-file', help='read in a line delimited file of environment variables',
                                action='append')
    env_add_parser.add_argument('--sync', help='block the command until the async operation has finished',
                                action='store_true')
    env_add_parser.add_argument('--redeploy', help="redeploy service with new configuration after set command",
                                action='store_true')

    # tutum service env list
    env_list_parser = env_subparser.add_parser('list', help='list all environment variables',
                                               description='list all environment variables')
    env_list_parser.add_argument('identifier', help="service's UUID (either long or short) or name[.stack_name]")
    env_list_parser.add_argument('-q', '--quiet', help='print only key value pair', action='store_true')
    env_list_parser.add_argument('--user', help='show only user defined environment variables', action='store_true')
    env_list_parser.add_argument('--image', help='show only image defined environment variables', action='store_true')
    env_list_parser.add_argument('--tutum', help='show only tutum defined environment variables', action='store_true')

    # tutum service env remove
    env_remove_parser = env_subparser.add_parser('remove', help='Remove existing environment variables',
                                                 description='Remove existing environment variables')
    env_remove_parser.add_argument('identifier', help="service's UUID (either long or short) or name[.stack_name]",
                                   nargs='+')
    env_remove_parser.add_argument('-n', '--name', help='names of the environments to remove', action='append')
    env_remove_parser.add_argument('--sync', help='block the command until the async operation has finished',
                                   action='store_true')
    env_remove_parser.add_argument('--redeploy', help="redeploy service with new configuration after set command",
                                   action='store_true')

    # tutum service env set
    env_set_parser = env_subparser.add_parser('set', help='Replace existing environment variables with new ones',
                                              description='Replace existing environment variables with new ones')
    env_set_parser.add_argument('identifier', help="service's UUID (either long or short) or name[.stack_name]",
                                nargs='+')
    env_set_parser.add_argument('-e', '--env',
                                help='set environment variables i.e. "ENVVAR=foo" '
                                     '(default: as defined in the image, plus any link- or role-generated variables)',
                                action='append')
    env_set_parser.add_argument('--env-file', help='read in a line delimited file of environment variables',
                                action='append')
    env_set_parser.add_argument('--sync', help='block the command until the async operation has finished',
                                action='store_true')
    env_set_parser.add_argument('--redeploy', help="redeploy service with new configuration after set command",
                                action='store_true')

    # tutum service env update
    env_update_parser = env_subparser.add_parser('update', help='Update existing environment variables with new values',
                                                 description='Update existing environment variables with new values')
    env_update_parser.add_argument('identifier', help="service's UUID (either long or short) or name[.stack_name]",
                                   nargs='+')
    env_update_parser.add_argument('-e', '--env',
                                   help='set environment variables i.e. "ENVVAR=foo" (default: '
                                        'as defined in the image, plus any link- or role-generated variables)',
                                   action='append')
    env_update_parser.add_argument('--env-file', help='read in a line delimited file of environment variables',
                                   action='append')
    env_update_parser.add_argument('--sync', help='block the command until the async operation has finished',
                                   action='store_true')
    env_update_parser.add_argument('--redeploy', help="redeploy service with new configuration after set command",
                                   action='store_true')

    # tutum service inspect
    inspect_parser = service_subparser.add_parser('inspect', help="Get all details from a service",
                                                  description="Get all details from a service")
    inspect_parser.add_argument('identifier', help="service's UUID (either long or short) or name[.stack_name]",
                                nargs='+')

    # tutum service logs
    logs_parser = service_subparser.add_parser('logs', help='Get logs from a service',
                                               description='Get logs from a service')
    logs_parser.add_argument('identifier', help="service's UUID (either long or short) or name[.stack_name]", nargs='+')
    logs_parser.add_argument('-f', '--follow', help='follow log output', action='store_true')
    logs_parser.add_argument('-t', '--tail', help='Output the specified number of lines at the end of logs '
                                                  '(defaults: 300)', type=int)

    # tutum service ps
    ps_parser = service_subparser.add_parser('ps', help='List services', description='List services')
    ps_parser.add_argument('-q', '--quiet', help='print only long UUIDs', action='store_true')
    ps_parser.add_argument('-s', '--status', help='filter services by status',
                           choices=['Init', 'Stopped', 'Starting', 'Running', 'Stopping', 'Terminating', 'Terminated',
                                    'Scaling', 'Partly running', 'Not running', 'Redeploying'])
    ps_parser.add_argument('--stack', help="filter services by stack (UUID either long or short, or name)")

    # tutum service redeploy
    redeploy_parser = service_subparser.add_parser('redeploy', help='Redeploy a running service',
                                                   description='Redeploy a running service')
    redeploy_parser.add_argument('identifier', help="service's UUID (either long or short) or name[.stack_name]",
                                 nargs='+')
    redeploy_parser.add_argument('--not-reuse-volumes', help="do not reuse volumes in redeployment",
                                 action='store_true')
    redeploy_parser.add_argument('--sync', help='block the command until the async operation has finished',
                                 action='store_true')

    # tutum service run
    run_parser = service_subparser.add_parser('run', help='Create and run a new service',
                                              description='Create and run a new service', )
    run_parser.add_argument('image', help='the name of the image used to deploy this service')
    run_parser.add_argument('-n', '--name', help='a human-readable name for the service '
                                                 '(default: image_tag without namespace)')
    run_parser.add_argument('--cpushares', help='Relative weight for CPU Shares', type=int)
    run_parser.add_argument('--memory', help='RAM memory hard limit in MB', type=int)
    run_parser.add_argument('--privileged', help='Give extended privileges to this container', action='store_true')
    run_parser.add_argument('-t', '--target-num-containers',
                            help='the number of containers to run for this service (default: 1)', type=int)
    run_parser.add_argument('-r', '--run-command',
                            help='the command used to start the service containers '
                                 '(default: as defined in the image)')
    run_parser.add_argument('--entrypoint',
                            help='the command prefix used to start the service containers '
                                 '(default: as defined in the image)')
    run_parser.add_argument('-p', '--publish', help="Publish a container's port to the host. "
                                                    "Format: [hostPort:]containerPort[/protocol], i.e. \"80:80/tcp\"",
                            action='append')
    run_parser.add_argument('--expose', help='Expose a port from the container without publishing it to your host',
                            action='append', type=int)
    run_parser.add_argument('-e', '--env',
                            help='set environment variables i.e. "ENVVAR=foo" '
                                 '(default: as defined in the image, plus any link- or role-generated variables)',
                            action='append')
    run_parser.add_argument('--env-file', help='read in a line delimited file of environment variables',
                            action='append')
    run_parser.add_argument('--tag', help="the tag name being added to the service", action='append')
    run_parser.add_argument('--link-service',
                            help="Add link to another service (name:alias) or (uuid:alias)", action='append')
    run_parser.add_argument('--autodestroy', help='whether the containers should be terminated if '
                                                  'they stop (default: OFF)',
                            choices=['OFF', 'ON_SUCCESS', 'ALWAYS'])
    run_parser.add_argument('--autoredeploy', help="whether the containers should be auto redeployed."
                                                   " It only applies to services that use an image stored in Tutum's "
                                                   "registry", action='store_true')
    run_parser.add_argument('--autorestart', help='whether the containers should be restarted if they stop '
                                                  '(default: OFF)', choices=['OFF', 'ON_FAILURE', 'ALWAYS'])
    run_parser.add_argument('--role', help='Tutum API roles to grant the service, '
                                           'i.e. "global" (default: none, possible values: "global")', action='append')
    run_parser.add_argument('--sequential', help='whether the containers should be launched and scaled sequentially',
                            action='store_true')
    run_parser.add_argument('-v', '--volume', help='Bind mount a volume (e.g., from the host: -v /host:/container, '
                                                   'from Docker: -v /container)', action='append')
    run_parser.add_argument('--volumes-from', help='Mount volumes from the specified service(s)', action='append')
    run_parser.add_argument('--deployment-strategy', help='Container distribution strategy among nodes',
                            choices=['EMPTIEST_NODE', 'HIGH_AVAILABILITY', 'EVERY_NODE'])
    run_parser.add_argument('--sync', help='block the command until the async operation has finished',
                            action='store_true')
    run_parser.add_argument('--net', help='Set the Network mode for the container')
    run_parser.add_argument('--pid', help="PID namespace to use")

    # tutum service scale
    scale_parser = service_subparser.add_parser('scale', help='Scale a running service',
                                                description='Scale a running service', )
    scale_parser.add_argument('identifier', help="service's UUID (either long or short) or name[.stack_name]",
                              nargs='+')
    scale_parser.add_argument("target_num_containers", metavar="target-num-containers",
                              help="target number of containers to scale this service to", type=int)
    scale_parser.add_argument('--sync', help='block the command until the async operation has finished',
                              action='store_true')

    # tutum service set
    set_parser = service_subparser.add_parser('set', help='Change and replace the existing service properties',
                                              description='Change service properties.'
                                                          ' This command REPLACES the existing properties.')
    set_parser.register('type', 'bool', str2bool)
    set_parser.add_argument('identifier', help="service's UUID (either long or short) or name[.stack_name]", nargs='+')
    set_parser.add_argument('--image', help='the name of the image used to deploy this service')
    set_parser.add_argument('--cpushares', help='Relative weight for CPU Shares', type=int)
    set_parser.add_argument('--memory', help='RAM memory hard limit in MB', type=int)
    set_parser.add_argument('--privileged', help='Give extended privileges to this container <true/false>', type='bool')
    set_parser.add_argument('-t', '--target-num-containers',
                            help='the number of containers to run for this service', type=int)
    set_parser.add_argument('-r', '--run-command',
                            help='the command used to start the service containers '
                                 '(default: as defined in the image)')
    set_parser.add_argument('--entrypoint',
                            help='the command prefix used to start the service containers '
                                 '(default: as defined in the image)')
    set_parser.add_argument('-p', '--publish', help="Publish a container's port to the host. "
                                                    "Format: [hostPort:]containerPort[/protocol], i.e. \"80:80/tcp\"",
                            action='append')
    set_parser.add_argument('--expose', help='Expose a port from the container without publishing it to your host',
                            action='append', type=int)
    set_parser.add_argument('-e', '--env',
                            help='set environment variables i.e. "ENVVAR=foo" '
                                 '(default: as defined in the image, plus any link- or role-generated variables)',
                            action='append')
    set_parser.add_argument('--env-file', help='read in a line delimited file of environment variables',
                            action='append')
    set_parser.add_argument('--tag', help="the tag name being added to the service", action='append')
    set_parser.add_argument('--link-service',
                            help="Add link to another service (name:alias) or (uuid:alias)", action='append')
    set_parser.add_argument('--autodestroy', help='whether the containers should be terminated if '
                                                  'they stop (default: OFF)',
                            choices=['OFF', 'ON_SUCCESS', 'ALWAYS'])
    set_parser.add_argument('--autoredeploy', help="whether the containers should be auto redeployed."
                                                   " It only applies to services that use an image stored in Tutum's "
                                                   "registry", action='store_true')
    set_parser.add_argument('--autorestart', help='whether the containers should be restarted if they stop '
                                                  '(default: OFF)', choices=['OFF', 'ON_FAILURE', 'ALWAYS'])
    set_parser.add_argument('--role', help='Tutum API roles to grant the service, '
                                           'i.e. "global" (default: none, possible values: "global")', action='append')
    set_parser.add_argument('--sequential',
                            help='whether the containers should be launched and scaled sequentially<true/false>',
                            type='bool')
    set_parser.add_argument('--redeploy', help="redeploy service with new configuration after set command",
                            action='store_true')
    set_parser.add_argument('-v', '--volume', help='Bind mount a volume (e.g., from the host: -v /host:/container, '
                                                   'from Docker: -v /container)', action='append')
    set_parser.add_argument('--volumes-from', help='Mount volumes from the specified service(s)', action='append')
    set_parser.add_argument('--deployment-strategy', help='Container distribution strategy among nodes',
                            choices=['EMPTIEST_NODE', 'HIGH_AVAILABILITY', 'EVERY_NODE'])
    set_parser.add_argument('--sync', help='block the command until the async operation has finished',
                            action='store_true')
    set_parser.add_argument('--net', help='Set the Network mode for the container')
    set_parser.add_argument('--pid', help="PID namespace to use")

    # tutum service start
    start_parser = service_subparser.add_parser('start', help='Start a stopped service',
                                                description='Start a stopped service')
    start_parser.add_argument('identifier', help="service's UUID (either long or short) or name[.stack_name]",
                              nargs='+')
    start_parser.add_argument('--sync', help='block the command until the async operation has finished',
                              action='store_true')

    # tutum service stop
    stop_parser = service_subparser.add_parser('stop', help='Stop a running service',
                                               description='Stop a running service')
    stop_parser.add_argument('identifier', help="service's UUID (either long or short) or name[.stack_name]", nargs='+')
    stop_parser.add_argument('--sync', help='block the command until the async operation has finished',
                             action='store_true')

    # tutum service terminate
    terminate_parser = service_subparser.add_parser('terminate', help='Terminate a service',
                                                    description='Terminate a service')
    terminate_parser.add_argument('identifier', help="service's UUID (either long or short) or name[.stack_name]",
                                  nargs='+')
    terminate_parser.add_argument('--sync', help='block the command until the async operation has finished',
                                  action='store_true')


def add_container_parser(subparsers):
    # tutum container
    container_parser = subparsers.add_parser('container', help='Container-related operations',
                                             description='Container-related operations')
    container_subparser = container_parser.add_subparsers(title='tutum container commands', dest='subcmd')

    # tutum container exec
    exec_parser = container_subparser.add_parser('exec', help='Run a command in a running container',
                                                 description='Run a command in a running container')
    exec_parser.add_argument('identifier', help="container's UUID (either long or short) or name[.stack_name]")
    exec_parser.add_argument('command', help="the command to run (default: sh)", nargs=argparse.REMAINDER)

    # tutum container inspect
    inspect_parser = container_subparser.add_parser('inspect', help='Inspect a container',
                                                    description='Inspect a container')
    inspect_parser.add_argument('identifier', help="container's UUID (either long or short) or name[.stack_name]",
                                nargs='+')

    # tutum container logs
    logs_parser = container_subparser.add_parser('logs', help='Get logs from a container',
                                                 description='Get logs from a container')
    logs_parser.add_argument('identifier', help="container's UUID (either long or short) or name[.stack_name]",
                             nargs='+')
    logs_parser.add_argument('-f', '--follow', help='follow log output', action='store_true')
    logs_parser.add_argument('-t', '--tail', help='Output the specified number of lines at the end of logs '
                                                  '(defaults: 300)', type=int)

    redeploy_parser = container_subparser.add_parser('redeploy', help='Redeploy a running container',
                                                     description='Redeploy a running container')
    redeploy_parser.add_argument('identifier', help="container's UUID (either long or short) or name[.stack_name]",
                                 nargs='+')
    redeploy_parser.add_argument('--not-reuse-volumes', help="do not reuse volumes in redeployment",
                                 action='store_true')
    redeploy_parser.add_argument('--sync', help='block the command until the async operation has finished',
                                 action='store_true')

    # tutum container ps
    ps_parser = container_subparser.add_parser('ps', help='List containers', description='List containers')
    ps_parser.add_argument('-q', '--quiet', help='print only long UUIDs', action='store_true')
    ps_parser.add_argument('-s', '--status', help='filter containers by status',
                           choices=['Init', 'Stopped', 'Starting', 'Running', 'Stopping', 'Terminating', 'Terminated'])
    ps_parser.add_argument('--service', help="filter containers by service (UUID either long or short, or name)")
    ps_parser.add_argument('--no-trunc', help="don't truncate output", action='store_true')

    # tutum container start
    start_parser = container_subparser.add_parser('start', help='Start a container', description='Start a container')
    start_parser.add_argument('identifier', help="container's UUID (either long or short) or name[.stack_name]",
                              nargs='+')
    start_parser.add_argument('--sync', help='block the command until the async operation has finished',
                              action='store_true')

    # tutum container stop
    stop_parser = container_subparser.add_parser('stop', help='Stop a container', description='Stop a container')
    stop_parser.add_argument('identifier', help="container's UUID (either long or short) or name[.stack_name]",
                             nargs='+')
    stop_parser.add_argument('--sync', help='block the command until the async operation has finished',
                             action='store_true')

    # tutum container terminate
    terminate_parser = container_subparser.add_parser('terminate', help='Terminate a container',
                                                      description='Terminate a container')
    terminate_parser.add_argument('identifier', help="container's UUID (either long or short) or name[.stack_name]",
                                  nargs='+')
    terminate_parser.add_argument('--sync', help='block the command until the async operation has finished',
                                  action='store_true')


def add_image_parser(subparsers):
    # tutum image
    image_parser = subparsers.add_parser('image', help='Image-related operations',
                                         description='Image-related operations')
    image_subparser = image_parser.add_subparsers(title='tutum image commands', dest='subcmd')

    # tutum image tag
    tag_parser = image_subparser.add_parser('tag', help="Image tag related operations",
                                            description="Image tag related operations")
    tag_subparser = tag_parser.add_subparsers(title='tutum image tag commands', dest='imagetagsubcmd')

    # tutum image tag list
    tag_list_parser = tag_subparser.add_parser('list', help="List tags of user's images",
                                               description="List tags of user's images")
    tag_list_exclusive_group = tag_list_parser.add_mutually_exclusive_group()
    tag_list_exclusive_group.add_argument('-j', '--jumpstarts', help='list jumpstart images only', action='store_true')
    tag_list_exclusive_group.add_argument('-p', '--private', help='list private images only', action='store_true')
    tag_list_exclusive_group.add_argument('-u', '--user', help='list user added images only(default)',
                                          action='store_true')
    tag_list_exclusive_group.add_argument('-a', '--all', help='list all images', action='store_true')
    tag_list_parser.add_argument('identifier', help="image name", nargs='*')

    # tutum image tag inspect
    tag_inspect_parser = tag_subparser.add_parser('inspect', help="Inspect an image tag",
                                                  description="Inspect an image tag")
    tag_inspect_parser.add_argument('identifier', help="image tag, format: image_name:[tag]", nargs='+')

    # tutum image tag build
    tag_build_parser = tag_subparser.add_parser('build', help="Build an image tag", description="Build an image tag")
    tag_build_parser.add_argument('identifier', help="image tag, format: image_name:[tag]", nargs='+')
    tag_build_parser.add_argument('--sync', help='block the command until the async operation has finished',
                                  action='store_true')

    # tutum image list
    list_parser = image_subparser.add_parser('list', help="List user's images", description="List user's images")
    list_parser.add_argument('-q', '--quiet', help='print only image names', action='store_true')

    list_exclusive_group = list_parser.add_mutually_exclusive_group()
    list_exclusive_group.add_argument('-j', '--jumpstarts', help='list jumpstart images only', action='store_true')
    list_exclusive_group.add_argument('-p', '--private', help='list private images only', action='store_true')
    list_exclusive_group.add_argument('-u', '--user', help='list user added images only(default)', action='store_true')
    list_exclusive_group.add_argument('-a', '--all', help='list all images', action='store_true')
    list_parser.add_argument('--no-trunc', help="don't truncate output", action='store_true')

    # tutum image inspect
    inspect_parser = image_subparser.add_parser('inspect', help='Inspect a image', description='Inspect a image')
    inspect_parser.add_argument('identifier', help="image name", nargs='+')

    # tutum image register
    register_parser = image_subparser.add_parser('register',
                                                 help='Register an image from a private repository in Tutum',
                                                 description='Register an image from a private repository in Tutum')
    register_parser.add_argument('image_name', help='full image name, i.e. quay.io/tutum/test-repo')
    register_parser.add_argument('-d', '--description', help='Image description')
    register_parser.add_argument('-u', '--username', help='Username of the private registry')
    register_parser.add_argument('-p', '--password', help='Password of the private registry')
    register_parser.add_argument('--sync', help='block the command until the async operation has finished',
                                 action='store_true')

    # tutum image push
    push_parser = image_subparser.add_parser('push', help='Deprecated. Please use "docker push" instead',
                                             description='Deprecated. Please use "docker push" instead')
    push_parser.add_argument('name', help='name of the image to push')
    push_parser.add_argument('--public', help='push image to public registry', action='store_true')

    # tutum image rm
    rm_parser = image_subparser.add_parser('rm', help='Deregister a private image from Tutum',
                                           description='Deregister a private image from Tutum')
    rm_parser.add_argument('image_name', help='full image name, i.e. quay.io/tutum/test-repo', nargs='+')
    rm_parser.add_argument('--sync', help='block the command until the async operation has finished',
                           action='store_true')

    # tutum image search
    search_parser = image_subparser.add_parser('search', help='Search for images in the Docker Index',
                                               description='Search for images in the Docker Index')
    search_parser.add_argument('query', help='query to search')

    # tutum image update
    update_parser = image_subparser.add_parser('update', help='Update a private image',
                                               description='Update a private image')
    update_parser.add_argument("image_name", help="full image name, i.e. quay.io/tutum/test-repo", nargs="+")
    update_parser.add_argument('-u', '--username', help='new username to authenticate with the registry')
    update_parser.add_argument('-p', '--password', help='new password to authenticate with the registry')
    update_parser.add_argument('-d', '--description', help='new image description')
    update_parser.add_argument('--sync', help='block the command until the async operation has finished',
                               action='store_true')


def add_node_parser(subparsers):
    # tutum node
    node_parser = subparsers.add_parser('node', help='Node-related operations', description='Node-related operations')
    node_subparser = node_parser.add_subparsers(title='tutum node commands', dest='subcmd')

    # tutum byo
    node_subparser.add_parser('byo', help='Instructions on how to Bring Your Own server to Tutum',
                              description='Instructions on how to Bring Your Own server to Tutum')

    # tutum node inspect
    inspect_parser = node_subparser.add_parser('inspect', help='Inspect a node', description='Inspect a node')
    inspect_parser.add_argument('identifier', help="node's UUID (either long or short)", nargs='+')

    # tutum node list
    list_parser = node_subparser.add_parser('list', help='List nodes', description='List nodes')
    list_parser.add_argument('-q', '--quiet', help='print only node uuid', action='store_true')

    # tutum node rm
    rm_parser = node_subparser.add_parser('rm', help='Remove a node', description='Remove a container')
    rm_parser.add_argument('identifier', help="node's UUID (either long or short)", nargs='+')
    rm_parser.add_argument('--sync', help='block the command until the async operation has finished',
                           action='store_true')

    # tutum node upgrade
    upgrade_parser = node_subparser.add_parser('upgrade', help='Upgrade docker daemon on the node',
                                               description='Upgrade docker daemon to the latest version on the node')
    upgrade_parser.add_argument('identifier', help="node's UUID (either long or short)", nargs='+')
    upgrade_parser.add_argument('--sync', help='block the command until the async operation has finished',
                                action='store_true')

    # tutum node healthcheck
    healthcheck_parser = node_subparser.add_parser('healthcheck', help='Test connectivity between Tutum and the node. '
                                                                       'Updates the node status to Deployed if the check was successful, or to Unreachable otherwise')
    healthcheck_parser.add_argument('identifier', help="node's UUID (either long or short)", nargs='+')


def add_nodecluster_parser(subparsers):
    # tutum nodecluster
    nodecluster_parser = subparsers.add_parser('nodecluster', help='NodeCluster-related operations',
                                               description='NodeCluster-related operations')
    nodecluster_subparser = nodecluster_parser.add_subparsers(title='tutum node commands', dest='subcmd')

    # tutum nodecluster create
    create_parser = nodecluster_subparser.add_parser('create', help='Create a nodecluster',
                                                     description='Create a nodecluster')
    create_parser.add_argument('-t', '--target-num-nodes',
                               help='the target number of nodes to run for this cluster (default: 1)', type=int)
    create_parser.add_argument('name', help='name of the node cluster to create')
    create_parser.add_argument('provider', help='name of the provider')
    create_parser.add_argument('region', help='name of the region')
    create_parser.add_argument('nodetype', help='name of the node type')
    create_parser.add_argument('--sync', help='block the command until the async operation has finished',
                               action='store_true')
    create_parser.add_argument('--disk', help="Disk size of node in GB(Default:60). "
                                              "The available value varies depending on the providers")
    create_parser.add_argument('--tag', help="set the tag of the node cluster", action='append')
    create_parser.add_argument('--aws-vpc-id', help='aws provider option: vpc id')
    create_parser.add_argument('--aws-vpc-subnet', help="aws provider option: vpc subnet",
                               action='append')
    create_parser.add_argument('--aws-vpc-security-group', help="aws provider option: vpc security group",
                               action='append')
    create_parser.add_argument('--aws-iam-instance-profile-name',
                               help='aws provider option: instance profile name for the iam')

    # tutum nodecluster inspect
    inspect_parser = nodecluster_subparser.add_parser('inspect', help='Inspect a nodecluster',
                                                      description='Inspect a nodecluster')
    inspect_parser.add_argument('identifier', help="node's UUID (either long or short)", nargs='+')

    # tutum nodecluster list
    list_parser = nodecluster_subparser.add_parser('list', help='List node clusters', description='List node clusters')
    list_parser.add_argument('-q', '--quiet', help='print only node uuid', action='store_true')

    # tutum nodecluster rm
    rm_parser = nodecluster_subparser.add_parser('rm', help='Remove node clusters', description='Remove node clusters')
    rm_parser.add_argument('identifier', help="node's UUID (either long or short)", nargs='+')
    rm_parser.add_argument('--sync', help='block the command until the async operation has finished',
                           action='store_true')

    # tutum nodecluster scale
    scale_parser = nodecluster_subparser.add_parser('scale', help='Scale a running node cluster',
                                                    description='Scale a running node cluster', )
    scale_parser.add_argument('identifier', help="node cluster's UUID (either long or short) or name", nargs='+')
    scale_parser.add_argument("target_num_nodes", metavar="target-num-nodes",
                              help="target number of nodes to scale this node cluster to", type=int)
    scale_parser.add_argument('--sync', help='block the command until the async operation has finished',
                              action='store_true')

    # tutum nodecluster provider
    provider_parser = nodecluster_subparser.add_parser('provider', help='Show all available infrastructure providers',
                                                       description='Show all available infrastructure providers')
    provider_parser.add_argument('-q', '--quiet', help='print only provider name', action='store_true')

    # tutum nodecluster region
    region_parser = nodecluster_subparser.add_parser('region', help='Show all available regions')
    region_parser.add_argument('-p', '--provider', help="filtered by provider name (e.g. digitalocean)")

    # tutum nodecluster nodetype
    nodetype_parser = nodecluster_subparser.add_parser('nodetype', help='Show all available types')
    nodetype_parser.add_argument('-p', '--provider', help="filtered by provider name (e.g. digitalocean)")
    nodetype_parser.add_argument('-r', '--region', help="filtered by region name (e.g. ams1)")

    # tutum nodecluster az
    az_parser = nodecluster_subparser.add_parser('az', help='Show all available availability zones')
    az_parser.add_argument('-q', '--quiet', help='print only avaialbity zone name', action='store_true')

    # tutum nodecluster upgrade
    upgrade_parser = nodecluster_subparser.add_parser('upgrade',
                                                      help='Upgrade docker daemon on all the nodes in the node cluster',
                                                      description='Upgrade docker daemon on all the '
                                                                  'nodes in the node cluster')
    upgrade_parser.add_argument('identifier', help="node's UUID (either long or short)", nargs='+')
    upgrade_parser.add_argument('--sync', help='block the command until the async operation has finished',
                                action='store_true')


def add_tag_parser(subparsers):
    # tutum tag
    tag_parser = subparsers.add_parser('tag', help='Tag-related operations', description='Tag-related operations')
    tag_subparser = tag_parser.add_subparsers(title='tutum tag commands', dest='subcmd')

    # tutum tag add
    add_parser = tag_subparser.add_parser('add', help='Add tags to services, nodes or nodeclusters',
                                          description='Add tags to services, nodes or nodeclusters')
    add_parser.add_argument('-t', '--tag', help="name of the tag", action='append', required=True)
    add_parser.add_argument('identifier', help="UUID or name of services, nodes or nodeclusters", nargs='+')

    # tutum tag list
    list_parser = tag_subparser.add_parser('list', help='List all tags associated with services, nodes or nodeclusters',
                                           description='List all tags associated with services, nodes or nodeclusters')
    list_parser.add_argument('identifier', help="UUID or name of services, nodes or nodeclusters", nargs='+')
    list_parser.add_argument('-q', '--quiet', help='print only tag names', action='store_true')

    # tutum tag rm
    rm_parser = tag_subparser.add_parser('rm', help='Remove tags from services, nodes or nodeclusters',
                                         description='Remove tags from services, nodes or nodeclusters')
    rm_parser.add_argument('-t', '--tag', help="name of the tag", action='append', required=True)
    rm_parser.add_argument('identifier', help="UUID or name of services, nodes or nodeclusters", nargs='+')

    # tutum tag set
    set_parser = tag_subparser.add_parser('set', help='Set tags from services, nodes or nodeclusters, '
                                                      'overwriting existing tags',
                                          description='Set tags from services, nodes or nodeclusters. '
                                                      'This will remove all the existing tags')
    set_parser.add_argument('-t', '--tag', help="name of the tag", action='append', required=True)
    set_parser.add_argument('identifier', help="UUID or name of services, nodes or nodeclusters", nargs='+')


def add_volume_parser(subparsers):
    # tutum volume
    volume_parser = subparsers.add_parser('volume', help='Volume-related operations',
                                          description='Volume-related operations')
    volume_subparser = volume_parser.add_subparsers(title='tutum volume commands', dest='subcmd')

    # tutum volume inspect
    inspect_parser = volume_subparser.add_parser('inspect', help='Inspect a volume', description='Inspect a volume')
    inspect_parser.add_argument('identifier', help="volume's UUID (either long or short)", nargs='+')

    # tutum volume list
    list_parser = volume_subparser.add_parser('list', help='List volumes', description='List volumes')
    list_parser.add_argument('-q', '--quiet', help='print only long UUIDs', action='store_true')


def add_volumegroup_parser(subparsers):
    # tutum volumegroup
    volumegroup_parser = subparsers.add_parser('volumegroup', help='VolumeGroup-related operations',
                                               description='VolumeGroup-related operations')
    volumegroup_subparser = volumegroup_parser.add_subparsers(title='tutum volumegroup commands', dest='subcmd')

    # tutum volumegroup inspect
    inspect_parser = volumegroup_subparser.add_parser('inspect', help='Inspect a volume group',
                                                      description='Inspect a volume group')
    inspect_parser.add_argument('identifier', help="volume group's UUID (either long or short) or name", nargs='+')

    # tutum volumegroup list
    list_parser = volumegroup_subparser.add_parser('list', help='List volume groups', description='List volume groups')
    list_parser.add_argument('-q', '--quiet', help='print only long UUIDs', action='store_true')


def add_trigger_parser(subparsers):
    # tutum trigger
    trigger_parser = subparsers.add_parser('trigger', help='Trigger-related operations',
                                           description='Trigger-related operations')
    trigger_subparser = trigger_parser.add_subparsers(title='tutum trigger commands', dest='subcmd')

    # tutum trigger create
    create_parser = trigger_subparser.add_parser('create', help='Create trigger to services',
                                                 description='Create trigger to services')
    create_parser.add_argument('-n', '--name', help="name of the trigger (optional)")
    create_parser.add_argument('-o', '--operation', help="operation of the trigger(default:redeploy)")
    create_parser.add_argument('identifier', help="UUID or name of services")

    # tutum ttrigger list
    list_parser = trigger_subparser.add_parser('list', help='List all trigger associated with services',
                                               description='List all triggers associated with services')
    list_parser.add_argument('identifier', help="UUID or name of services")
    list_parser.add_argument('-q', '--quiet', help='print only trigger uuid', action='store_true')

    # tutum trigger delete
    rm_parser = trigger_subparser.add_parser('rm', help='Remove trigger from a service',
                                             description='Remove trigger from a service')
    rm_parser.add_argument('identifier', help="UUID or name of services")
    rm_parser.add_argument('trigger', help="UUID or name of the trigger", nargs='+')


def add_stack_parser(subparsers):
    # tutum stack
    stack_parser = subparsers.add_parser('stack', help='Stack-related operations',
                                         description='Stack-related operations')
    stack_subparser = stack_parser.add_subparsers(title='tutum stack commands', dest='subcmd')

    # tutum stack create
    create_parser = stack_subparser.add_parser('create', help='Create a new stack without deploying',
                                               description='Create a new stack without deploying')
    create_parser.add_argument('-n', '--name', help='The name of the stack, which wil be shown in tutum')
    create_parser.add_argument('-f', '--file', help="the name of the Stackfile")
    create_parser.add_argument('--sync', help='block the command until the async operation has finished',
                               action='store_true')

    # tutum stack export
    export_parser = stack_subparser.add_parser('export', help='Export the stack from tutum',
                                               description='Export the stack from tutum')
    export_parser.add_argument('identifier', help='UUID or name of the stack')
    export_parser.add_argument('-f', '--file', help="the name of the file to export to")

    # tutum stack inspect
    inspect_parser = stack_subparser.add_parser('inspect', help='Inspect a stack', description='Inspect a stack')
    inspect_parser.add_argument('identifier', help="stack's UUID (either long or short) or name", nargs='+')

    # tutum stack list
    list_parser = stack_subparser.add_parser('list', help='List stacks', description='List stacks')
    list_parser.add_argument('-q', '--quiet', help='print only long UUIDs', action='store_true')

    # tutum stack redeploy
    redeploy_parser = stack_subparser.add_parser('redeploy', help='Redeploy a running stack',
                                                 description='Redeploy a running stack')
    redeploy_parser.add_argument('identifier', help="stack's UUID (either long or short) or name", nargs='+')
    redeploy_parser.add_argument('--not-reuse-volumes', help="do not reuse volumes in redeployment",
                                 action='store_true')
    redeploy_parser.add_argument('--sync', help='block the command until the async operation has finished',
                                 action='store_true')

    # tutum stack start
    start_parser = stack_subparser.add_parser('start', help='Start a stack', description='Start a stack')
    start_parser.add_argument('identifier', help="stack's UUID (either long or short) or name", nargs='+')
    start_parser.add_argument('--sync', help='block the command until the async operation has finished',
                              action='store_true')

    # tutum stack stop
    stop_parser = stack_subparser.add_parser('stop', help='Stop a stack', description='Stop a stack')
    stop_parser.add_argument('identifier', help="stack's UUID (either long or short) or name", nargs='+')
    stop_parser.add_argument('--sync', help='block the command until the async operation has finished',
                             action='store_true')

    # tutum stack terminate
    terminate_parser = stack_subparser.add_parser('terminate', help='Terminate a stack',
                                                  description='Terminate a stack')
    terminate_parser.add_argument('identifier', help="stack's UUID (either long or short) or name", nargs='+')
    terminate_parser.add_argument('--sync', help='block the command until the async operation has finished',
                                  action='store_true')

    # tutum stack up
    up_parser = stack_subparser.add_parser('up', help='Create and deploy a stack',
                                           description='Create and deploy a stack')
    up_parser.add_argument('-n', '--name', help='The name of the stack, which will be shown in tutum')
    up_parser.add_argument('-f', '--file', help="the name of the Stackfile")
    up_parser.add_argument('--sync', help='block the command until the async operation has finished',
                           action='store_true')

    # tutum stack update
    update_parser = stack_subparser.add_parser('update', help='Update a stack', description='Update a stack')
    update_parser.add_argument('identifier', help="stack's UUID (either long or short) or name")
    update_parser.add_argument('-f', '--file', help="the name of the Stackfile")
    update_parser.add_argument('--sync', help='block the command until the async operation has finished',
                               action='store_true')
