# -*- coding: utf-8 -*-
import unittest
import mock
import __builtin__
import StringIO
import uuid

from tutumcli.commands import *
from tutum.api.exceptions import *

import tutumcli


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


class BuildTestCase(unittest.TestCase):
    def setUp(self):
        self.stdout = sys.stdout
        sys.stdout = self.buf = StringIO.StringIO()

    def tearDown(self):
        sys.stdout = self.stdout

    @mock.patch('tutumcli.commands.utils.get_docker_client', return_value=docker.Client())
    @mock.patch.object(tutumcli.commands.docker.Client, 'build')
    def test_build_with_dockerfile(self, mock_build, mock_get_docker_client):
        os.system('touch /tmp/Dockerfile')
        tag = 'mysql'
        working_directory = '/tmp'
        quiet = True
        no_cache = False
        build(tag, working_directory, quiet, no_cache)
        mock_build.assert_called('mysql', join(abspath('/tmp'), "Dockerfile"), True, False)
        self.assertEqual(tag, self.buf.getvalue().strip())
        self.buf.truncate(0)
        try:
            os.remove('/tmp/Dockerfile')
        except:
            pass

    @mock.patch('tutumcli.commands.utils.get_docker_client', return_value=docker.Client())
    @mock.patch.object(tutumcli.commands.docker.Client, 'build')
    def test_build_with_procfile(self, mock_build, mock_get_docker_client):
        try:
            os.remove('/tmp/Dockerfile')
        except:
            pass

        os.system(" echo 'web:     python ranking/manage.py runserver' > /tmp/Procfile")
        tag = 'mysql'
        working_directory = '/tmp'
        quiet = True
        no_cache = False
        build(tag, working_directory, quiet, no_cache)
        mock_build.assert_called('mysql', join(abspath('/tmp'), "Dockerfile"), True, False)
        self.assertEqual(tag, self.buf.getvalue().strip())
        self.buf.truncate(0)
        output = '''FROM tutum/buildstep

EXPOSE 80

CMD ["/start","web"]'''
        file = open('/tmp/Dockerfile', 'r')
        try:
            data = file.read()
            self.assertEqual(output.strip(), data.strip())
        finally:
            file.close()
            os.remove('/tmp/Dockerfile')
            os.remove('/tmp/Procfile')


