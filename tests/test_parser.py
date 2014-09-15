import unittest
import copy
import mock
import StringIO
import sys

from tutumcli.tutum_cli import patch_help_option, dispatch_cmds, initialize_parser
from tutumcli.exceptions import InternalError
import tutumcli


class PatchHelpOptionTestCase(unittest.TestCase):
    def setUp(self):
        self.add_help_argv_list = [
            ['tutum'],
            ['tutum', 'cluster'],
            ['tutum', 'cluster', 'alias'],
            ['tutum', 'cluster', 'inspect'],
            ['tutum', 'cluster', 'logs'],
            ['tutum', 'cluster', 'redeploy'],
            ['tutum', 'cluster', 'run'],
            ['tutum', 'cluster', 'scale'],
            ['tutum', 'cluster', 'set'],
            ['tutum', 'cluster', 'start'],
            ['tutum', 'cluster', 'stop'],
            ['tutum', 'cluster', 'terminate'],
            ['tutum', 'build'],
            ['tutum', 'container'],
            ['tutum', 'container', 'inspect'],
            ['tutum', 'container', 'logs'],
            ['tutum', 'container', 'redeploy'],
            ['tutum', 'container', 'run'],
            ['tutum', 'container', 'start'],
            ['tutum', 'container', 'stop'],
            ['tutum', 'container', 'terminate'],
            ['tutum', 'image'],
            ['tutum', 'image', 'register'],
            ['tutum', 'image', 'push'],
            ['tutum', 'image', 'rm'],
            ['tutum', 'image', 'search'],
            ['tutum', 'image', 'update'],
            ['tutum', 'node'],
            ['tutum', 'node', 'inspect'],
            ['tutum', 'node', 'rm'],
            ['tutum', 'nodecluster'],
            ['tutum', 'nodecluster', 'create'],
            ['tutum', 'nodecluster', 'inspect'],
            ['tutum', 'nodecluster', 'region'],
            ['tutum', 'nodecluster', 'nodetype'],
            ['tutum', 'nodecluster', 'rm'],
            ['tutum', 'nodecluster', 'scale'],
        ]
        self.not_add_help_argv_list = [
            ["tutum", "cluster", "ps"],
            ["tutum", "cluster", "open"],
            ["tutum", "container", "ps"],
            ["tutum", "image", "list"],
            ["tutum", "node", "list"],
            ["tutum", "nodecluster", "list"],
            ["tutum", "nodecluster", "provider"],
            ["tutum", "container", "run", "-p", "80:80", "tutum/wordpress"],
        ]

    def test_parser_with_empty_args(self):
        args = []
        self.assertRaises(InternalError, patch_help_option, args)

    def test_help_append(self):
        for argv in self.add_help_argv_list:
            args = patch_help_option(argv)
            target = copy.copy(argv[1:])
            target.append('-h')
            self.assertEqual(target, args, "Help option not patch correctly: %s" % argv)

    def test_help_not_append(self):
        for argv in self.not_add_help_argv_list:
            args = patch_help_option(argv)
            self.assertEqual(argv[1:], args, "Should not patch help option correctly: %s" % argv)

    def test_help_append_with_debug_option(self):
        argvlist = copy.copy(self.add_help_argv_list)
        for argv in argvlist:
            argv.insert(1, "--debug")
            args = patch_help_option(argv)
            target = copy.copy(argv[1:])
            target.append('-h')
            self.assertEqual(target, args, "Help option not patch correctly: %s" % argv)

    def test_help_not_append_with_debug_option(self):
        argvlist = copy.copy(self.not_add_help_argv_list)
        for argv in argvlist:
            argv.insert(1, "--debug")
            args = patch_help_option(argv)
            self.assertEqual(argv[1:], args, "Should not patch help option correctly: %s" % argv)


