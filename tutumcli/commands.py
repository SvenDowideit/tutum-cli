from __future__ import print_function
import getpass
import ConfigParser
import json
import sys
import urlparse
import webbrowser
import re
import os
from os.path import join, expanduser, abspath, isfile
import requests
import yaml
from exceptions import StreamOutputError
import tutum
from tutum.api import auth
from tutum.api import exceptions
from packages import docker
from tutumcli import utils
from . import __version__


TUTUM_FILE = '.tutum'
AUTH_SECTION = 'auth'
USER_OPTION = "user"
APIKEY_OPTION = 'apikey'
AUTH_ERROR = 'auth_error'
NO_ERROR = 'no_error'

TUTUM_AUTH_ERROR_EXIT_CODE = 2
EXCEPTION_EXIT_CODE = 3


def login():
    def try_register(_username, _password):
        email = raw_input("Email: ")

        headers = {"Content-Type": "application/json", "User-Agent": "tutum/%s" % __version__}
        data = {'username': _username, "password1": _password, "password2": _password, "email": email}

        r = requests.post(urlparse.urljoin(tutum.base_url, "register/"), data=json.dumps(data), headers=headers)

        try:
            if r.status_code == 201:
                return True, "Account created. Please check your email for activation instructions."
            elif r.status_code == 429:
                return False, "Too many retries. Please login again later."
            else:
                messages = r.json()['register']
                if isinstance(messages, dict):
                    _text = []
                    for key in messages.keys():
                        _text.append("%s: %s" % (key, '\n'.join(messages[key])))
                    _text = '\n'.join(_text)
                else:
                    _text = messages
                return False, _text
        except Exception:
            return False, r.text

    username = raw_input("Username: ")
    password = getpass.getpass()
    try:
        user, api_key = auth.get_auth(username, password)
        if api_key is not None:
            config = ConfigParser.ConfigParser()
            config.add_section(AUTH_SECTION)
            config.set(AUTH_SECTION, USER_OPTION, user)
            config.set(AUTH_SECTION, APIKEY_OPTION, api_key)
            with open(join(expanduser('~'), TUTUM_FILE), 'w') as cfgfile:
                config.write(cfgfile)
            print("Login succeeded!")
    except exceptions.TutumAuthError:
        registered, text = try_register(username, password)
        if registered:
            print(text)
        else:
            if 'username: A user with that username already exists.' in text:
                print("Wrong username and/or password. Please try to login again", file=sys.stderr)
                sys.exit(TUTUM_AUTH_ERROR_EXIT_CODE)
            text = text.replace('password1', 'password')
            text = text.replace('password2', 'password')
            text = text.replace('\npassword: This field is required.', '', 1)
            print(text, file=sys.stderr)
            sys.exit(TUTUM_AUTH_ERROR_EXIT_CODE)
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(EXCEPTION_EXIT_CODE)


def build(tag, working_directory, quiet, no_cache):
    try:
        directory = abspath(working_directory)
        dockerfile_path = join(directory, "Dockerfile")

        if not isfile(dockerfile_path):
            procfile_path = join(directory, "Procfile")
            ports = ""
            process = ''
            if isfile(procfile_path):
                cmd = ['"/start"']
                with open(procfile_path) as procfile:
                    datamap = yaml.load(procfile)
                if len(datamap) > 1:
                    while not process or (not process in datamap):
                        process = raw_input("Process type to build, %s: " % datamap.keys())
                    process = '"%s"' % process

                if (len(datamap) == 1 and 'web' in datamap) or (process == 'web'):
                    ports = "80"
                    process = '"web"'

                cmd.append(process)

            else:
                while not process:
                    process = raw_input("Run command: ")
                cmd = process

            if process != '"web"':
                port_regexp = re.compile('^\d{1,5}(\s\d{1,5})*$')
                while not ports or not bool(port_regexp.match(ports)):
                    ports = raw_input("Exposed Ports (ports separated by whitespace) i.e. 80 8000: ") or ""

            utils.build_dockerfile(dockerfile_path, ports, cmd)

        docker_client = utils.get_docker_client()
        stream = docker_client.build(path=directory, tag=tag, quiet=quiet, nocache=no_cache, rm=True, stream=True)
        try:
            utils.stream_output(stream, sys.stdout)
        except Exception as e:
            print(e.message, file=sys.stderr)
        print(tag)
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(EXCEPTION_EXIT_CODE)


