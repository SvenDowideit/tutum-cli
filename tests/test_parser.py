import unittest
import copy
import mock
import StringIO
import sys

from tutumcli.tutum_cli import patch_help_option, dispatch_cmds, initialize_parser
from tutumcli.exceptions import InternalError
import tutumcli

from help_output_text import *


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


    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.add_argument')
    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_version(self, mock_exit, mock_add_arg):
        initialize_parser()
        mock_add_arg.assert_any_call('-v', '--version', action='version', version='%(prog)s ' + tutumcli.__version__)

    @mock.patch('tutumcli.tutum_cli.argparse.ArgumentParser.exit')
    def test_tutum_help_output(self, mock_exit):
        self.compare_output(TUTUM, args=['tutum', '-h'])
        self.compare_output(TUTUM_BUILD, args=['tutum', 'build', '-h'])
        self.compare_output(TUTUM_CONTAINER, args=['tutum', 'container', '-h'])
        self.compare_output(TUTUM_CONTAINER_INSPECT, args=['tutum', 'container', 'inspect', '-h'])
        self.compare_output(TUTUM_CONTAINER_LOGS, args=['tutum', 'container', 'logs', '-h'])
        self.compare_output(TUTUM_CONTAINER_PS, args=['tutum', 'container', 'ps', '-h'])
        self.compare_output(TUTUM_CONTAINER_REDEPLOY, args=['tutum', 'container', 'redeploy', '-h'])
        self.compare_output(TUTUM_CONTAINER_RUN, args=['tutum', 'container', 'run', '-h'])
        self.compare_output(TUTUM_CONTAINER_START, args=['tutum', 'container', 'start', '-h'])
        self.compare_output(TUTUM_CONTAINER_STOP, args=['tutum', 'container', 'stop', '-h'])
        self.compare_output(TUTUM_CONTAINER_TERMINATE, args=['tutum', 'container', 'terminate', '-h'])
        self.compare_output(TUTUM_CLUSTER, args=['tutum', 'cluster', '-h'])
        self.compare_output(TUTUM_CLUSTER_ALIAS, args=['tutum', 'cluster', 'alias', '-h'])
        self.compare_output(TUTUM_CLUSTER_INSPECT, args=['tutum', 'cluster', 'inspect', '-h'])
        self.compare_output(TUTUM_CLUSTER_LOGS, args=['tutum', 'cluster', 'logs', '-h'])
        self.compare_output(TUTUM_CLUSTER_OPEN, args=['tutum', 'cluster', 'open', '-h'])
        self.compare_output(TUTUM_CLUSTER_PS, args=['tutum', 'cluster', 'ps', '-h'])
        self.compare_output(TUTUM_CLUSTER_REDEPLOY, args=['tutum', 'cluster', 'redeploy', '-h'])
        self.compare_output(TUTUM_CLUSTER_RUN, args=['tutum', 'cluster', 'run', '-h'])
        self.compare_output(TUTUM_CLUSTER_SCALE, args=['tutum', 'cluster', 'scale', '-h'])
        self.compare_output(TUTUM_CLUSTER_SET, args=['tutum', 'cluster', 'set', '-h'])
        self.compare_output(TUTUM_CLUSTER_START, args=['tutum', 'cluster', 'start', '-h'])
        self.compare_output(TUTUM_CLUSTER_STOP, args=['tutum', 'cluster', 'stop', '-h'])
        self.compare_output(TUTUM_CLUSTER_TERMINATE, args=['tutum', 'cluster', 'terminate', '-h'])
        self.compare_output(TUTUM_IMAGE, args=['tutum', 'image', '-h'])
        self.compare_output(TUTUM_IMAGE_LIST, args=['tutum', 'image', 'list', '-h'])
        self.compare_output(TUTUM_IMAGE_REGISTER, args=['tutum', 'image', 'register', '-h'])
        self.compare_output(TUTUM_IMAGE_PUSH, args=['tutum', 'image', 'push', '-h'])
        self.compare_output(TUTUM_IMAGE_RM, args=['tutum', 'image', 'rm', '-h'])
        self.compare_output(TUTUM_IMAGE_SEARCH, args=['tutum', 'image', 'search', '-h'])
        self.compare_output(TUTUM_IMAGE_UPDATE, args=['tutum', 'image', 'update', '-h'])
        self.compare_output(TUTUM_LOGIN, args=['tutum', 'login', '-h'])
        self.compare_output(TUTUM_NODE, args=['tutum', 'node', '-h'])
        self.compare_output(TUTUM_NODE_INSPECT, args=['tutum', 'node', 'inspect', '-h'])
        self.compare_output(TUTUM_NODE_LIST, args=['tutum', 'node', 'list', '-h'])
        self.compare_output(TUTUM_NODE_RM, args=['tutum', 'node', 'rm', '-h'])
        self.compare_output(TUTUM_NODECLUSTER, args=['tutum', 'nodecluster', '-h'])
        self.compare_output(TUTUM_NODECLUSTER_CREATE, args=['tutum', 'nodecluster', 'create', '-h'])
        self.compare_output(TUTUM_NODECLUSTER_INSPECT, args=['tutum', 'nodecluster', 'inspect', '-h'])
        self.compare_output(TUTUM_NODECLUSTER_LIST, args=['tutum', 'nodecluster', 'list', '-h'])
        self.compare_output(TUTUM_NODECLUSTER_RM, args=['tutum', 'nodecluster', 'rm', '-h'])
        self.compare_output(TUTUM_NODECLUSTER_SCALE, args=['tutum', 'nodecluster', 'scale', '-h'])
        self.compare_output(TUTUM_NODECLUSTER_PROVIDER, args=['tutum', 'nodecluster', 'provider', '-h'])
        self.compare_output(TUTUM_NODECLUSTER_REGION, args=['tutum', 'nodecluster', 'region', '-h'])
        self.compare_output(TUTUM_NODECLUSTER_NODETYPE, args=['tutum', 'nodecluster', 'nodetype', '-h'])