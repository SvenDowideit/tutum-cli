def add_login_parser(subparsers):
    # tutum login
    subparsers.add_parser('login', help='Login into Tutum', description='Login into Tutum')


def add_build_parser(subparsers):
    # tutum build
    build_parser = subparsers.add_parser('build', help='Build an image using an existing Dockerfile, '
                                                       'or create one using buildstep',
                                         description='Build an image using an existing Dockerfile, '
                                                     'or create one using buildstep')
    build_parser.add_argument('-q', '--quiet', help='print minimum information', action='store_true')
    build_parser.add_argument('--no-cache', help='do not use the cache when building the image', action='store_true')
    build_parser.add_argument('-t', '--tag', help='repository name (and optionally a tag) to be applied '
                                                  'to the resulting image in case of success')
    build_parser.add_argument('directory', help='working directory')


def add_cluster_parser(subparsers):
    # tutum cluster
    cluster_parser = subparsers.add_parser('cluster', help='Cluster-related operations',
                                        description='Cluster-related operations')
    cluster_subparser = cluster_parser.add_subparsers(title='tutum cluster commands', dest='subcmd')

    # tutum cluster alias
    alias_parser = cluster_subparser.add_parser('alias',
                                             help="Set a custom FQDN (CNAME) to a running web cluster",
                                             description="Set a custom DNS record (CNAME) to a running web cluster")
    alias_parser.add_argument('identifier', help="cluster's UUID (either long or short) or name", nargs='+')
    alias_parser.add_argument('dns', help='custom FQDN to use for this web cluster')

    # tutum cluster inspect
    inspect_parser = cluster_subparser.add_parser('inspect', help="Get all details from an cluster",
                                               description="Get all details from an cluster")
    inspect_parser.add_argument('identifier', help="cluster's UUID (either long or short) or name", nargs='+')

    # tutum cluster logs
    logs_parser = cluster_subparser.add_parser('logs', help='Get logs from an cluster',
                                            description='Get logs from an cluster')
    logs_parser.add_argument('identifier', help="cluster's UUID (either long or short) or name", nargs='+')

    # tutum cluster open
    cluster_subparser.add_parser('open', help='Open last web cluster launched',
                              description='Open last web cluster launched', )

    # tutum cluster ps
    ps_parser = cluster_subparser.add_parser('ps', help='List clusters', description='List clusters')
    ps_parser.add_argument('-q', '--quiet', help='print only long UUIDs', action='store_true')
    ps_parser.add_argument('-s', '--status', help='filter clusters by status',
                           choices=['Running', 'Partly running', 'Stopped', 'Start failed', 'Stopped with errors'])

    # tutum cluster redeploy
    redeploy_parser = cluster_subparser.add_parser('redeploy', help='Redeploy a running cluster with a '
                                                                 'new version/tag',
                                                description='Redeploy a running cluster with a new version/tag')
    redeploy_parser.add_argument('identifier', help="cluster's UUID (either long or short) or name", nargs='+')
    redeploy_parser.add_argument('-t', '--tag', help='tag of the image to redeploy')

    # tutum cluster run
    run_parser = cluster_subparser.add_parser('run', help='Create and run a new cluster',
                                           description='Create and run a new cluster', )
    run_parser.add_argument('image', help='the name of the image used to deploy this cluster')
    run_parser.add_argument('-n', '--name', help='a human-readable name for the cluster '
                                                 '(default: image_tag without namespace)')
    run_parser.add_argument('-s', '--container-size', help='the size of the cluster containers '
                                                           '(default: XS, possible values: XS, S, M, L, XL)',
                            default='XS')
    run_parser.add_argument('-t', '--target-num-containers',
                            help='the number of containers to run for this cluster (default: 1)', type=int,
                            default=1)
    run_parser.add_argument('-r', '--run-command',
                            help='the command used to start the cluster containers '
                                 '(default: as defined in the image)')
    run_parser.add_argument('--entrypoint',
                            help='the command prefix used to start the cluster containers '
                                 '(default: as defined in the image)')
    run_parser.add_argument('-p', '--port',
                            help='set ports i.e. "80/tcp" (default: as defined in the image)', action='append')
    run_parser.add_argument('-e', '--env',
                            help='set environment variables i.e. "ENVVAR=foo" '
                                 '(default: as defined in the image, plus any link- or role-generated variables)',
                            action='append')
    run_parser.add_argument('--link-cluster',
                            help="Add link to another cluster (name:alias) or (uuid:alias)", action='append')
    run_parser.add_argument('--link-container',
                            help="Add link to another container (name:alias) or (uuid:alias)", action='append')
    run_parser.add_argument('--autorestart', help='whether the containers should be restarted if they stop '
                                                  '(default: OFF)', choices=['OFF', 'ON_FAILURE', 'ALWAYS'])
    run_parser.add_argument('--autoreplace', help='whether the containers should be replaced with a new one if '
                                                  'they stop (default: OFF)', choices=['OFF', 'ON_FAILURE', 'ALWAYS'])
    run_parser.add_argument('--autodestroy', help='whether the containers should be terminated if '
                                                  'they stop (default: OFF)', choices=['OFF', 'ON_FAILURE', 'ALWAYS'])
    run_parser.add_argument('--role', help='Tutum API roles to grant the cluster, '
                                           'i.e. "global" (default: none, possible values: "global")', action='append')
    run_parser.add_argument('--sequential', help='whether the containers should be launched and scaled sequentially',
                            action='store_true')
    run_parser.add_argument('--web-public-dns', help="Set your own web public dns")

    # tutum cluster scale
    scale_parser = cluster_subparser.add_parser('scale', help='Scale a running cluster',
                                                 description='Scale a running cluster', )
    scale_parser.add_argument('identifier', help="cluster's UUID (either long or short) or name", nargs='+')
    scale_parser.add_argument("target_num_containers", metavar="target-num-containers",
                                  help="target number of containers to scale this cluster to", type=int)
    # tutum cluster set
    set_parser = cluster_subparser.add_parser('set', help='Enable or disable Crash Recovery and Autodestroy features to '
                                                       'an existing cluster',
                                           description='Enable or disable Crash Recovery and Autodestroy features to '
                                                       'an existing cluster')
    set_parser.add_argument('identifier', help="cluster's UUID (either long or short) or name", nargs='+')
    set_parser.add_argument('--autorestart', help="whether the containers should be restarted if they stop "
                                                  "(default: OFF)", choices=['OFF', 'ON_FAILURE', 'ALWAYS'])
    set_parser.add_argument('--autoreplace', help="whether the containers should be replaced with a new one if "
                                                  "they stop (default: OFF)", choices=['OFF', 'ON_FAILURE', 'ALWAYS'])
    set_parser.add_argument('--autodestroy',
                            help="whether the containers should be terminated if they stop (default: OFF)",
                            choices=['OFF', 'ON_FAILURE', 'ALWAYS'])

    # tutum cluster start
    start_parser = cluster_subparser.add_parser('start', help='Start a stopped cluster',
                                             description='Start a stopped cluster')
    start_parser.add_argument('identifier', help="cluster's UUID (either long or short) or name", nargs='+')

    # tutum cluster stop
    stop_parser = cluster_subparser.add_parser('stop', help='Stop a running cluster',
                                            description='Stop a running cluster')
    stop_parser.add_argument('identifier', help="cluster's UUID (either long or short) or name", nargs='+')

    # tutum cluster terminate
    terminate_parser = cluster_subparser.add_parser('terminate', help='Terminate an cluster',
                                                 description='Terminate an cluster')
    terminate_parser.add_argument('identifier', help="cluster's UUID (either long or short) or name", nargs='+')