def apps_alias(identifiers, dns):
    has_exception = False
    for identifier in identifiers:
        try:
            app_details = utils.fetch_remote_app(identifier)
            if dns is not None:
                app_details.web_public_dns = dns
                result = app_details.save()
                if result:
                    print(app_details.uuid)
        except Exception as e:
            print(e, file=sys.stderr)
            has_exception = True
    if has_exception:
        sys.exit(EXCEPTION_EXIT_CODE)


def apps_inspect(identifiers):
    has_exception = False
    for identifier in identifiers:
        try:
            app = utils.fetch_remote_app(identifier)
            print(json.dumps(tutum.Application.fetch(app.uuid).get_all_attributes(), indent=2))
        except Exception as e:
            print(e, file=sys.stderr)
            has_exception = True
    if has_exception:
        sys.exit(EXCEPTION_EXIT_CODE)


def apps_logs(identifiers):
    has_exception = False
    for identifier in identifiers:
        try:
            app = utils.fetch_remote_app(identifier)
            print(app.logs)
        except Exception as e:
            print(e, file=sys.stderr)
            has_exception = True
    if has_exception:
        sys.exit(EXCEPTION_EXIT_CODE)


def apps_open():
    try:
        app_list = tutum.Application.list()
        deployed_datetimes = {}
        for app in app_list:
            if app.web_public_dns and app.state in ["Running", "Partly running"]:
                deployed_datetimes[utils.from_utc_string_to_utc_datetime(app.deployed_datetime)] = app.web_public_dns
        if deployed_datetimes:
            max_datetime = max(deployed_datetimes.keys())
            webbrowser.open("http://" + deployed_datetimes[max_datetime])
        else:
            print("Error: There are not web applications Running or Partly Running")
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(EXCEPTION_EXIT_CODE)


def apps_ps(quiet=False, status=None):
    try:
        headers = ["NAME", "UUID", "STATUS", "IMAGE", "SIZE (#)", "DEPLOYED", "WEB HOSTNAME"]
        app_list = tutum.Application.list(state=status)
        data_list = []
        long_uuid_list = []
        for app in app_list:
            data_list.append([app.unique_name, app.uuid[:8], utils.add_unicode_symbol_to_state(app.state),
                              app.image_name, "%s (%d)" % (app.container_size, app.current_num_containers),
                              utils.get_humanize_local_datetime_from_utc_datetime_string(app.deployed_datetime),
                              app.web_public_dns])
            long_uuid_list.append(app.uuid)
        if len(data_list) == 0:
            data_list.append(["", "", "", "", "", "", ""])

        if quiet:
            for uuid in long_uuid_list:
                print(uuid)
        else:
            utils.tabulate_result(data_list, headers)

    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(EXCEPTION_EXIT_CODE)


def apps_redeploy(identifiers, tag):
    has_exception = False
    for identifier in identifiers:
        try:
            app = utils.fetch_remote_app(identifier)
            result = app.redeploy(tag)
            if result:
                print(app.uuid)
        except Exception as e:
            print(e, file=sys.stderr)
            has_exception = True
    if has_exception:
        sys.exit(EXCEPTION_EXIT_CODE)


