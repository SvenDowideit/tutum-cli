import datetime
import re
import multiprocessing

from tabulate import tabulate
import tutum
from dateutil import tz
import ago
import docker
from os import getenv

from tutumcli.exceptions import NonUniqueIdentifier, ObjectNotFound, BadParameter, DockerNotFound

TUTUM_LOCAL_PREFIX = "local-"
TUTUM_LOCAL_CONTAINER_NAME = TUTUM_LOCAL_PREFIX + "%s"

CONTAINER_SIZE = {
        "XS": {"cpu_shares": 256, "memory": 268435456},
        "S": {"cpu_shares": 512, "memory": 536870912},
        "M": {"cpu_shares": 1024, "memory": 1073741824},
        "L": {"cpu_shares": 2048, "memory": 2147483648},
        "XL": {"cpu_shares": 4096, "memory": 4294967286}
}


def tabulate_result(data_list, headers):
    print tabulate(data_list, headers, stralign="left", tablefmt="plain")


def _from_utc_string_to_utc_datetime(utc_datetime_string):
    if not utc_datetime_string:
        return None
    utc_date_object = datetime.datetime.strptime(utc_datetime_string, "%a, %d %b %Y %H:%M:%S +0000")

    return utc_date_object


def get_humanize_local_datetime_from_utc_datetime_string(utc_datetime_string):
    utc_target_datetime = _from_utc_string_to_utc_datetime(utc_datetime_string)
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


def fetch_container(identifier, raise_exceptions=True):

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


def fetch_app(identifier, raise_exceptions=True):

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
    parsed_ports = []
    if port_list is not None:
        parsed_ports = []
        for port in port_list:
            parsed_ports.append(_get_port_dict(port))
    return parsed_ports


def _get_port_dict(port):
    port_regexp = re.compile('^[0-9]{1,5}/(tcp|udp)$')
    match = port_regexp.match(port)
    if bool(match):
        port = port.split("/", 1)
        inner_port = int(port[0])
        protocol = port[1].lower()
        return {'protocol': protocol, 'inner_port': inner_port}
    raise BadParameter("Port argument %s does not match with 'port/protocol'. Example: 80/tcp" % port)


def parse_envvars(envvar_list):
    parsed_envvars = []
    if envvar_list is not None:
        for envvar in envvar_list:
            parsed_envvars.append(_is_envvar(envvar))
    return parsed_envvars


def _is_envvar(envvar):
    envvar_regexp = re.compile('^[a-zA-Z_]+[a-zA-Z0-9_]*=[^?!=]+$')
    match = envvar_regexp.match(envvar)
    if bool(match):
        envvar = envvar.split("=", 1)
        return {'key': envvar[0], 'value': envvar[1]}
    raise BadParameter("Environment Variable argument %s does not match with 'KEY=VALUE'. Example: ENVVAR=foo" % envvar)


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


def launch_queries_in_parallel(identifier):

    pool = multiprocessing.Pool(processes=2)
    apps_result = pool.apply_async(fetch_app, (identifier, False, ))
    containers_result = pool.apply_async(fetch_container, (identifier, False, ))
    pool.close()
    pool.join()

    app = apps_result.get()
    container = containers_result.get()

    if isinstance(app, ObjectNotFound) and isinstance(container, ObjectNotFound):
        raise ObjectNotFound("Cannot find an application or a container with identifier '%s'" % identifier)
    elif isinstance(app, NonUniqueIdentifier) or isinstance(container, NonUniqueIdentifier) or \
            (not isinstance(app, Exception) and isinstance(container, Exception)):
        raise NonUniqueIdentifier("Identifier '%s' is being used by more than one container and/or application, "
                                  "please use the long uuid" % identifier)
    elif not isinstance(app, ObjectNotFound):
        return app

    elif not isinstance(container, ObjectNotFound):
        return container

    return None


def get_docker_client():
    try:
        docker_client = docker.Client(base_url=getenv("DOCKER_HOST"))
        docker_client.version()
        return docker_client
    except Exception:
        raise DockerNotFound("Cannot connect to docker (is it running?)")


def parse_image_name(image_name):
    regexp = r"^(?P<full_name>((?P<registry_host>[a-z0-9\.\-]+\.[a-z0-9\.\-]+)/)?" \
             r"(?P<name_without_host>((?P<namespace>[a-z0-9\.\-]+)/)?" \
             r"(?P<short_name>[a-z0-9\.\-_]+)))(:(?P<tag>[a-z0-9\.\-]+))?$"
    if not re.search(regexp, str(image_name)):
        raise Exception("Invalid image name")
    parsed_results = re.match(regexp, str(image_name)).groupdict()
    parsed_results["index"] = "index.docker.io"
    return parsed_results