def add_container_parser(subparsers):
    # tutum container
    container_parser = subparsers.add_parser('container', help='Container-related operations',
                                              description='Container-related operations')
    container_subparser = container_parser.add_subparsers(title='tutum container commands', dest='subcmd')

    # tutum container inspect
    inspect_parser = container_subparser.add_parser('inspect', help='Inspect a container',
                                                     description='Inspect a container')
    inspect_parser.add_argument('identifier', help="container's UUID (either long or short) or name", nargs='+')

    # tutum container logs
    logs_parser = container_subparser.add_parser('logs', help='Get logs from a container',
                                                  description='Get logs from a container')
    logs_parser.add_argument('identifier', help="container's UUID (either long or short) or name", nargs='+')

    # tutum container ps
    ps_parser = container_subparser.add_parser('ps', help='List containers', description='List containers')
    ps_parser.add_argument('-i', '--identifier', help="container's UUID (either long or short) or name")
    ps_parser.add_argument('-q', '--quiet', help='print only long UUIDs', action='store_true')
    ps_parser.add_argument('-s', '--status', help='filter containers by status',
                           choices=['Running', 'Stopped', 'Start failed', 'Stopped with errors'])

    # tutum container redeploy
    redeploy_parser = container_subparser.add_parser('redeploy', help='Redeploy a running container with a '
                                                                 'new version/tag',
                                                description='Redeploy a running container with a new version/tag')
    redeploy_parser.add_argument('identifier', help="container's UUID (either long or short) or name", nargs='+')
    redeploy_parser.add_argument('-t', '--tag', help='tag of the image to redeploy')

    # tutum container run
    run_parser = container_subparser.add_parser('run', help='Create and run a new container',
                                           description='Create and run a new container', )
    run_parser.add_argument('image', help='the name of the image used to deploy this container')
    run_parser.add_argument('-n', '--name', help='a human-readable name for the container'
                                                 '(default: image_tag without namespace)')
    run_parser.add_argument('-s', '--container-size', help='the size of the container containers '
                                                           '(default: XS, possible values: XS, S, M, L, XL)',
                            default='XS')
    run_parser.add_argument('-t', '--target-num-containers',
                            help='the number of containers to run for this container (default: 1)', type=int,
                            default=1)
    run_parser.add_argument('-r', '--run-command',
                            help='the command used to start the container containers '
                                 '(default: as defined in the image)')
    run_parser.add_argument('--entrypoint',
                            help='the command prefix used to start the container containers '
                                 '(default: as defined in the image)')
    run_parser.add_argument('-p', '--port',
                            help='set ports i.e. "80/tcp" (default: as defined in the image)', action='append')
    run_parser.add_argument('-e', '--env',
                            help='set environment variables i.e. "ENVVAR=foo" '
                                 '(default: as defined in the image, plus any link- or role-generated variables)',
                            action='append')
    run_parser.add_argument('--link-cluster',
                            help="Add link to another cluster (name:alias) or (uuid:alias)", action='append')
    run_parser.add_argument('--link-container',
                            help="Add link to another container (name:alias) or (uuid:alias)", action='append')
    run_parser.add_argument('--autorestart', help='whether the containers should be restarted if they stop '
                                                  '(default: OFF)', choices=['OFF', 'ON_FAILURE', 'ALWAYS'])
    run_parser.add_argument('--autoreplace', help='whether the containers should be replaced with a new one if '
                                                  'they stop (default: OFF)', choices=['OFF', 'ON_FAILURE', 'ALWAYS'])
    run_parser.add_argument('--autodestroy', help='whether the containers should be terminated if '
                                                  'they stop (default: OFF)', choices=['OFF', 'ON_FAILURE', 'ALWAYS'])
    run_parser.add_argument('--role', help='Tutum API roles to grant the container, '
                                           'i.e. "global" (default: none, possible values: "global")', action='append')
    run_parser.add_argument('--sequential', help='whether the containers should be launched and scaled sequentially',
                            action='store_true')
    run_parser.add_argument('--web-public-dns', help="Set your own web public dns")

    # tutum container start
    start_parser = container_subparser.add_parser('start', help='Start a container', description='Start a container')
    start_parser.add_argument('identifier', help="container's UUID (either long or short) or name", nargs='+')

    # tutum container stop
    stop_parser = container_subparser.add_parser('stop', help='Stop a container', description='Stop a container')
    stop_parser.add_argument('identifier', help="container's UUID (either long or short) or name", nargs='+')

    # tutum container terminate
    terminate_parser = container_subparser.add_parser('terminate', help='Terminate a container',
                                                       description='Terminate a container')
    terminate_parser.add_argument('identifier', help="container's UUID (either long or short) or name", nargs='+')


