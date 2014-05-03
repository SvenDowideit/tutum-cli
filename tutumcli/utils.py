from __future__ import print_function
import datetime
import re
import json
import sys
from os import getenv

from tabulate import tabulate
import tutum
from dateutil import tz
import ago
import docker

from tutumcli.exceptions import NonUniqueIdentifier, ObjectNotFound, BadParameter, DockerNotFound


def tabulate_result(data_list, headers):
    print (tabulate(data_list, headers, stralign="left", tablefmt="plain"))


def from_utc_string_to_utc_datetime(utc_datetime_string):
    if not utc_datetime_string:
        return None
    utc_date_object = datetime.datetime.strptime(utc_datetime_string, "%a, %d %b %Y %H:%M:%S +0000")

    return utc_date_object


def get_humanize_local_datetime_from_utc_datetime_string(utc_datetime_string):
    utc_target_datetime = from_utc_string_to_utc_datetime(utc_datetime_string)
    return get_humanize_local_datetime_from_utc_datetime(utc_target_datetime)


def get_humanize_local_datetime_from_utc_datetime(utc_target_datetime):
    local_now = datetime.datetime.now(tz.tzlocal())
    if utc_target_datetime:
        local_target_datetime = utc_target_datetime.replace(tzinfo=tz.gettz("UTC")).astimezone(tz=tz.tzlocal())
        return ago.human(local_now - local_target_datetime, precision=1)
    return ""


def is_uuid4(identifier):
    uuid4_regexp = re.compile('^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}', re.I)
    match = uuid4_regexp.match(identifier)
    return bool(match)


def fetch_remote_container(identifier, raise_exceptions=True):
    try:
        if is_uuid4(identifier):
            try:
                return tutum.Container.fetch(identifier)
            except Exception:
                raise ObjectNotFound("Cannot find a container with the identifier '%s'" % identifier)
        else:
            objects_same_identifier = tutum.Container.list(unique_name=identifier) or \
                                      tutum.Container.list(uuid__startswith=identifier)
            if len(objects_same_identifier) == 1:
                return objects_same_identifier[0]
            elif len(objects_same_identifier) == 0:
                raise ObjectNotFound("Cannot find a container with the identifier '%s'" % identifier)
            raise NonUniqueIdentifier("More than one container has the same identifier, please use the long uuid")

    except (NonUniqueIdentifier, ObjectNotFound) as e:
        if not raise_exceptions:
            return e
        raise e


def fetch_remote_app(identifier, raise_exceptions=True):
    try:
        if is_uuid4(identifier):
            try:
                return tutum.Application.fetch(identifier)
            except Exception:
                raise ObjectNotFound("Cannot find an application with the identifier '%s'" % identifier)
        else:
            objects_same_identifier = tutum.Application.list(unique_name=identifier) or \
                                      tutum.Application.list(uuid__startswith=identifier)
            if len(objects_same_identifier) == 1:
                return objects_same_identifier[0]
            elif len(objects_same_identifier) == 0:
                raise ObjectNotFound("Cannot find an application with the identifier '%s'" % identifier)
            raise NonUniqueIdentifier("More than one application has the same identifier, please use the long uuid")
    except (NonUniqueIdentifier, ObjectNotFound) as e:
        if not raise_exceptions:
            return e
        raise e


def parse_ports(port_list):
    def _get_port_dict(_port):
        port_regexp = re.compile('^[0-9]{1,5}/(tcp|udp)$')
        match = port_regexp.match(_port)
        if bool(match):
            _port = _port.split("/", 1)
            inner_port = int(_port[0])
            protocol = _port[1].lower()
            return {'protocol': protocol, 'inner_port': inner_port}
        raise BadParameter("Port argument %s does not match with 'port/protocol'. Example: 80/tcp" % _port)

    parsed_ports = []
    if port_list is not None:
        parsed_ports = []
        for port in port_list:
            parsed_ports.append(_get_port_dict(port))
    return parsed_ports


def parse_envvars(envvar_list):
    def _is_envvar(_envvar):
        envvar_regexp = re.compile('^[a-zA-Z_]+[a-zA-Z0-9_]*=[^?!=]+$')
        match = envvar_regexp.match(_envvar)
        if bool(match):
            _envvar = _envvar.split("=", 1)
            return {'key': _envvar[0], 'value': _envvar[1]}
        raise BadParameter("Environment Variable argument %s does not match with 'KEY=VALUE'."
                           " Example: ENVVAR=foo" % _envvar)

    parsed_envvars = []
    if envvar_list is not None:
        for envvar in envvar_list:
            parsed_envvars.append(_is_envvar(envvar))
    return parsed_envvars


def add_unicode_symbol_to_state(state):
    if state in ["Running", "Partly running"]:
        return u"\u25B6 " + state
    elif state in ["Init", "Stopped"]:
        return u"\u25FC " + state
    elif state in ["Starting", "Stopping", "Scaling", "Terminating"]:
        return u"\u2699 " + state
    elif state in ["Start failed", "Stopped with errors"]:
        return u"\u0021 " + state
    elif state == "Terminated":
        return u"\u2718 " + state
    return state


def get_docker_client():
    try:
        docker_client = docker.Client(base_url=getenv("DOCKER_HOST"))
        docker_client.version()
        return docker_client
    except Exception:
        raise DockerNotFound("Cannot connect to docker (is it running?)")


def build_dockerfile(filepath, ports, command):
    with open(filepath, "w") as dockerfile:
        base_image = "FROM tutum/buildstep\n\n"
        expose_ports = " ".join(["EXPOSE", ports]) + "\n\n" if ports else ""
        if isinstance(command, list):
            command = ','.join(command)
            command = '[%s]' % command
        cmd = " ".join(["CMD", command])

        for line in [base_image, expose_ports, cmd]:
            if line:
                dockerfile.write(line)


def print_stream_line(output):
    if "}{" in output:
        lines = output.replace('}{', '}}{{').split('}{')
    else:
        lines = [output]
    print_stream_line.last_id = None
    for line in lines:
        formatted_output = ''
        try:
            obj = json.loads(line)
            status = obj.get('status', None)
            identifier = obj.get('id', None)
            progress = obj.get('progress', None)
            error = obj.get('error', None)

            if error:
                print('', file=sys.stderr)
                print(error, file=sys.stderr)
                break

            if status and identifier and progress:
                if identifier != print_stream_line.last_id:
                    formatted_output = '\n%s: %s %s' % (identifier, status, progress)
                else:
                    formatted_output = '\r%s: %s %s\033[K' % (identifier, status, progress)
                print_stream_line.last_id = identifier
            elif status and identifier:
                if identifier != print_stream_line.last_id:
                    formatted_output = '\n%s: %s' % (identifier, status)
                else:
                    formatted_output = '\r%s: %s\033[K' % (identifier, status)
                print_stream_line.last_id = identifier
            elif status:
                formatted_output = '\n%s' % status
            else:
                for key in obj.keys():
                    formatted_output = '%s' % obj.get(key, '')
        except ValueError:
            sys.stdout.write(line)

        sys.stdout.write(formatted_output)
        sys.stdout.flush()