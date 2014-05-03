def add_login_parser(subparsers):
    # tutum login
    subparsers.add_parser('login', help='Login into Tutum', description='Login into Tutum')


def add_build_parser(subparsers):
    # tutum build
    build_parser = subparsers.add_parser('build', help='Build an image', description='Build an image')
    build_parser.add_argument('name', help='image name')
    build_parser.add_argument('-d', '--directory', help='working directory', default='.')
    build_parser.add_argument('-q', '--quiet', help='print minimum information', action='store_true')
    build_parser.add_argument('--nocache', help='do not use the cache when building the image', action='store_true')


def add_apps_parser(subparsers):
    # tutum apps
    apps_parser = subparsers.add_parser('apps', help='Applications related operations',
                                        description='Applications related operations')
    apps_subparser = apps_parser.add_subparsers(title='tutum apps commands', dest='subcmd')

    # tutum apps alias
    alias_parser = apps_subparser.add_parser('alias',
                                             help="Change application's dns (only for Tutum applications)",
                                             description="Change application's dns (only for Tutum applications)")
    alias_parser.add_argument('identifier', help="application's uuid (either long or short) or name", nargs='+')
    alias_parser.add_argument('dns', help='custom domain to use for this web application')

    # tutum apps inspect
    inspect_parser = apps_subparser.add_parser('inspect', help='Inspect an application',
                                               description='Inspect an application')
    inspect_parser.add_argument('identifier', help="application's uuid (either long or short) or name", nargs='+')

    # tutum apps logs
    logs_parser = apps_subparser.add_parser('logs', help='Get logs from an application',
                                            description='Get logs from an application')
    logs_parser.add_argument('identifier', help="application's uuid (either long or short) or name", nargs='+')

    # tutum apps open
    apps_subparser.add_parser('open', help='Open last web application created in Tutum',
                              description='Open last web application created in Tutum', )

    # tutum apps ps
    ps_parser = apps_subparser.add_parser('ps', help='List applications', description='List applications')
    ps_parser.add_argument('-q', '--quiet', help='print only long uuids', action='store_true')
    ps_parser.add_argument('-s', '--status', help='filter applications by status',
                           choices=['Running', 'Partly running', 'Stopped', 'Start failed', 'Stopped with errors'])

    # tutum apps redeploy
    redeploy_parser = apps_subparser.add_parser('redeploy', help='Redeploy an application ',
                                                description='Redeploy an application')
    redeploy_parser.add_argument('identifier', help="application's uuid (either long or short) or name", nargs='+')
    redeploy_parser.add_argument('-t', '--tag', help='tag of the image')

    # tutum apps run
    run_parser = apps_subparser.add_parser('run', help='Create and run an application',
                                           description='Create and run an application', )
    run_parser.add_argument('image', help='the image used to deploy this application in docker format')
    run_parser.add_argument('-n', '--name', help='a human-readable name for the application '
                                                 '(default: image_tag without namespace)')
    run_parser.add_argument('-s', '--container_size', help='the size of the application containers '
                                                           '(default: XS, possible values: XS, S, M, L, XL)',
                            default='XS')
    run_parser.add_argument('-t', '--target_num_containers',
                            help='the number of containers to run for this application (default: 1)', type=int,
                            default=1)
    run_parser.add_argument('-r', '--run_command',
                            help='the command used to start the application containers '
                                 '(default: as defined in the image)')
    run_parser.add_argument('--entrypoint',
                            help='the command prefix used to start the application containers '
                                 '(default: as defined in the image)')
    run_parser.add_argument('-p', '--port',
                            help='set ports i.e. "80/tcp" (default: as defined in the image)', action='append')
    run_parser.add_argument('-e', '--env',
                            help='set environment variables i.e. "ENVVAR=foo" '
                                 '(default: as defined in the image, plus any link- or role-generated variables)',
                            action='append')
    run_parser.add_argument('-l', '--link',
                            help="an application's uuid (either long or short) or name to link this application "
                                 "to, i.e. 80ff1635-2d56-478d-a97f-9b59c720e513'] (default: none)", action='append')
    run_parser.add_argument('--autorestart', help='whether the containers should be restarted if they stop '
                                                  '(default: OFF)', choices=['OFF', 'ON_FAILURE', 'ALWAYS'])
    run_parser.add_argument('--autoreplace', help='whether the containers should be replaced with a new one if '
                                                  'they stop (default: OFF)', choices=['OFF', 'ON_FAILURE', 'ALWAYS'])
    run_parser.add_argument('--autodestroy', help='whether the containers should be terminated if '
                                                  'they stop (default: OFF)', choices=['OFF', 'ON_FAILURE', 'ALWAYS'])
    run_parser.add_argument('--role', help='Tutum API roles to grant the application, '
                                           'i.e. "global" (default: none, possible values: "global"', action='append')
    run_parser.add_argument('-P', '--parallel', help='run the application in parallel', action='store_true')

    # tutum apps scale
    scale_app_parser = apps_subparser.add_parser('scale', help='Scale an application',
                                                 description='Scale an application', )
    scale_app_parser.add_argument('identifier', help="application's uuid (either long or short) or name", nargs='+')
    scale_app_parser.add_argument("target_num_containers",
                                  help="target number of containers to scale this application to", type=int)
    # tutum apps set
    set_parser = apps_subparser.add_parser('set', help='Set crash-recovery and auto-destroy of Turum applications',
                                           description='Set crash-recovery and auto-destroy of Turum applications')
    set_parser.add_argument('identifier', help="application's uuid (either long or short) or name", nargs='+')
    set_parser.add_argument('--autorestart', help="whether the containers should be restarted if they stop "
                                                  "(default: OFF)", choices=['OFF', 'ON_FAILURE', 'ALWAYS'])
    set_parser.add_argument('--autoreplace', help="whether the containers should be replaced with a new one if "
                                                  "they stop (default: OFF)", choices=['OFF', 'ON_FAILURE', 'ALWAYS'])
    set_parser.add_argument('--autodestroy',
                            help="whether the containers should be terminated if they stop (default: OFF)",
                            choices=['OFF', 'ON_FAILURE', 'ALWAYS'])

    # tutum apps start
    start_parser = apps_subparser.add_parser('start', help='Start an application', description='Start an application')
    start_parser.add_argument('identifier', help="application's uuid (either long or short) or name", nargs='+')

    # tutum apps stop
    stop_parser = apps_subparser.add_parser('stop', help='Stop an application', description='Stop an application')
    stop_parser.add_argument('identifier', help="application's uuid (either long or short) or name", nargs='+')

    # tutum apps terminate
    terminate_parser = apps_subparser.add_parser('terminate', help='Terminate an application',
                                                 description='Terminate an application')
    terminate_parser.add_argument('identifier', help="application's uuid (either long or short) or name", nargs='+')


