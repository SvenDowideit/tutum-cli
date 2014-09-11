import unittest

from tutumcli.tutum_cli import patch_help_option
from tutumcli.exceptions import InternalError

class PatchHelpOptionTestCase(unittest.TestCase):
    def test_parser_with_empty_args(self):
        args = []
        self.assertRaises(InternalError, patch_help_option, args)


if __name__ == '__main__':
    unittest.main()