class CommandsDispatchTestCase(unittest.TestCase):
    def setUp(self):
        self.parser = tutumcli.tutum_cli.initialize_parser()

    @mock.patch('tutumcli.tutum_cli.commands')
    def test_login_dispatch(self, mock_cmds):
        args = self.parser.parse_args(['login'])
        dispatch_cmds(args)
        mock_cmds.login.assert_called_with()

    @mock.patch('tutumcli.tutum_cli.commands')
    def test_build_dispatch(self, mock_cmds):
        args = self.parser.parse_args(['build', '-t', 'mysql', '.'])
        dispatch_cmds(args)
        mock_cmds.build.assert_called_with(args.tag, args.directory, args.quiet, args.no_cache)

    @mock.patch('tutumcli.tutum_cli.commands')
    def test_cluster_dispatch(self, mock_cmds):
        args = self.parser.parse_args(['cluster', 'alias', 'id', 'dns'])
        dispatch_cmds(args)
        mock_cmds.cluster_alias.assert_called_with(args.identifier, args.dns)

        args = self.parser.parse_args(['cluster', 'inspect', 'id'])
        dispatch_cmds(args)
        mock_cmds.cluster_inspect.assert_called_with(args.identifier)

        args = self.parser.parse_args(['cluster', 'logs', 'id'])
        dispatch_cmds(args)
        mock_cmds.cluster_logs.assert_called_with(args.identifier)

        args = self.parser.parse_args(['cluster', 'open'])
        dispatch_cmds(args)
        mock_cmds.cluster_open.assert_called_with()

        args = self.parser.parse_args(['cluster', 'ps'])
        dispatch_cmds(args)
        mock_cmds.cluster_ps.assert_called_with(args.quiet, args.status)

        args = self.parser.parse_args(['cluster', 'redeploy', '-t', 'latest', 'mysql'])
        dispatch_cmds(args)
        mock_cmds.cluster_redeploy.assert_called_with(args.identifier, args.tag)

        args = self.parser.parse_args(['cluster', 'run', 'mysql'])
        dispatch_cmds(args)
        mock_cmds.cluster_run.assert_called_with(image=args.image, name=args.name, cpu_shares=args.cpushares,
                                                 memory=args.memory, memory_swap=args.memoryswap,
                                                 target_num_containers=args.target_num_containers,
                                                 run_command=args.run_command,
                                                 entrypoint=args.entrypoint, container_ports=args.port,
                                                 container_envvars=args.env,
                                                 linked_to_cluster=args.link_cluster,
                                                 linked_to_container=args.link_container,
                                                 autorestart=args.autorestart,
                                                 autoreplace=args.autoreplace, autodestroy=args.autodestroy,
                                                 roles=args.role,
                                                 sequential=args.sequential, web_public_dns=args.web_public_dns)

        args = self.parser.parse_args(['cluster', 'scale', 'id', '3'])
        dispatch_cmds(args)
        mock_cmds.cluster_scale.assert_called_with(args.identifier, args.target_num_containers)

        args = self.parser.parse_args(['cluster', 'set', 'id'])
        dispatch_cmds(args)
        mock_cmds.cluster_set.assert_called_with(args.autorestart, args.autoreplace, args.autodestroy, args.identifier)

        args = self.parser.parse_args(['cluster', 'start', 'id'])
        dispatch_cmds(args)
        mock_cmds.cluster_start.assert_called_with(args.identifier)

        args = self.parser.parse_args(['cluster', 'stop', 'id'])
        dispatch_cmds(args)
        mock_cmds.cluster_stop.assert_called_with(args.identifier)

        args = self.parser.parse_args(['cluster', 'terminate', 'id'])
        dispatch_cmds(args)
        mock_cmds.cluster_terminate.assert_called_with(args.identifier)

    @mock.patch('tutumcli.tutum_cli.commands')
    def test_container_dispatch(self, mock_cmds):
        args = self.parser.parse_args(['container', 'inspect', 'id'])
        dispatch_cmds(args)
        mock_cmds.container_inspect.assert_called_with(args.identifier)

        args = self.parser.parse_args(['container', 'logs', 'id'])
        dispatch_cmds(args)
        mock_cmds.container_logs.assert_called_with(args.identifier)

        args = self.parser.parse_args(['container', 'ps'])
        dispatch_cmds(args)
        mock_cmds.container_ps.assert_called_with(args.identifier, args.quiet, args.status)

        args = self.parser.parse_args(['container', 'redeploy', '-t', 'latest', 'mysql'])
        dispatch_cmds(args)
        mock_cmds.container_redeploy.assert_called_with(args.identifier, args.tag)

        args = self.parser.parse_args(['container', 'run', 'mysql'])
        dispatch_cmds(args)
        mock_cmds.container_run.assert_called_with(image=args.image, name=args.name, cpu_shares=args.cpushares,
                                                   memory=args.memory, memory_swap=args.memoryswap,
                                                   run_command=args.run_command, entrypoint=args.entrypoint,
                                                   container_ports=args.port,
                                                   container_envvars=args.env,
                                                   linked_to_cluster=args.link_cluster,
                                                   linked_to_container=args.link_container,
                                                   autorestart=args.autorestart, autoreplace=args.autoreplace,
                                                   autodestroy=args.autodestroy,
                                                   roles=args.role, web_public_dns=args.web_public_dns)

        args = self.parser.parse_args(['container', 'start', 'id'])
        dispatch_cmds(args)
        mock_cmds.container_start.assert_called_with(args.identifier)

        args = self.parser.parse_args(['container', 'stop', 'id'])
        dispatch_cmds(args)
        mock_cmds.container_stop.assert_called_with(args.identifier)

        args = self.parser.parse_args(['container', 'terminate', 'id'])
        dispatch_cmds(args)
        mock_cmds.container_terminate.assert_called_with(args.identifier)

    @mock.patch('tutumcli.tutum_cli.commands')
    def test_image_dispatch(self, mock_cmds):
        args = self.parser.parse_args(['image', 'list'])
        dispatch_cmds(args)
        mock_cmds.image_list.assert_called_with(args.quiet, args.jumpstarts, args.linux)

        args = self.parser.parse_args(['image', 'register', 'name'])
        dispatch_cmds(args)
        mock_cmds.image_register(args.image_name, args.description)

        args = self.parser.parse_args(['image', 'push', 'name'])
        dispatch_cmds(args)
        mock_cmds.image_push(args.name, args.public)

        args = self.parser.parse_args(['image', 'rm', 'name'])
        dispatch_cmds(args)
        mock_cmds.image_rm(args.image_name)

        args = self.parser.parse_args(['image', 'search', 'name'])
        dispatch_cmds(args)
        mock_cmds.image_search(args.query)

        args = self.parser.parse_args(['image', 'update', 'name'])
        dispatch_cmds(args)
        mock_cmds.image_update(args.image_name, args.username, args.password, args.description)

    @mock.patch('tutumcli.tutum_cli.commands')
    def test_node_dispatch(self, mock_cmds):
        args = self.parser.parse_args(['node', 'inspect', 'id'])
        dispatch_cmds(args)
        mock_cmds.node_inspect.assert_called_with(args.identifier)

        args = self.parser.parse_args(['node', 'list'])
        dispatch_cmds(args)
        mock_cmds.node_list(args.quiet)

        args = self.parser.parse_args(['node', 'rm', 'id'])
        dispatch_cmds(args)
        mock_cmds.node_rm(args.identifier)

    @mock.patch('tutumcli.tutum_cli.commands')
    def test_nodecluste_dispatch(self, mock_cmds):
        args = self.parser.parse_args(['nodecluster', 'create', 'name', '1', '2', '3'])
        dispatch_cmds(args)
        mock_cmds.nodecluster_create(args.target_num_nodes, args.name,
                                     args.provider_id, args.region_id, args.nodetype_id)

        args = self.parser.parse_args(['nodecluster', 'inspect', 'id'])
        dispatch_cmds(args)
        mock_cmds.nodecluster_inspect(args.identifier)

        args = self.parser.parse_args(['nodecluster', 'list'])
        dispatch_cmds(args)
        mock_cmds.nodecluster_list(args.quiet)

        args = self.parser.parse_args(['nodecluster', 'provider'])
        dispatch_cmds(args)
        mock_cmds.nodecluster_show_providers(args.quiet)

        args = self.parser.parse_args(['nodecluster', 'region', '3'])
        dispatch_cmds(args)
        mock_cmds.nodecluster_show_regions(args.provider_id)

        args = self.parser.parse_args(['nodecluster', 'nodetype', '3'])
        dispatch_cmds(args)
        mock_cmds.nodecluster_show_types(args.region_id)

        args = self.parser.parse_args(['nodecluster', 'rm', 'id'])
        dispatch_cmds(args)
        mock_cmds.nodecluster_rm(args.identifier)

        args = self.parser.parse_args(['nodecluster', 'scale', 'id', '3'])
        dispatch_cmds(args)
        mock_cmds.nodecluster_scale(args.identifier, args.target_num_nodes)