class ServiceAliasTestCase(unittest.TestCase):
    def setUp(self):
        self.stdout = sys.stdout
        sys.stdout = self.buf = StringIO.StringIO()

    def tearDown(self):
        sys.stdout = self.stdout

    @mock.patch('tutumcli.commands.tutum.Service.save')
    @mock.patch('tutumcli.commands.utils.fetch_remote_service')
    def test_service_alias_with_dns(self, mock_fetch_remote_service, mock_save):
        uuid = '7A4CFE51-03BB-42D6-825E-3B533888D8CD'
        new_dns = 'new_dns'
        service = tutumcli.commands.tutum.Service()
        service.uuid = uuid
        service.web_public_dns = 'placeholder'
        mock_fetch_remote_service.return_value = service
        mock_save.return_value = True
        service_alias(['test_id'], new_dns)

        self.assertEqual(uuid, self.buf.getvalue().strip())
        self.assertEqual(new_dns, service.web_public_dns)
        self.buf.truncate(0)

    @mock.patch('tutumcli.commands.tutum.Service.save')
    @mock.patch('tutumcli.commands.utils.fetch_remote_service')
    def test_service_alias_empty_dns(self, mock_fetch_remote_service, mock_save):
        service = tutumcli.commands.tutum.Service()
        service.uuid = '7A4CFE51-03BB-42D6-825E-3B533888D8CD'
        service.web_public_dns = 'placeholder'
        mock_fetch_remote_service.return_value = service
        mock_save.return_value = True
        service_alias(['test_id'], None)

        self.assertEqual('', self.buf.getvalue().strip())
        self.assertEqual('placeholder', service.web_public_dns)
        self.buf.truncate(0)

    @mock.patch('tutumcli.commands.tutum.Service.save')
    @mock.patch('tutumcli.commands.utils.fetch_remote_service')
    def test_service_alias_multi_identifier(self, mock_fetch_remote_service, mock_save):
        uuid = '7A4CFE51-03BB-42D6-825E-3B533888D8CD'
        new_dns = 'new_dns'
        service = tutumcli.commands.tutum.Service()
        service.uuid = uuid
        service.web_public_dns = 'placeholder'
        mock_fetch_remote_service.return_value = service
        mock_save.return_value = True
        service_alias(['test_id', 'test_id2'], new_dns)

        self.assertEqual('\n'.join([uuid, uuid]), self.buf.getvalue().strip())
        self.assertEqual(new_dns, service.web_public_dns)
        self.buf.truncate(0)

    @mock.patch('tutumcli.commands.tutum.Service.save')
    @mock.patch('tutumcli.commands.utils.fetch_remote_service')
    def test_service_alias_multi_identifier_empty_dns(self, mock_fetch_remote_service, mock_save):
        uuid = '7A4CFE51-03BB-42D6-825E-3B533888D8CD'
        service = tutumcli.commands.tutum.Service()
        service.uuid = uuid
        service.web_public_dns = 'placeholder'
        mock_fetch_remote_service.return_value = service
        mock_save.return_value = True
        service_alias(['test_id', 'test_id2'], None)

        self.assertEqual('', self.buf.getvalue().strip())
        self.assertEqual('placeholder', service.web_public_dns)
        self.buf.truncate(0)

    @mock.patch('tutumcli.commands.sys.exit')
    @mock.patch('tutumcli.commands.utils.fetch_remote_service', side_effect=TutumApiError)
    def test_service_alias_with_exception(self, mock_fetch_remote_service, mock_exit):
        service = tutumcli.commands.tutum.Service()
        mock_fetch_remote_service.return_value = service
        service_alias(['test_id', 'test_id2'], None)

        mock_exit.assert_called_with(EXCEPTION_EXIT_CODE)


class ServiceInspectTestCase(unittest.TestCase):
    def setUp(self):
        self.stdout = sys.stdout
        sys.stdout = self.buf = StringIO.StringIO()

    def tearDown(self):
        sys.stdout = self.stdout

    @mock.patch('tutumcli.commands.tutum.Service.get_all_attributes')
    @mock.patch('tutumcli.commands.tutum.Service.fetch')
    @mock.patch('tutumcli.commands.utils.fetch_remote_service')
    def test_service_inspect(self, mock_fetch_remote_service, mock_fetch, mock_get_all_attributes):
        output = '''{
  "key": [
    {
      "name": "test",
      "id": "1"
    }
  ]
}'''
        uuid = '7A4CFE51-03BB-42D6-825E-3B533888D8CD'
        service = tutumcli.commands.tutum.Service()
        service.uuid = uuid
        mock_fetch.return_value = service
        mock_fetch_remote_service.return_value = service
        mock_get_all_attributes.return_value = {'key': [{'name': 'test', 'id': '1'}]}
        service_inspect(['test_id'])

        mock_fetch.assert_called_with(uuid)
        self.assertEqual(' '.join(output.split()), ' '.join(self.buf.getvalue().strip().split()))
        self.buf.truncate(0)

    @mock.patch('tutumcli.commands.sys.exit')
    @mock.patch('tutumcli.commands.utils.fetch_remote_service', side_effect=TutumApiError)
    def test_service_inspect_with_exception(self, mock_fetch_remote_service, mock_exit):
        service = tutumcli.commands.tutum.Service()
        mock_fetch_remote_service.return_value = service
        service_inspect(['test_id', 'test_id2'])

        mock_exit.assert_called_with(EXCEPTION_EXIT_CODE)