def apps_run(image, name, container_size, target_num_containers, run_command, entrypoint, container_ports,
             container_envvars, linked_to_applications, autorestart, autoreplace, autodestroy, roles, sequential):
    try:
        ports = utils.parse_ports(container_ports)
        envvars = utils.parse_envvars(container_envvars)
        app = tutum.Application.create(image=image, name=name, container_size=container_size,
                                       target_num_containers=target_num_containers, run_command=run_command,
                                       entrypoint=entrypoint, container_ports=ports,
                                       container_envvars=envvars, linked_to_application=linked_to_applications,
                                       autorestart=autorestart, autoreplace=autoreplace, autodestroy=autodestroy,
                                       roles=roles, sequential_deployment=sequential)
        result = app.save()
        if result:
            print(app.uuid)
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(EXCEPTION_EXIT_CODE)


def apps_scale(identifiers, target_num_containers):
    has_exception = False
    for identifier in identifiers:
        try:
            app = utils.fetch_remote_app(identifier)
            app.target_num_containers = target_num_containers
            result = app.save()
            if result:
                print(app.uuid)
        except Exception as e:
            print(e, file=sys.stderr)
            has_exception = True
    if has_exception:
        sys.exit(EXCEPTION_EXIT_CODE)


def apps_set(autorestart, autoreplace, autodestroy, identifiers):
    has_exception = False
    for identifier in identifiers:
        try:
            app_details = utils.fetch_remote_app(identifier, raise_exceptions=True)
            if app_details is not None:
                app_details.autorestart = autorestart
                app_details.autoreplace = autoreplace
                app_details.autodestroy = autodestroy
                result = app_details.save()
                if result:
                    print(app_details.uuid)
        except Exception as e:
            print(e, file=sys.stderr)
            has_exception = True
    if has_exception:
        sys.exit(EXCEPTION_EXIT_CODE)


def apps_start(identifiers):
    has_exception = False
    for identifier in identifiers:
        try:
            app = utils.fetch_remote_app(identifier)
            result = app.start()
            if result:
                print(app.uuid)
        except Exception as e:
            print(e, file=sys.stderr)
            has_exception = True
    if has_exception:
        sys.exit(EXCEPTION_EXIT_CODE)


def apps_stop(identifiers):
    has_exception = False
    for identifier in identifiers:
        try:
            app = utils.fetch_remote_app(identifier)
            result = app.stop()
            if result:
                print(app.uuid)
        except Exception as e:
            print(e, file=sys.stderr)
            has_exception = True
    if has_exception:
        sys.exit(EXCEPTION_EXIT_CODE)


def apps_terminate(identifiers):
    has_exception = False
    for identifier in identifiers:
        try:
            app = utils.fetch_remote_app(identifier)
            result = app.delete()
            if result:
                print(app.uuid)
        except Exception as e:
            print(e, file=sys.stderr)
            has_exception = True
    if has_exception:
        sys.exit(EXCEPTION_EXIT_CODE)


def containers_inspect(identifiers):
    has_exception = False
    for identifier in identifiers:
        try:
            app = utils.fetch_remote_container(identifier)
            print(json.dumps(tutum.Container.fetch(app.uuid).get_all_attributes(), indent=2))
        except Exception as e:
            print(e, file=sys.stderr)
            has_exception = True
    if has_exception:
        sys.exit(EXCEPTION_EXIT_CODE)


def containers_logs(identifiers):
    has_exception = False
    for identifier in identifiers:
        try:
            container = utils.fetch_remote_container(identifier)
            print(container.logs)
        except Exception as e:
            print(e, file=sys.stderr)
            has_exception = True
    if has_exception:
        sys.exit(EXCEPTION_EXIT_CODE)