class ParserTestCase(unittest.TestCase):
    def setUp(self):
        self.stdout = sys.stdout
        self.stderr = sys.stderr


    def tearDown(self):
        sys.stdout = self.stdout
        sys.stdout = self.stderr

    def compare_output(self, output, args, stdout=True):
        parser = initialize_parser()
        argv = patch_help_option(args)

        if stdout:
            sys.stdout = buf = StringIO.StringIO()
        else:
            sys.stderr = buf = StringIO.StringIO()
        parser.parse_args(argv)
        sys.stdout = self.stdout
        sys.stderr = self.stderr

        out = buf.getvalue()
        self.assertEqual(' '.join(output.split()), ' '.join(out.split()))

    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum(self, mock_exit):
        output = '''usage: tutum [-h] [-v]
             {build,container,cluster,image,login,node,nodecluster} ...

Tutum's CLI

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit

Tutum's CLI commands:
  {build,container,cluster,image,login,node,nodecluster}
    build               Build an image using an existing Dockerfile, or create
                        one using buildstep
    container           Container-related operations
    cluster             Cluster-related operations
    image               Image-related operations
    login               Login into Tutum
    node                Node-related operations
    nodecluster         NodeCluster-related operations'''
        self.compare_output(output, args=['tutum', '-h'])

    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.add_argument')
    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_version(self, mock_exit, mock_add_arg):
        initialize_parser()
        mock_add_arg.assert_any_call('-v', '--version', action='version', version='%(prog)s ' + tutumcli.__version__)


    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_build(self, mock_exit):
        output = '''usage: tutum build [-h] [-q] [--no-cache] [-t TAG] directory

Build an image using an existing Dockerfile, or create one using buildstep

positional arguments:
  directory          working directory

optional arguments:
  -h, --help         show this help message and exit
  -q, --quiet        print minimum information
  --no-cache         do not use the cache when building the image
  -t TAG, --tag TAG  repository name (and optionally a tag) to be applied to
                     the resulting image in case of success'''
        self.compare_output(output, args=['tutum', 'build', '-h'])

    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_container(self, mock_exit):
        output = '''usage: tutum container [-h]
                       {inspect,logs,ps,redeploy,run,start,stop,terminate} ...

Container-related operations

optional arguments:
  -h, --help            show this help message and exit

tutum container commands:
  {inspect,logs,ps,redeploy,run,start,stop,terminate}
    inspect             Inspect a container
    logs                Get logs from a container
    ps                  List containers
    redeploy            Redeploy a running container with a new version/tag
    run                 Create and run a new container
    start               Start a container
    stop                Stop a container
    terminate           Terminate a container'''
        self.compare_output(output, args=['tutum', 'container', '-h'])

    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_container_inspect(self, mock_exit):
        output = '''usage: tutum container inspect [-h] identifier [identifier ...]

Inspect a container

positional arguments:
  identifier  container's UUID (either long or short) or name

optional arguments:
  -h, --help  show this help message and exit'''
        self.compare_output(output, args=['tutum', 'container', 'inspect', '-h'])

    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_container_logs(self, mock_exit):
        output = '''usage: tutum container logs [-h] identifier [identifier ...]

Get logs from a container

positional arguments:
  identifier  container's UUID (either long or short) or name

optional arguments:
  -h, --help  show this help message and exit'''
        self.compare_output(output, args=['tutum', 'container', 'logs', '-h'])

    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_container_ps(self, mock_exit):
        output = '''usage: tutum container ps [-h] [-i IDENTIFIER] [-q]
                          [-s {Running,Stopped,Start failed,Stopped with errors}]

List containers

optional arguments:
  -h, --help            show this help message and exit
  -i IDENTIFIER, --identifier IDENTIFIER
                        container's UUID (either long or short) or name
  -q, --quiet           print only long UUIDs
  -s {Running,Stopped,Start failed,Stopped with errors}, --status {Running,Stopped,Start failed,Stopped with errors}
                        filter containers by status'''
        self.compare_output(output, args=['tutum', 'container', 'ps', '-h'])

    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_container_redeploy(self, mock_exit):
        output = '''usage: tutum container redeploy [-h] [-t TAG] identifier [identifier ...]

Redeploy a running container with a new version/tag

positional arguments:
  identifier         container's UUID (either long or short) or name

optional arguments:
  -h, --help         show this help message and exit
  -t TAG, --tag TAG  tag of the image to redeploy'''
        self.compare_output(output, args=['tutum', 'container', 'redeploy', '-h'])

    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_container_run(self, mock_exit):
        output = '''usage: tutum container run [-h] [-n NAME] [--cpushares CPUSHARES]
                           [--memory MEMORY] [--memoryswap MEMORYSWAP]
                           [-t TARGET_NUM_CONTAINERS] [-r RUN_COMMAND]
                           [--entrypoint ENTRYPOINT] [-p PORT] [-e ENV]
                           [--link-cluster LINK_CLUSTER]
                           [--link-container LINK_CONTAINER]
                           [--autorestart {OFF,ON_FAILURE,ALWAYS}]
                           [--autoreplace {OFF,ON_FAILURE,ALWAYS}]
                           [--autodestroy {OFF,ON_FAILURE,ALWAYS}]
                           [--role ROLE] [--sequential]
                           [--web-public-dns WEB_PUBLIC_DNS]
                           image

Create and run a new container

positional arguments:
  image                 the name of the image used to deploy this container

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  a human-readable name for the container(default:
                        image_tag without namespace)
  --cpushares CPUSHARES
                        Relative weight for CPU Shares
  --memory MEMORY       RAM memory hard limit in MB
  --memoryswap MEMORYSWAP
                        Memory swap hard limit in MB
  -t TARGET_NUM_CONTAINERS, --target-num-containers TARGET_NUM_CONTAINERS
                        the number of containers to run for this container
                        (default: 1)
  -r RUN_COMMAND, --run-command RUN_COMMAND
                        the command used to start the container containers
                        (default: as defined in the image)
  --entrypoint ENTRYPOINT
                        the command prefix used to start the container
                        containers (default: as defined in the image)
  -p PORT, --port PORT  set ports i.e. "80/tcp" (default: as defined in the
                        image)
  -e ENV, --env ENV     set environment variables i.e. "ENVVAR=foo" (default:
                        as defined in the image, plus any link- or role-
                        generated variables)
  --link-cluster LINK_CLUSTER
                        Add link to another cluster (name:alias) or
                        (uuid:alias)
  --link-container LINK_CONTAINER
                        Add link to another container (name:alias) or
                        (uuid:alias)
  --autorestart {OFF,ON_FAILURE,ALWAYS}
                        whether the containers should be restarted if they
                        stop (default: OFF)
  --autoreplace {OFF,ON_FAILURE,ALWAYS}
                        whether the containers should be replaced with a new
                        one if they stop (default: OFF)
  --autodestroy {OFF,ON_FAILURE,ALWAYS}
                        whether the containers should be terminated if they
                        stop (default: OFF)
  --role ROLE           Tutum API roles to grant the container, i.e. "global"
                        (default: none, possible values: "global")
  --sequential          whether the containers should be launched and scaled
                        sequentially
  --web-public-dns WEB_PUBLIC_DNS
                        Set your own web public dns'''
        self.compare_output(output, args=['tutum', 'container', 'run', '-h'])

    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_container_start(self, mock_exit):
        output = '''usage: tutum container start [-h] identifier [identifier ...]

Start a container

positional arguments:
  identifier  container's UUID (either long or short) or name

optional arguments:
  -h, --help  show this help message and exit'''
        self.compare_output(output, args=['tutum', 'container', 'start', '-h'])

    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_container_stop(self, mock_exit):
        output = '''usage: tutum container stop [-h] identifier [identifier ...]

Stop a container

positional arguments:
  identifier  container's UUID (either long or short) or name

optional arguments:
  -h, --help  show this help message and exit'''
        self.compare_output(output, args=['tutum', 'container', 'stop', '-h'])

    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_container_terminate(self, mock_exit):
        output = '''usage: tutum container terminate [-h] identifier [identifier ...]

Terminate a container

positional arguments:
  identifier  container's UUID (either long or short) or name

optional arguments:
  -h, --help  show this help message and exit'''
        self.compare_output(output, args=['tutum', 'container', 'terminate', '-h'])

    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_cluster(self, mock_exit):
        output = '''usage: tutum cluster [-h]

                     {alias,inspect,logs,open,ps,redeploy,run,scale,set,start,stop,terminate}
                     ...

Cluster-related operations

optional arguments:
  -h, --help            show this help message and exit

tutum cluster commands:
  {alias,inspect,logs,open,ps,redeploy,run,scale,set,start,stop,terminate}
    alias               Set a custom FQDN (CNAME) to a running web cluster
    inspect             Get all details from an cluster
    logs                Get logs from an cluster
    open                Open last web cluster launched
    ps                  List clusters
    redeploy            Redeploy a running cluster with a new version/tag
    run                 Create and run a new cluster
    scale               Scale a running cluster
    set                 Enable or disable Crash Recovery and Autodestroy
                        features to an existing cluster
    start               Start a stopped cluster
    stop                Stop a running cluster
    terminate           Terminate an cluster'''
        self.compare_output(output, args=['tutum', 'cluster', '-h'])


    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_cluster_alias(self, mock_exit):
        output = '''usage: tutum cluster alias [-h] identifier [identifier ...] dns

Set a custom DNS record (CNAME) to a running web cluster

positional arguments:
  identifier  cluster's UUID (either long or short) or name
  dns         custom FQDN to use for this web cluster

optional arguments:
  -h, --help  show this help message and exit'''
        self.compare_output(output, args=['tutum', 'cluster', 'alias', '-h'])

    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_cluster_inspect(self, mock_exit):
        output = '''usage: tutum cluster inspect [-h] identifier [identifier ...]

Get all details from an cluster

positional arguments:
  identifier  cluster's UUID (either long or short) or name

optional arguments:
  -h, --help  show this help message and exit'''
        self.compare_output(output, args=['tutum', 'cluster', 'inspect', '-h'])

    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_cluster_logs(self, mock_exit):
        output = '''usage: tutum cluster logs [-h] identifier [identifier ...]

Get logs from an cluster

positional arguments:
  identifier  cluster's UUID (either long or short) or name

optional arguments:
  -h, --help  show this help message and exit'''
        self.compare_output(output, args=['tutum', 'cluster', 'logs', '-h'])

    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_cluster_open(self, mock_exit):
        output = '''usage: tutum cluster open [-h]

Open last web cluster launched

optional arguments:
  -h, --help  show this help message and exit'''
        self.compare_output(output, args=['tutum', 'cluster', 'open', '-h'])

    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_cluster_ps(self, mock_exit):
        output = '''usage: tutum cluster ps [-h] [-q]
                        [-s {Running,Partly running,Stopped,Start failed,Stopped with errors}]

List clusters

optional arguments:
  -h, --help            show this help message and exit
  -q, --quiet           print only long UUIDs
  -s {Running,Partly running,Stopped,Start failed,Stopped with errors}, --status {Running,Partly running,Stopped,Start failed,Stopped with errors}
                        filter clusters by status'''
        self.compare_output(output, args=['tutum', 'cluster', 'ps', '-h'])

    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_cluster_redeploy(self, mock_exit):
        output = '''usage: tutum cluster redeploy [-h] [-t TAG] identifier [identifier ...]

Redeploy a running cluster with a new version/tag

positional arguments:
  identifier         cluster's UUID (either long or short) or name

optional arguments:
  -h, --help         show this help message and exit
  -t TAG, --tag TAG  tag of the image to redeploy'''
        self.compare_output(output, args=['tutum', 'cluster', 'redeploy', '-h'])

    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_cluster_run(self, mock_exit):
        output = '''usage: tutum cluster run [-h] [-n NAME] [--cpushares CPUSHARES]
                         [--memory MEMORY] [--memoryswap MEMORYSWAP]
                         [-t TARGET_NUM_CONTAINERS] [-r RUN_COMMAND]
                         [--entrypoint ENTRYPOINT] [-p PORT] [-e ENV]
                         [--link-cluster LINK_CLUSTER]
                         [--link-container LINK_CONTAINER]
                         [--autorestart {OFF,ON_FAILURE,ALWAYS}]
                         [--autoreplace {OFF,ON_FAILURE,ALWAYS}]
                         [--autodestroy {OFF,ON_FAILURE,ALWAYS}] [--role ROLE]
                         [--sequential] [--web-public-dns WEB_PUBLIC_DNS]
                         image

Create and run a new cluster

positional arguments:
  image                 the name of the image used to deploy this cluster

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  a human-readable name for the cluster (default:
                        image_tag without namespace)
  --cpushares CPUSHARES
                        Relative weight for CPU Shares
  --memory MEMORY       RAM memory hard limit in MB
  --memoryswap MEMORYSWAP
                        Memory swap hard limit in MB
  -t TARGET_NUM_CONTAINERS, --target-num-containers TARGET_NUM_CONTAINERS
                        the number of containers to run for this cluster
                        (default: 1)
  -r RUN_COMMAND, --run-command RUN_COMMAND
                        the command used to start the cluster containers
                        (default: as defined in the image)
  --entrypoint ENTRYPOINT
                        the command prefix used to start the cluster
                        containers (default: as defined in the image)
  -p PORT, --port PORT  set ports i.e. "80/tcp" (default: as defined in the
                        image)
  -e ENV, --env ENV     set environment variables i.e. "ENVVAR=foo" (default:
                        as defined in the image, plus any link- or role-
                        generated variables)
  --link-cluster LINK_CLUSTER
                        Add link to another cluster (name:alias) or
                        (uuid:alias)
  --link-container LINK_CONTAINER
                        Add link to another container (name:alias) or
                        (uuid:alias)
  --autorestart {OFF,ON_FAILURE,ALWAYS}
                        whether the containers should be restarted if they
                        stop (default: OFF)
  --autoreplace {OFF,ON_FAILURE,ALWAYS}
                        whether the containers should be replaced with a new
                        one if they stop (default: OFF)
  --autodestroy {OFF,ON_FAILURE,ALWAYS}
                        whether the containers should be terminated if they
                        stop (default: OFF)
  --role ROLE           Tutum API roles to grant the cluster, i.e. "global"
                        (default: none, possible values: "global")
  --sequential          whether the containers should be launched and scaled
                        sequentially
  --web-public-dns WEB_PUBLIC_DNS
                        Set your own web public dns'''
        self.compare_output(output, args=['tutum', 'cluster', 'run', '-h'])

    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_cluster_scale(self, mock_exit):
        output = '''usage: tutum cluster scale [-h]
                           identifier [identifier ...] target-num-containers

Scale a running cluster

positional arguments:
  identifier            cluster's UUID (either long or short) or name
  target-num-containers
                        target number of containers to scale this cluster to

optional arguments:
  -h, --help            show this help message and exit'''
        self.compare_output(output, args=['tutum', 'cluster', 'scale', '-h'])

    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_cluster_set(self, mock_exit):
        output = '''usage: tutum cluster set [-h] [--autorestart {OFF,ON_FAILURE,ALWAYS}]
                         [--autoreplace {OFF,ON_FAILURE,ALWAYS}]
                         [--autodestroy {OFF,ON_FAILURE,ALWAYS}]
                         identifier [identifier ...]

Enable or disable Crash Recovery and Autodestroy features to an existing
cluster

positional arguments:
  identifier            cluster's UUID (either long or short) or name

optional arguments:
  -h, --help            show this help message and exit
  --autorestart {OFF,ON_FAILURE,ALWAYS}
                        whether the containers should be restarted if they
                        stop (default: OFF)
  --autoreplace {OFF,ON_FAILURE,ALWAYS}
                        whether the containers should be replaced with a new
                        one if they stop (default: OFF)
  --autodestroy {OFF,ON_FAILURE,ALWAYS}
                        whether the containers should be terminated if they
                        stop (default: OFF)'''
        self.compare_output(output, args=['tutum', 'cluster', 'set', '-h'])

    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_cluster_start(self, mock_exit):
        output = '''usage: tutum cluster start [-h] identifier [identifier ...]

Start a stopped cluster

positional arguments:
  identifier  cluster's UUID (either long or short) or name

optional arguments:
  -h, --help  show this help message and exit'''
        self.compare_output(output, args=['tutum', 'cluster', 'start', '-h'])

    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_cluster_stop(self, mock_exit):
        output = '''usage: tutum cluster stop [-h] identifier [identifier ...]

Stop a running cluster

positional arguments:
  identifier  cluster's UUID (either long or short) or name

optional arguments:
  -h, --help  show this help message and exit'''
        self.compare_output(output, args=['tutum', 'cluster', 'stop', '-h'])

    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_cluster_terminate(self, mock_exit):
        output = '''usage: tutum cluster terminate [-h] identifier [identifier ...]

Terminate an cluster

positional arguments:
  identifier  cluster's UUID (either long or short) or name

optional arguments:
  -h, --help  show this help message and exit'''
        self.compare_output(output, args=['tutum', 'cluster', 'terminate', '-h'])


    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_image(self, mock_exit):
        output = '''usage: tutum image [-h] {list,register,push,rm,search,update} ...

Image-related operations

optional arguments:
  -h, --help            show this help message and exit

tutum image commands:
  {list,register,push,rm,search,update}
    list                List private images
    register            Register an image from a private repository in Tutum
    push                Push a local image to Tutum private registry
    rm                  Deregister a private image from Tutum
    search              Search for images in the Docker Index
    update              Update a private image'''
        self.compare_output(output, args=['tutum', 'image', '-h'])


    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_image_list(self, mock_exit):
        output = '''usage: tutum image list [-h] [-q] [-j | -l]

List private images

optional arguments:
  -h, --help        show this help message and exit
  -q, --quiet       print only image names
  -j, --jumpstarts  list jumpstart images
  -l, --linux       list linux images'''
        self.compare_output(output, args=['tutum', 'image', 'list', '-h'])

    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_image_register(self, mock_exit):
        output = '''usage: tutum image register [-h] [-d DESCRIPTION] image_name

Register an image from a private repository in Tutum

positional arguments:
  image_name            full image name, i.e. quay.io/tutum/test-repo

optional arguments:
  -h, --help            show this help message and exit
  -d DESCRIPTION, --description DESCRIPTION
                        Image description'''
        self.compare_output(output, args=['tutum', 'image', 'register', '-h'])

    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_image_push(self, mock_exit):
        output = '''usage: tutum image push [-h] [--public] name

Push a local image to Tutum private registry

positional arguments:
  name        name of the image to push

optional arguments:
  -h, --help  show this help message and exit
  --public    push image to public registry'''
        self.compare_output(output, args=['tutum', 'image', 'push', '-h'])

    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_image_rm(self, mock_exit):
        output = '''usage: tutum image rm [-h] image_name [image_name ...]

Deregister a private image from Tutum

positional arguments:
  image_name  full image name, i.e. quay.io/tutum/test-repo

optional arguments:
  -h, --help  show this help message and exit'''
        self.compare_output(output, args=['tutum', 'image', 'rm', '-h'])

    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_image_search(self, mock_exit):
        output = '''usage: tutum image search [-h] query

Search for images in the Docker Index

positional arguments:
  query       query to search

optional arguments:
  -h, --help  show this help message and exit'''
        self.compare_output(output, args=['tutum', 'image', 'search', '-h'])

    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_image_update(self, mock_exit):
        output = '''usage: tutum image update [-h] [-u USERNAME] [-p PASSWORD] [-d DESCRIPTION]
                          image_name [image_name ...]

Update a private image

positional arguments:
  image_name            full image name, i.e. quay.io/tutum/test-repo

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        new username to authenticate with the registry
  -p PASSWORD, --password PASSWORD
                        new password to authenticate with the registry
  -d DESCRIPTION, --description DESCRIPTION
                        new image description'''
        self.compare_output(output, args=['tutum', 'image', 'update', '-h'])


    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_login(self, mock_exit):
        output = '''usage: tutum login [-h]

Login into Tutum

optional arguments:
  -h, --help  show this help message and exit'''
        self.compare_output(output, args=['tutum', 'login', '-h'])


    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_node(self, mock_exit):
        output = '''usage: tutum node [-h] {inspect,list,rm} ...

Node-related operations

optional arguments:
  -h, --help         show this help message and exit

tutum node commands:
  {inspect,list,rm}
    inspect          Inspect a node
    list             List nodes
    rm               Remove a node'''
        self.compare_output(output, args=['tutum', 'node', '-h'])

    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_node_inspect(self, mock_exit):
        output = '''usage: tutum node inspect [-h] identifier [identifier ...]

Inspect a node

positional arguments:
  identifier  node's UUID (either long or short)

optional arguments:
  -h, --help  show this help message and exit'''
        self.compare_output(output, args=['tutum', 'node', 'inspect', '-h'])

    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_node_list(self, mock_exit):
        output = '''usage: tutum node list [-h] [-q]

List nodes

optional arguments:
  -h, --help   show this help message and exit
  -q, --quiet  print only node uuid'''
        self.compare_output(output, args=['tutum', 'node', 'list', '-h'])

    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_node_rm(self, mock_exit):
        output = '''usage: tutum node rm [-h] identifier [identifier ...]

Remove a container

positional arguments:
  identifier  node's UUID (either long or short)

optional arguments:
  -h, --help  show this help message and exit'''
        self.compare_output(output, args=['tutum', 'node', 'rm', '-h'])


    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_nodecluster(self, mock_exit):
        output = '''usage: tutum nodecluster [-h]

                         {create,inspect,list,rm,scale,provider,region,nodetype}
                         ...

NodeCluster-related operations

optional arguments:
  -h, --help            show this help message and exit

tutum node commands:
  {create,inspect,list,rm,scale,provider,region,nodetype}
    create              Create a nodecluster
    inspect             Inspect a nodecluster
    list                List node clusters
    rm                  Remove node clusters
    scale               Scale a running node cluster
    provider            Show all available infrastructure providers
    region              Show all available regions of a given provider
    nodetype            Show all available types of a given region'''
        self.compare_output(output, args=['tutum', 'nodecluster', '-h'])


    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_nodecluster_create(self, mock_exit):
        output = '''usage: tutum nodecluster create [-h] [-t TARGET_NUM_NODES]
                                name provider_id region_id nodetype_id

Create a nodecluster

positional arguments:
  name                  name of the cluster to create
  provider_id           id of the provider
  region_id             id of the region
  nodetype_id           id of the nodetype

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET_NUM_NODES, --target-num-nodes TARGET_NUM_NODES
                        the target number of nodes to run for this cluster
                        (default: 1)'''
        self.compare_output(output, args=['tutum', 'nodecluster', 'create', '-h'])

    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_nodecluster_inspect(self, mock_exit):
        output = '''usage: tutum nodecluster inspect [-h] identifier [identifier ...]

Inspect a nodecluster

positional arguments:
  identifier  node's UUID (either long or short)

optional arguments:
  -h, --help  show this help message and exit'''
        self.compare_output(output, args=['tutum', 'nodecluster', 'inspect', '-h'])

    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_nodecluster_list(self, mock_exit):
        output = '''usage: tutum nodecluster list [-h] [-q]

List node clusters

optional arguments:
  -h, --help   show this help message and exit
  -q, --quiet  print only node uuid'''
        self.compare_output(output, args=['tutum', 'nodecluster', 'list', '-h'])

    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_nodecluster_rm(self, mock_exit):
        output = '''usage: tutum nodecluster rm [-h] identifier [identifier ...]

Remove node clusters

positional arguments:
  identifier  node's UUID (either long or short)

optional arguments:
  -h, --help  show this help message and exit'''
        self.compare_output(output, args=['tutum', 'nodecluster', 'rm', '-h'])

    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_nodecluster_scale(self, mock_exit):
        output = '''usage: tutum nodecluster scale [-h]
                               identifier [identifier ...] target-num-nodes

Scale a running node cluster

positional arguments:
  identifier        node cluster's UUID (either long or short) or name
  target-num-nodes  target number of nodes to scale this node cluster to

optional arguments:
  -h, --help        show this help message and exit'''
        self.compare_output(output, args=['tutum', 'nodecluster', 'scale', '-h'])

    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_nodecluster_provider(self, mock_exit):
        output = '''usage: tutum nodecluster provider [-h] [-q]

Show all available infrastructure providers

optional arguments:
  -h, --help   show this help message and exit
  -q, --quiet  print only provider name'''
        self.compare_output(output, args=['tutum', 'nodecluster', 'provider', '-h'])

    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_nodecluster_region(self, mock_exit):
        output = '''usage: tutum nodecluster region [-h] provider_id

positional arguments:
  provider_id  id of the provider (to find out id, use `tutum nodecluster
               provider`)

optional arguments:
  -h, --help   show this help message and exit'''
        self.compare_output(output, args=['tutum', 'nodecluster', 'region', '-h'])

    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_nodecluster_nodetype(self, mock_exit):
        output = '''usage: tutum nodecluster nodetype [-h] region_id

positional arguments:
  region_id   id of the region (to find out id use `tutum nodecluster region`)

optional arguments:
  -h, --help  show this help message and exit'''
        self.compare_output(output, args=['tutum', 'nodecluster', 'nodetype', '-h'])