def add_image_parser(subparsers):
    # tutum image
    image_parser = subparsers.add_parser('image', help='Image-related operations',
                                          description='Image-related operations')
    image_subparser = image_parser.add_subparsers(title='tutum image commands', dest='subcmd')

    # tutum image list
    list_parser = image_subparser.add_parser('list', help='List private images',
                                              description='List private images')
    list_parser.add_argument('-q', '--quiet', help='print only image names', action='store_true')

    list_exclusive_group = list_parser.add_mutually_exclusive_group()
    list_exclusive_group.add_argument('-j', '--jumpstarts', help='list jumpstart images', action='store_true')
    list_exclusive_group.add_argument('-l', '--linux', help='list linux images', action='store_true')

    # tutum image register
    register_parser = image_subparser.add_parser('register',
                                                  help='Register an image from a private repository in Tutum',
                                                  description='Register an image from a private repository in Tutum')
    register_parser.add_argument('image_name', help='full image name, i.e. quay.io/tutum/test-repo')
    register_parser.add_argument('-d', '--description', help='Image description')

    # tutum image push
    push_parser = image_subparser.add_parser('push', help='Push a local image to Tutum private registry',
                                              description='Push a local image to Tutum private registry')
    push_parser.add_argument('name', help='name of the image to push')
    push_parser.add_argument('--public', help='push image to public registry', action='store_true')

    # tutum image rm
    rm_parser = image_subparser.add_parser('rm', help='Deregister a private image from Tutum',
                                            description='Deregister a private image from Tutum')
    rm_parser.add_argument('image_name', help='full image name, i.e. quay.io/tutum/test-repo', nargs='+')

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