class ServiceLogsTestCase(unittest.TestCase):
    def setUp(self):
        self.stdout = sys.stdout
        sys.stdout = self.buf = StringIO.StringIO()

    def tearDown(self):
        sys.stdout = self.stdout

    @mock.patch('tutumcli.commands.utils.fetch_remote_service')
    def test_service_logs(self, mock_fetch_remote_service):
        log = 'Here is the log'
        service = tutumcli.commands.tutum.Service
        service.logs = log
        mock_fetch_remote_service.return_value = service
        service_logs(['test_id'])

        self.assertEqual(log, self.buf.getvalue().strip())
        self.buf.truncate(0)

    @mock.patch('tutumcli.commands.sys.exit')
    @mock.patch('tutumcli.commands.utils.fetch_remote_service', side_effect=TutumApiError)
    def test_service_logs_with_exception(self, mock_fetch_remote_service, mock_exit):
        service = tutumcli.commands.tutum.Service()
        mock_fetch_remote_service.return_value = service
        service_logs(['test_id', 'test_id2'])

        mock_exit.assert_called_with(EXCEPTION_EXIT_CODE)


class ServiceOpenTestCase(unittest.TestCase):
    def setUp(self):
        self.stderr = sys.stderr
        sys.stderr = self.buf = StringIO.StringIO()

    def tearDown(self):
        sys.stderr = self.stderr

    @mock.patch('tutumcli.commands.webbrowser.open')
    @mock.patch('tutumcli.commands.tutum.Service.list')
    def test_service_open(self, mock_list, mock_open):
        service1 = tutumcli.commands.tutum.Service()
        service1.state = 'Running'
        service1.deployed_datetime = 'Sun, 6 Apr 2014 18:11:17 +0000'
        service1.web_public_dns = 'server1.co'
        service2 = tutumcli.commands.tutum.Service()
        service2.state = 'Partly running'
        service2.deployed_datetime = 'Mon, 7 Apr 2014 18:11:17 +0000'
        service2.web_public_dns = 'service2.co'
        service3 = tutumcli.commands.tutum.Service()
        service3.state = 'Stopped'
        service3.deployed_datetime = 'Tue, 8 Apr 2014 18:11:17 +0000'
        service3.web_public_dns = 'service3.co'
        mock_list.return_value = [service1, service2, service3]
        service_open()

        mock_open.assert_called_with('http://service2.co')

    @mock.patch('tutumcli.commands.tutum.Service.list')
    def test_service_open_no_running_service(self, mock_list):
        service1 = tutumcli.commands.tutum.Service()
        service1.state = 'Stopped'
        service1.deployed_datetime = 'Sun, 6 Apr 2014 18:11:17 +0000'
        service1.web_public_dns = 'server1.co'
        service2 = tutumcli.commands.tutum.Service()
        service2.state = 'Terminated'
        service2.deployed_datetime = 'Mon, 7 Apr 2014 18:11:17 +0000'
        service2.web_public_dns = 'service2.co'
        mock_list.return_value = [service1, service2]
        service_open()

        self.assertEqual('Error: There are not web applications Running or Partly Running', self.buf.getvalue().strip())
        self.buf.truncate(0)

    @mock.patch('tutumcli.commands.sys.exit')
    @mock.patch('tutumcli.commands.tutum.Service.list', side_effect=TutumApiError)
    def test_service_open_with_exception(self, mock_list, mock_exit):
        service_open()

        mock_exit.assert_called_with(EXCEPTION_EXIT_CODE)


