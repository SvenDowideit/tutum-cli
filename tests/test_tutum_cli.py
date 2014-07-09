from unittest import TestCase

from tutumcli.tutum_cli import parser


class CommandLineTestCase(TestCase):
    """
    Base TestCase class, sets up a CLI parser
    """
    @classmethod
    def setUpClass(cls):
        cls.parser = parser


class TutumCliTestCase(CommandLineTestCase):
    def test_with_empty_args(self):
        """
        User passes no args, should fail with SystemExit
        """
        with self.assertRaises(SystemExit):
            self.parser.parse_args([])