def containers_ps(app_identifier, quiet=False, status=None):
    try:
        headers = ["NAME", "UUID", "STATUS", "IMAGE", "RUN COMMAND", "SIZE", "EXIT CODE", "DEPLOYED", "PORTS"]

        if app_identifier is None:
            containers = tutum.Container.list(state=status)
        elif utils.is_uuid4(app_identifier):
            containers = tutum.Container.list(application__uuid=app_identifier, state=status)
        else:
            containers = tutum.Container.list(application__unique_name=app_identifier, state=status) + \
                         tutum.Container.list(application__uuid__startswith=app_identifier, state=status)

        data_list = []
        long_uuid_list = []

        for container in containers:
            ports = []
            for index, port in enumerate(container.container_ports):
                ports_string = ""
                if port['outer_port'] is not None:
                    ports_string += "%s:%d->" % (container.public_dns, port['outer_port'])
                ports_string += "%d/%s" % (port['inner_port'], port['protocol'])
                ports.append(ports_string)

            ports_string = ", ".join(ports)
            data_list.append([container.unique_name, container.uuid[:8],
                              utils.add_unicode_symbol_to_state(container.state), container.image_name,
                              container.run_command, container.container_size, container.exit_code,
                              utils.get_humanize_local_datetime_from_utc_datetime_string(container.deployed_datetime),
                              ports_string])
            long_uuid_list.append(container.uuid)
        if len(data_list) == 0:
            data_list.append(["", "", "", "", "", "", "", "", ""])
        if quiet:
            for uuid in long_uuid_list:
                print(uuid)
        else:
            utils.tabulate_result(data_list, headers)
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(EXCEPTION_EXIT_CODE)


def containers_start(identifiers):
    has_exception = False
    for identifier in identifiers:
        try:
            container = utils.fetch_remote_container(identifier)
            result = container.start()
            if result:
                print(container.uuid)
        except Exception as e:
            print(e, file=sys.stderr)
            has_exception = True
    if has_exception:
        sys.exit(EXCEPTION_EXIT_CODE)


def containers_stop(identifiers):
    has_exception = False
    for identifier in identifiers:
        try:
            container = utils.fetch_remote_container(identifier)
            result = container.stop()
            if result:
                print(container.uuid)
        except Exception as e:
            print(e, file=sys.stderr)
            has_exception = True
    if has_exception:
        sys.exit(EXCEPTION_EXIT_CODE)


def containers_terminate(identifiers):
    has_exception = False
    for identifier in identifiers:
        try:
            container = utils.fetch_remote_container(identifier)
            result = container.delete()
            if result:
                print(container.uuid)
        except Exception as e:
            print(e, file=sys.stderr)
            has_exception = True
    if has_exception:
        sys.exit(EXCEPTION_EXIT_CODE)


def images_list(quiet=False, jumpstarts=False, linux=False):
    try:

        headers = ["NAME", "DESCRIPTION"]
        data_list = []
        name_list = []
        if jumpstarts:
            image_list = tutum.Image.list(starred=True)
        elif linux:
            image_list = tutum.Image.list(base_image=True)
        else:
            image_list = tutum.Image.list(is_private_image=True)
        if len(image_list) != 0:
            for image in image_list:
                data_list.append([image.name, image.description])
                name_list.append(image.name)
        else:
            data_list.append(["", ""])

        if quiet:
            for name in name_list:
                print(name)
        else:
            utils.tabulate_result(data_list, headers)

    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(EXCEPTION_EXIT_CODE)


def images_register(repository, description):
    print('Please input username and password of the repository:')
    username = raw_input('Username: ')
    password = getpass.getpass()
    try:
        image = tutum.Image.create(name=repository, username=username, password=password, description=description)
        result = image.save()
        if result:
            print(image.name)
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(EXCEPTION_EXIT_CODE)