class ServicePsTestCase(unittest.TestCase):
    def setUp(self):
        self.stdout = sys.stdout
        sys.stdout = self.buf = StringIO.StringIO()

        service1 = tutumcli.commands.tutum.Service()
        service1.unique_name = 'SERVICE1'
        service1.uuid = '7A4CFE51-03BB-42D6-825E-3B533888D8CD'
        service1.image_name = 'test/service1'
        service1.web_public_dns = 'service1.io'
        service1.state = 'Running'
        service1.deployed_datetime = ''
        service2 = tutumcli.commands.tutum.Service()
        service2.unique_name = 'SERVICE2'
        service2.uuid = '8B4CFE51-03BB-42D6-825E-3B533888D8CD'
        service2.image_name = 'test/service2'
        service2.web_public_dns = 'service2.io'
        service2.state = 'Stopped'
        service2.deployed_datetime = ''
        self.servicelist = [service1, service2]

    def tearDown(self):
        sys.stdout = self.stdout

    @mock.patch('tutumcli.commands.tutum.Service.list')
    def test_service_ps(self, mock_list):
        output = u'''NAME      UUID      STATUS     IMAGE          DEPLOYED    WEB HOSTNAME
SERVICE1  7A4CFE51  ▶ Running  test/service1              service1.io
SERVICE2  8B4CFE51  ◼ Stopped  test/service2              service2.io'''
        mock_list.return_value = self.servicelist
        service_ps(status='Running')

        mock_list.assert_called_with(state='Running')
        self.assertEqual(output, self.buf.getvalue().strip())
        self.buf.truncate(0)

    @mock.patch('tutumcli.commands.tutum.Service.list')
    def test_service_ps_quiet(self, mock_list):
        output = '''7A4CFE51-03BB-42D6-825E-3B533888D8CD
8B4CFE51-03BB-42D6-825E-3B533888D8CD'''
        mock_list.return_value = self.servicelist
        service_ps(quiet=True)

        self.assertEqual(output, self.buf.getvalue().strip())

    @mock.patch('tutumcli.commands.sys.exit')
    @mock.patch('tutumcli.commands.tutum.Service.list', side_effect=TutumApiError)
    def test_service_ps_with_exception(self, mock_list, mock_exit):
        service_ps()

        mock_exit.assert_called_with(EXCEPTION_EXIT_CODE)


class ServiceRunTestCase(unittest.TestCase):
    def setUp(self):
        self.stdout = sys.stdout
        sys.stdout = self.buf = StringIO.StringIO()

    def tearDown(self):
        sys.stdout = self.stdout

    @mock.patch('tutumcli.commands.tutum.Service.start')
    @mock.patch('tutumcli.commands.tutum.Service.save')
    @mock.patch('tutumcli.commands.tutum.Service.create')
    def test_service_run(self, mock_create, mock_save, mock_start):
        container_ports = ['80:80/tcp', '22:22']
        container_envvars = ['MYSQL_ADMIN=admin', 'MYSQL_PASS=password']
        linked_to_service = ['mysql:mysql', 'redis:redis']
        linked_to_container = ['mariadb:mariadb', 'wordpress:wordpress']

        service = tutumcli.commands.tutum.Service()
        service.uuid = '7A4CFE51-03BB-42D6-825E-3B533888D8CD'
        mock_create.return_value = service
        mock_start.return_value = True
        service_run('imagename', 'containername', 1, '256M', '1024M', 3, '-d', '/bin/mysql',
                    container_ports, container_envvars, linked_to_service, linked_to_container,
                    'OFF', 'OFF', 'OFF', 'poweruser', True, 'tutum.co')

        mock_create.assert_called_with(image='imagename', name='containername', cpu_shares=1,
                                       memory='256M', memory_swap='1024M',
                                       target_num_containers=3, run_command='-d',
                                       entrypoint='/bin/mysql', container_ports=utils.parse_ports(container_ports),
                                       container_envvars=utils.parse_envvars(container_envvars),
                                       linked_to_service=utils.parse_links(linked_to_service, 'to_service'),
                                       linked_to_container=utils.parse_links(linked_to_container, 'to_container'),
                                       autorestart='OFF', autoreplace='OFF', autodestroy='OFF',
                                       roles='poweruser', sequential_deployment=True, web_public_dns='tutum.co')
        mock_save.asser_called()
        self.assertEqual(service.uuid, self.buf.getvalue().strip())
        self.buf.truncate(0)

    @mock.patch('tutumcli.commands.sys.exit')
    @mock.patch('tutumcli.commands.tutum.Service.create', side_effect=TutumApiError)
    def test_service_run_with_exception(self, mock_create, mock_exit):
        container_ports = ['80:80/tcp', '22:22']
        container_envvars = ['MYSQL_ADMIN=admin', 'MYSQL_PASS=password']
        linked_to_service = ['mysql:mysql', 'redis:redis']
        linked_to_container = ['mariadb:mariadb', 'wordpress:wordpress']
        service_run('imagename', 'containername', 1, '256M', '1024M', 3, '-d', '/bin/mysql',
                    container_ports, container_envvars, linked_to_service, linked_to_container,
                    'OFF', 'OFF', 'OFF', 'poweruser', True, 'tutum.co')

        mock_exit.assert_called_with(EXCEPTION_EXIT_CODE)