def get_app_and_containers_unique_name(name, num_containers=1):
    current_apps = get_current_apps_and_its_containers()
    similar_names = {}

    for app_name, config in current_apps.iteritems():
        if app_name.startswith(name):
            similar_names[app_name] = config["containers"]

    app_name = None
    if not name in similar_names:
        app_name = name
    else:
        i = 1
        while not app_name:
            new_name = name + "-" + str(i)
            if not new_name in similar_names:
                app_name = new_name
                break
            i += 1
    return app_name, get_containers_unique_names(app_name, [], num_containers)


def get_containers_unique_names(app_name, current_containers=[], num_containers=1):
    container_names = []
    for i in range(num_containers):
        i = 1
        container_name = None
        while not container_name:
            new_name = app_name + "-" + str(i)
            if not new_name in current_containers and not new_name in container_names:
                container_name = new_name
                container_names.append(container_name)
            i += 1
    return container_names


def get_current_apps_and_its_containers():
    docker_client = get_docker_client()
    stopped_running_containers = docker_client.containers(all=True, quiet=True)
    current_apps = {}
    deployed_datetime = datetime.datetime.utcnow()

    for container in stopped_running_containers:
        inspected_container = docker_client.inspect_container(container["Id"])
        app_name = get_app_name_from_container_name(inspected_container['Name'][1:])
        size_by_cpu = get_size_from_cpu_shares(inspected_container["Config"]["CpuShares"])
        size_by_memory = get_size_from_memory(inspected_container["Config"]["Memory"])

        if not app_name or not size_by_cpu or not size_by_memory or size_by_cpu != size_by_memory:
            #it is not a tutum container
            continue
        app_config = current_apps.get(app_name, {"uuid": "", "status": "",
                                                 "image": inspected_container["Config"]["Image"],
                                                 "container_size": size_by_cpu,
                                                 "deployed": "",
                                                 "web_hostname": "", "containers": []})

        container_status = "Running" if inspected_container["State"]["Running"] else "Stopped"
        if container_status == "Stopped" and inspected_container["State"]["ExitCode"] != 0:
            container_status = "Stopped with errors"
        container_config = {"name": inspected_container['Name'][1:],
                            "uuid": inspected_container["ID"],
                            "status": container_status,
                            "image": inspected_container["Config"]["Image"],
                            "run_command": " ".join(inspected_container["Config"]["Cmd"]),
                            "size": size_by_cpu,
                            "exit_code": inspected_container["State"]["ExitCode"],
                            "deployed": datetime.datetime.strptime(inspected_container["Created"].split(".")[0],
                                                                   "%Y-%m-%dT%H:%M:%S")}
        ports = ""
        if inspected_container["HostConfig"]["PortBindings"] is not None:
            for port, bindings in inspected_container["HostConfig"]["PortBindings"].iteritems():
                port_number_protocol = port.split("/")
                for binding in bindings:
                    ports += "%s:%s->%s/%s, " % \
                             (binding["HostIp"], binding["HostPort"], port_number_protocol[0], port_number_protocol[1])
        ports = ports if ports == "" else ports[:-2]
        container_config["ports"] = ports
        app_config["containers"].append(container_config)

        app_config["deployed"] = container_config["deployed"] \
            if container_config["deployed"] < deployed_datetime else deployed_datetime

        current_apps[app_name] = app_config

    for app, app_config in current_apps.iteritems():
        current_apps[app]["status"] = _calculate_local_app_status(app_config["containers"])

    return current_apps


def get_app_name_from_container_name(container_local_name):
    local_name_regexp = re.compile('^local\-([a-zA-Z0-9_\-]+)\-([0-9]+)$')
    match = local_name_regexp.match(container_local_name)
    if bool(match):
        split_name = container_local_name.split("-")
        return "-".join(split_name[:-1])
    return None


def get_size_from_cpu_shares(cpu_shares_value):
    for size, config in CONTAINER_SIZE.iteritems():
        if config["cpu_shares"] == cpu_shares_value:
            return size
    return None


def get_size_from_memory(memory_value):
    for size, config in CONTAINER_SIZE.iteritems():
        if config["memory"] == memory_value:
            return size
    return None


def _calculate_local_app_status(container_list):
    all_status = {}

    for container in container_list:
        number = all_status.get(container["status"], 0)
        all_status[container["status"]] = number + 1

    if all_status.get("Running", 0) != 0:
        if all_status.get("Stopped", 0) == all_status.get("Stopped with errors", 0) == 0:
            return "Running"
        else:
            return "Partly running"
    else:
        if all_status.get("Stopped", 0) == 0 and all_status.get("Stopped with errors", 0) != 0:
            return "Stopped with errors"
        else:
            return "Stopped"