def images_push(name, public):
    def push_to_public(repository):
        print('Pushing %s to public registry ...' % repository)

        output_status = NO_ERROR
        #tag a image to its name to check if the images exists
        try:
            docker_client.tag(name, name)
        except Exception as e:
            print(e, file=sys.stderr)
            sys.exit(EXCEPTION_EXIT_CODE)
        try:
            stream = docker_client.push(repository, stream=True)
            utils.stream_output(stream, sys.stdout)
        except StreamOutputError as e:
            if 'status 401' in e.message.lower():
                output_status = AUTH_ERROR
            else:
                print(e, file=sys.stderr)
                sys.exit(EXCEPTION_EXIT_CODE)
        except Exception as e:
            print(e.message, file=sys.stderr)
            sys.exit(EXCEPTION_EXIT_CODE)

        if output_status == NO_ERROR:
            print('')
            sys.exit()

        if output_status == AUTH_ERROR:
            print('Please login prior to push:')
            username = raw_input('Username: ')
            password = getpass.getpass()
            email = raw_input('Email: ')
            try:
                result = docker_client.login(username, password=password, email=email)
                if isinstance(result, dict):
                    print(result.get('Status', None))
            except Exception as e:
                print(e, file=sys.stderr)
                sys.exit(TUTUM_AUTH_ERROR_EXIT_CODE)
            push_to_public(repository)

    def push_to_tutum(repository):
        print('Pushing %s to Tutum private registry ...' % repository)

        user = tutum.user
        apikey = tutum.apikey
        if user is None or apikey is None:
            print('Not authorized')
            sys.exit(TUTUM_AUTH_ERROR_EXIT_CODE)

        try:
            registry = os.getenv('TUTUM_REGISTRY_URL') or 'https://r.tutum.co/v1/'
            docker_client.login(user, apikey, registry=registry)
        except Exception as e:
            print(e, file=sys.stderr)
            sys.exit(TUTUM_AUTH_ERROR_EXIT_CODE)

        if repository:
            repository = filter(None, repository.split('/'))[-1]
        repository = '%s/%s/%s' % (registry.split('//')[-1].split('/')[0], user, repository)

        try:
            print('Tagging %s as %s ...' % (name, repository))
            docker_client.tag(name, repository)
        except Exception as e:
            print(e, file=sys.stderr)
            sys.exit(EXCEPTION_EXIT_CODE)

        stream = docker_client.push(repository, stream=True)
        try:
            utils.stream_output(stream, sys.stdout)
        except docker.client.APIError as e:
            print(e.explanation, file=sys.stderr)
            sys.exit(EXCEPTION_EXIT_CODE)
        except Exception as e:
            print(e.message, file=sys.stderr)
            sys.exit(EXCEPTION_EXIT_CODE)
        print('')

    docker_client = utils.get_docker_client()
    if public:
        push_to_public(name)
    else:
        push_to_tutum(name)


def images_rm(repositories):
    has_exception = False
    for repository in repositories:
        try:
            image = tutum.Image.fetch(repository)
            result = image.delete()
            if result:
                print(repository)
        except Exception as e:
            print(e, file=sys.stderr)
            has_exception = True
    if has_exception:
        sys.exit(EXCEPTION_EXIT_CODE)


def images_search(text):
    try:
        docker_client = utils.get_docker_client()
        results = docker_client.search(text)
        headers = ["NAME", "DESCRIPTION", "STARS", "OFFICIAL", "TRUSTED"]
        data_list = []
        if len(results) != 0:
            for result in results:
                description = result["description"].replace("\n", "\\n")
                description = description[:80] + " [...]" if len(result["description"]) > 80 else description
                data_list.append([result["name"], description, str(result["star_count"]),
                                  u"\u2713" if result["is_official"] else "",
                                  u"\u2713" if result["is_trusted"] else ""])
        else:
            data_list.append(["", "", "", "", ""])
        utils.tabulate_result(data_list, headers)
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(EXCEPTION_EXIT_CODE)


def images_update(repositories, username, password, description):
    for repository in repositories:
        try:
            image = tutum.Image.fetch(repository)
            if username is not None:
                image.username = username
            if password is not None:
                image.password = password
            if description is not None:
                image.description = description
            result = image.save()
            if result:
                print(image.name)
        except Exception as e:
            print(e, file=sys.stderr)