class ServiceScaleTestCase(unittest.TestCase):
    def setUp(self):
        self.stdout = sys.stdout
        sys.stdout = self.buf = StringIO.StringIO()

    def tearDown(self):
        sys.stdout = self.stdout

    @mock.patch('tutumcli.commands.tutum.Service.save')
    @mock.patch('tutumcli.commands.utils.fetch_remote_service')
    def test_service_scale(self, mock_fetch_remote_service, mock_save):
        service = tutumcli.commands.tutum.Service()
        service.uuid = '7A4CFE51-03BB-42D6-825E-3B533888D8CD'
        mock_fetch_remote_service.return_value = service
        service_scale(['7A4CFE51-03BB-42D6-825E-3B533888D8CD'], 3)

        mock_save.assert_called()
        self.assertEqual(3, service.target_num_containers)
        self.assertEqual(service.uuid, self.buf.getvalue().strip())
        self.buf.truncate(0)

    @mock.patch('tutumcli.commands.sys.exit')
    @mock.patch('tutumcli.commands.utils.fetch_remote_service', side_effect=TutumApiError)
    def test_service_scale_with_exception(self, mock_fetch_remote_service, mock_exit):
        service_scale(['test_id'], 3)

        mock_exit.assert_called_with(EXCEPTION_EXIT_CODE)


class ServiceSetTestCase(unittest.TestCase):
    def setUp(self):
        self.stdout = sys.stdout
        sys.stdout = self.buf = StringIO.StringIO()

    def tearDown(self):
        sys.stdout = self.stdout

    @mock.patch('tutumcli.commands.tutum.Service.save')
    @mock.patch('tutumcli.commands.utils.fetch_remote_service')
    def test_service_set(self, mock_fetch_remote_service, mock_save):
        service = tutumcli.commands.tutum.Service()
        service.uuid = '7A4CFE51-03BB-42D6-825E-3B533888D8CD'
        mock_fetch_remote_service.return_value = service
        service_set('ALWAYS', 'ON_FAILURE', 'ALWAYS', ['7A4CFE51-03BB-42D6-825E-3B533888D8CD'])

        mock_save.assert_called()
        self.assertEqual('ALWAYS', service.autorestart)
        self.assertEqual('ON_FAILURE', service.autoreplace)
        self.assertEqual('ALWAYS', service.autodestroy)
        self.assertEqual(service.uuid, self.buf.getvalue().strip())
        self.buf.truncate(0)

    @mock.patch('tutumcli.commands.sys.exit')
    @mock.patch('tutumcli.commands.utils.fetch_remote_service', side_effect=TutumApiError)
    def test_service_set_with_exception(self, mock_fetch_remote_service, mock_exit):
        service_set('OFF', 'OFF', 'OFF', ['test_id'])

        mock_exit.assert_called_with(EXCEPTION_EXIT_CODE)


