import unittest
import mock
import __builtin__
import uuid
import StringIO

from tutumcli.commands import *
from  tutum.api.exceptions import *


class LoginTestCase(unittest.TestCase):
    def setUp(self):
        self.raw_input_holder = __builtin__.raw_input
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        sys.stdout = self.stdout_buf = StringIO.StringIO()
        sys.stderr = self.stderr_buf = StringIO.StringIO()

    def tearDown(self):
        __builtin__.raw_input = self.raw_input_holder
        sys.stdout = self.stdout
        sys.stdout = self.stderr

    def set_username(self, username):
        __builtin__.raw_input = lambda _: username

    @mock.patch('tutumcli.commands.getpass.getpass', return_value='test_password')
    @mock.patch('tutumcli.commands.tutum.auth.get_auth')
    def test_login_success(self, mock_get_auth, mock_password):
        user = uuid.uuid4()
        apikey = uuid.uuid4()
        __builtin__.raw_input = lambda _: user  # set username
        mock_get_auth.return_value = (user, apikey)
        login()
        out = self.stdout_buf.getvalue().strip()
        self.stdout_buf.truncate(0)
        self.assertEqual('Login succeeded!', out)
        configFile = os.path.join(os.path.expanduser('~'), TUTUM_FILE)
        output = '''[auth]
user = %s
apikey = %s''' % (user, apikey)
        file = open(configFile, 'r')
        try:
            data = file.read()
            self.assertEqual(output.strip(), data.strip())
        finally:
            file.close()
            os.remove(configFile)

    @mock.patch('tutumcli.commands.utils.try_register', return_value=(True, 'Registration succeeded!'))
    @mock.patch('tutumcli.commands.getpass.getpass', return_value='test_password')
    @mock.patch('tutumcli.commands.tutum.auth.get_auth', side_effect=TutumAuthError)
    def test_login_register_success(self, mock_get_auth, mock_getpass, mock_register):
        __builtin__.raw_input = lambda _: 'test_username'  # set username
        login()
        mock_register.assert_called_with('test_username', 'test_password')
        out = self.stdout_buf.getvalue().strip()
        self.stdout_buf.truncate(0)
        self.assertEqual('Registration succeeded!', out)

    @mock.patch('tutumcli.commands.utils.try_register',
                return_value=(False, 'ERROR: username: A user with that username already exists.'))
    @mock.patch('tutumcli.commands.sys.exit')
    @mock.patch('tutumcli.commands.getpass.getpass', return_value='test_password')
    @mock.patch('tutumcli.commands.tutum.auth.get_auth', side_effect=TutumAuthError)
    def test_login_register_user_exist(self, mock_get_auth, mock_getpass, mock_exit, mock_register):
        __builtin__.raw_input = lambda _: 'test_username'  # set username
        login()
        mock_register.assert_called_with('test_username', 'test_password')
        out = self.stderr_buf.getvalue().strip()
        self.stderr_buf.truncate(0)
        self.assertEqual('Wrong username and/or password. Please try to login again', out)
        mock_exit.assert_called_with(TUTUM_AUTH_ERROR_EXIT_CODE)

    @mock.patch('tutumcli.commands.utils.try_register',
                return_value=(False, 'password1: This field is required.\npassword2: This field is required.'
                                     '\nemail: This field is required.'))
    @mock.patch('tutumcli.commands.sys.exit')
    @mock.patch('tutumcli.commands.getpass.getpass', return_value='test_password')
    @mock.patch('tutumcli.commands.tutum.auth.get_auth', side_effect=TutumAuthError)
    def test_login_register_password_required(self, mock_get_auth, mock_getpass, mock_exit, mock_register):
        __builtin__.raw_input = lambda _: 'test_username'  # set username
        login()
        mock_register.assert_called_with('test_username', 'test_password')
        out = self.stderr_buf.getvalue().strip()
        self.stderr_buf.truncate(0)
        self.assertEqual('password: This field is required.\nemail: This field is required.', out)
        mock_exit.assert_called_with(TUTUM_AUTH_ERROR_EXIT_CODE)

    @mock.patch('tutumcli.commands.sys.exit')
    @mock.patch('tutumcli.commands.getpass.getpass', return_value='test_password')
    @mock.patch('tutumcli.commands.tutum.auth.get_auth', side_effect=Exception('Cannot open config file'))
    def test_login_register_Exception(self, mock_get_auth, mock_getpass, mock_exit):
        __builtin__.raw_input = lambda _: 'test_username'  # set username
        login()
        out = self.stderr_buf.getvalue().strip()
        self.stderr_buf.truncate(0)
        self.assertEqual('Cannot open config file', out)
        mock_exit.assert_called_with(EXCEPTION_EXIT_CODE)