def add_containers_parser(subparsers):
    # tutum containers
    containers_parser = subparsers.add_parser('containers', help='Containers related operations',
                                              description='Containers related operations')
    containers_subparser = containers_parser.add_subparsers(title='tutum apps commands', dest='subcmd')

    # tutum containers inspect
    inspect_parser = containers_subparser.add_parser('inspect', help='Inspect a container',
                                                     description='Inspect a container')
    inspect_parser.add_argument('identifier', help="container's uuid (either long or short) or name", nargs='+')

    # tutum containers logs
    logs_parser = containers_subparser.add_parser('logs', help='Get logs from a container',
                                                  description='Get logs from a container')
    logs_parser.add_argument('identifier', help="application's uuid (either long or short) or name", nargs='+')

    # tutum containers ps
    ps_parser = containers_subparser.add_parser('ps', help='List containers', description='List containers')
    ps_parser.add_argument('-i', '--identifier', help="application's uuid (either long or short) or name")
    ps_parser.add_argument('-q', '--quiet', help='print only long uuids', action='store_true')
    ps_parser.add_argument('-s', '--status', help='filter containers by status',
                           choices=['Running', 'Stopped', 'Start failed', 'Stopped with errors'])

    # tutum containers start
    start_parser = containers_subparser.add_parser('start', help='Start a container', description='Start a container')
    start_parser.add_argument('identifier', help="container's uuid (either long or short) or name", nargs='+')

    # tutum containers stop
    stop_parser = containers_subparser.add_parser('stop', help='Stop a container', description='Stop a container')
    stop_parser.add_argument('identifier', help="container's uuid (either long or short) or name", nargs='+')

    # tutum containers terminate
    terminate_parser = containers_subparser.add_parser('terminate', help='Terminate a container',
                                                       description='Terminate a container')
    terminate_parser.add_argument('identifier', help="container's uuid (either long or short) or name", nargs='+')


def add_images_parser(subparsers):
    # tutum images
    images_parser = subparsers.add_parser('images', help='Image related operations',
                                          description='Image related operations')
    images_subparser = images_parser.add_subparsers(title='tutum images commands', dest='subcmd')

    # tutum images list
    list_parser = images_subparser.add_parser('list', help='List private images',
                                              description='List private images')
    list_parser.add_argument('-q', '--quiet', help='print only image names', action='store_true')

    list_exclusive_group = list_parser.add_mutually_exclusive_group()
    list_exclusive_group.add_argument('-j', '--jumpstarts', help='list jumpstart images', action='store_true')
    list_exclusive_group.add_argument('-l', '--linux', help='list linux images', action='store_true')

    # tutum images register
    register_parser = images_subparser.add_parser('register',
                                                  help='Register an image from a private repository to Tutum',
                                                  description='Register an image from a private repository to Tutum')
    register_parser.add_argument('repository', help='full image repository, i.e. quay.io/tutum/test-repo')
    register_parser.add_argument('-d', '--description', help='Image description')

    # tutum images push
    push_parser = images_subparser.add_parser('push', help='Push an image or a repository to Tutum registry',
                                              description='Push an image or a repository to Tutum registry')
    push_parser.add_argument('name', help='name of the image or the repository')
    push_parser.add_argument('--public', help='push image or repository to public registry', action='store_true')

    # tutum images rm
    rm_parser = images_subparser.add_parser('rm', help='Remove a private image', description='Remove a private image')
    rm_parser.add_argument('repository', help='full image repository, i.e. quay.io/tutum/test-repo', nargs='+')

    # tutum images search
    search_parser = images_subparser.add_parser('search', help='Search for images in the Docker Index',
                                                description='Search for images in the Docker Index')
    search_parser.add_argument('text', help='text to search')

    # tutum images update
    update_parser = images_subparser.add_parser('update', help='Update a private image',
                                                description='Update a private image')
    update_parser.add_argument("repository", help="Full image repository, i.e. quay.io/tutum/test-repo", nargs="+")
    update_parser.add_argument('-u', '--username', help='new username to authenticate with the registry')
    update_parser.add_argument('-p', '--password', help='new username password')
    update_parser.add_argument('-d', '--description', help='new image description')