class ServiceStartTestCase(unittest.TestCase):
    def setUp(self):
        self.stdout = sys.stdout
        sys.stdout = self.buf = StringIO.StringIO()

    def tearDown(self):
        sys.stdout = self.stdout

    @mock.patch('tutumcli.commands.tutum.Service.start')
    @mock.patch('tutumcli.commands.utils.fetch_remote_service')
    def test_service_start(self, mock_fetch_remote_service, mock_start):
        service = tutumcli.commands.tutum.Service()
        service.uuid = '7A4CFE51-03BB-42D6-825E-3B533888D8CD'
        mock_fetch_remote_service.return_value = service
        mock_start.return_value = True
        service_start(['7A4CFE51-03BB-42D6-825E-3B533888D8CD'])

        self.assertEqual(service.uuid, self.buf.getvalue().strip())
        self.buf.truncate(0)

    @mock.patch('tutumcli.commands.sys.exit')
    @mock.patch('tutumcli.commands.utils.fetch_remote_service', side_effect=TutumApiError)
    def test_service_start_with_exception(self, mock_fetch_remote_service, mock_exit):
        service_start(['7A4CFE51-03BB-42D6-825E-3B533888D8CD'])

        mock_exit.assert_called_with(EXCEPTION_EXIT_CODE)


class ServiceStopTestCase(unittest.TestCase):
    def setUp(self):
        self.stdout = sys.stdout
        sys.stdout = self.buf = StringIO.StringIO()

    def tearDown(self):
        sys.stdout = self.stdout

    @mock.patch('tutumcli.commands.tutum.Service.stop')
    @mock.patch('tutumcli.commands.utils.fetch_remote_service')
    def test_service_stop(self, mock_fetch_remote_service, mock_stop):
        service = tutumcli.commands.tutum.Service()
        service.uuid = '7A4CFE51-03BB-42D6-825E-3B533888D8CD'
        mock_fetch_remote_service.return_value = service
        mock_stop.return_value = True
        service_stop(['7A4CFE51-03BB-42D6-825E-3B533888D8CD'])

        self.assertEqual(service.uuid, self.buf.getvalue().strip())
        self.buf.truncate(0)

    @mock.patch('tutumcli.commands.sys.exit')
    @mock.patch('tutumcli.commands.utils.fetch_remote_service', side_effect=TutumApiError)
    def test_service_stop_with_exception(self, mock_fetch_remote_service, mock_exit):
        service_start(['7A4CFE51-03BB-42D6-825E-3B533888D8CD'])

        mock_exit.assert_called_with(EXCEPTION_EXIT_CODE)


class ServiceTerminateTestCase(unittest.TestCase):
    def setUp(self):
        self.stdout = sys.stdout
        sys.stdout = self.buf = StringIO.StringIO()

    def tearDown(self):
        sys.stdout = self.stdout

    @mock.patch('tutumcli.commands.tutum.Service.delete')
    @mock.patch('tutumcli.commands.utils.fetch_remote_service')
    def test_service_teminate(self, mock_fetch_remote_service, mock_delete):
        service = tutumcli.commands.tutum.Service()
        service.uuid = '7A4CFE51-03BB-42D6-825E-3B533888D8CD'
        mock_fetch_remote_service.return_value = service
        mock_delete.return_value = True
        service_terminate(['7A4CFE51-03BB-42D6-825E-3B533888D8CD'])

        self.assertEqual(service.uuid, self.buf.getvalue().strip())
        self.buf.truncate(0)

    @mock.patch('tutumcli.commands.sys.exit')
    @mock.patch('tutumcli.commands.utils.fetch_remote_service', side_effect=TutumApiError)
    def test_service_terminate_with_exception(self, mock_fetch_remote_service, mock_exit):
        service_terminate(['7A4CFE51-03BB-42D6-825E-3B533888D8CD'])

        mock_exit.assert_called_with(EXCEPTION_EXIT_CODE)