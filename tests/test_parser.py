import unittest
import copy
from tutumcli.tutum_cli import patch_help_option
from tutumcli.exceptions import InternalError


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


if __name__ == '__main__':
    unittest.main()

