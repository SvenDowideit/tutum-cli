import unittest
import copy
import mock

from tutumcli.tutum_cli import patch_help_option, dispatch_cmds
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
                                 target_num_containers=args.target_num_containers, run_command=args.run_command,
                                 entrypoint=args.entrypoint, container_ports=args.port, container_envvars=args.env,
                                 linked_to_cluster=args.link_cluster, linked_to_container=args.link_container,
                                 autorestart=args.autorestart,
                                 autoreplace=args.autoreplace, autodestroy=args.autodestroy, roles=args.role,
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
                                   run_command=args.run_command, entrypoint=args.entrypoint, container_ports=args.port,
                                   container_envvars=args.env,
                                   linked_to_cluster=args.link_cluster, linked_to_container=args.link_container,
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

        args = self.parser.parse_args(['nodecluster','rm', 'id'])
        dispatch_cmds(args)
        mock_cmds.nodecluster_rm(args.identifier)

        args = self.parser.parse_args(['nodecluster', 'scale', 'id', '3'])
        print args
        dispatch_cmds(args)
        mock_cmds.nodecluster_scale(args.identifier, args.target_num_nodes)
if __name__ == '__main__':
    unittest.main()

