import argparse


def add_login_parser(subparsers, parent_parser):
    login_parser = subparsers.add_parser('login', help='Login into Tutum', parents=[parent_parser])
    return login_parser


def add_apps_parser(subparsers, parent_parser):
    apps_parser = subparsers.add_parser('apps', help='List all applications', parents=[parent_parser])
    return apps_parser


def add_app_parser(subparsers, parent_parser):
    # App common options
    app_common_parser = argparse.ArgumentParser(add_help=False)
    app_common_parser.add_argument("identifier", help="Application's uuid (either long or short) or name")

    # App parser
    app_parser = subparsers.add_parser('app', help='Manage an app', parents=[parent_parser])

    # App commands
    app_subparsers = app_parser.add_subparsers(title="App commands", dest='app_command')
    inspect_app_parser = app_subparsers.add_parser('inspect', help='Inspect an application',
                                                   parents=[parent_parser, app_common_parser])
    start_app_parser = app_subparsers.add_parser('start', help='Start an application',
                                                 parents=[parent_parser, app_common_parser])
    stop_app_parser = app_subparsers.add_parser('stop', help='Stop an application',
                                                parents=[parent_parser, app_common_parser])
    terminate_app_parser = app_subparsers.add_parser('terminate', help='Terminate an application',
                                                     parents=[parent_parser, app_common_parser])
    logs_app_parser = app_subparsers.add_parser('logs', help='Get logs from an application',
                                                parents=[parent_parser, app_common_parser])
    update_app_parser = app_subparsers.add_parser('update', help='Update an application',
                                                  parents=[parent_parser, app_common_parser])
    update_app_parser.add_argument("--target_num_containers",
                                   help="target number of containers to scale this application to",
                                   type=int)
    update_app_parser.add_argument("--web_public_dns", help="custom domain to use for this web application")

    create_app_parser = app_subparsers.add_parser('create', help='Create an application', parents=[parent_parser])
    create_app_parser.add_argument("image", help="the image used to deploy this application in docker format")
    create_app_parser.add_argument("--name", help="a human-readable name for the application "
                                                  "(default: image_tag without namespace)")
    create_app_parser.add_argument("--container_size", help="the size of the application containers "
                                                            "(default: XS, possible values: XS, S, M, L, XL)")
    create_app_parser.add_argument("--target_num_containers", help="the number of containers to run "
                                                                   "for this application (default: 1)", type=int)
    create_app_parser.add_argument("--run_command",
                                   help="the command used to start the application containers "
                                        "(default: as defined in the image)")
    create_app_parser.add_argument("--entrypoint",
                                   help="the command prefix used to start the application containers "
                                        "(default: as defined in the image)")
    create_app_parser.add_argument("--container_ports",
                                   help="an array of objects with port information to be exposed in the application "
                                        "containers, i.e. [{'protocol': 'tcp', 'inner_port': 80}] "
                                        "(default: as defined in the image)")
    create_app_parser.add_argument("--container_envvars",
                                   help="an array of objects with environment variables to be set in the application "
                                        "containers on launch, i.e. [{'key': 'DB_PASSWORD', 'value': 'mypass'}] "
                                        "(default: as defined in the image, plus any link- or role-generated variables)")
    create_app_parser.add_argument("--linked_to_application",
                                   help="an array of application resource URIs to link this application to, "
                                        "i.e. ['/api/v1/application/80ff1635-2d56-478d-a97f-9b59c720e513/'] "
                                        "(default: empty array)")
    create_app_parser.add_argument('--autorestart', help="whether the containers should be restarted if they stop "
                                                         "(default: OFF)", choices=['OFF', 'ON_FAILURE', 'ALWAYS'])
    create_app_parser.add_argument('--autoreplace', help="whether the containers should be replaced with a new one if "
                                                         "they stop (default: OFF)",
                                   choices=['OFF', 'ON_FAILURE', 'ALWAYS'])
    create_app_parser.add_argument('--autodestroy', help="whether the containers should be terminated if "
                                                         "they stop (default: OFF)",
                                   choices=['OFF', 'ON_FAILURE', 'ALWAYS'])
    create_app_parser.add_argument('--roles', help="a list of Tutum API roles to grant the application, "
                                                   "i.e. ['global'] (default: empty array, possible values: 'global')")

    return app_parser


def add_containers_parser(subparsers, parent_parser):
    containers_parser = subparsers.add_parser('ps', help='List all containers', parents=[parent_parser])
    return containers_parser


def add_container_parser(subparsers, parent_parser):
    # Container common options
    container_common_parser = argparse.ArgumentParser(add_help=False)
    container_common_parser.add_argument("identifier", help="Container's uuid (either long or short) or name")

    # Container parser
    container_parser = subparsers.add_parser('container', help='Manage a container', parents=[parent_parser])

    # Container commands
    container_subparsers = container_parser.add_subparsers(title="Container commands", dest='container_command')
    inspect_container_parser = container_subparsers.add_parser('inspect', help='Inspect a container',
                                                               parents=[parent_parser, container_common_parser])
    start_container_parser = container_subparsers.add_parser('start', help='Start a container',
                                                             parents=[parent_parser, container_common_parser])
    stop_container_parser = container_subparsers.add_parser('stop', help='Stop a container',
                                                            parents=[parent_parser, container_common_parser])
    terminate_container_parser = container_subparsers.add_parser('terminate', help='Terminate a container',
                                                                 parents=[parent_parser, container_common_parser])
    logs_container_parser = container_subparsers.add_parser('logs', help='Get logs from a container',
                                                            parents=[parent_parser, container_common_parser])

    return container_parser
