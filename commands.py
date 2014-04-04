import getpass
import ConfigParser
from os.path import join, expanduser
import pprint

from tutum.api import auth
from tutum.api import exceptions
import tutum

import utils


TUTUM_FILE = '.tutum'
AUTH_SECTION = 'auth'
USER_OPTION = "user"
APIKEY_OPTION = 'apikey'


def authenticate():

    username = raw_input("Username: ")
    password = getpass.getpass()
    try:
        api_key = auth.get_apikey(username, password)
        if api_key is not None:
            config = ConfigParser.ConfigParser()
            config.add_section(AUTH_SECTION)
            config.set(AUTH_SECTION, USER_OPTION, username)
            config.set(AUTH_SECTION, APIKEY_OPTION, api_key)
            print join(expanduser('~'), TUTUM_FILE)
            with open(join(expanduser('~'), TUTUM_FILE), 'w') as cfgfile:
                config.write(cfgfile)
            print "Login succeeded!"
    except exceptions.TutumAuthError:
        print "Wrong username and/or password. Please try to login again"
    except exceptions.TutumApiError as e:
        print e


def apps():
    try:
        apps = tutum.Application.list()
        headers = ["Name", "UUID", "State", "Image", "Size", "Deployed datetime"]
        data_list = []
        for app in apps:
            data_list.append([app.name, app.uuid[:8], app.state, app.image_tag, app.container_size,
                              app.deployed_datetime])
        utils.tabulate_result(data_list, headers)
    except (exceptions.TutumAuthError, exceptions.TutumApiError) as e:
        print e


def app_details(uuid):
    try:
        app_detail = tutum.Application.fetch(uuid)
        pprint.pprint(app_detail.get_all_attributes())
    except (exceptions.TutumAuthError, exceptions.TutumApiError) as e:
        print e


def app_start(uuid):
    try:
        app_detail = tutum.Application.fetch(uuid)
        result = app_detail.start()
        if result:
            print app_detail.uuid
    except (exceptions.TutumAuthError, exceptions.TutumApiError) as e:
        print e


def app_stop(uuid):
    try:
        app_detail = tutum.Application.fetch(uuid)
        result = app_detail.stop()
        if result:
            print app_detail.uuid
    except (exceptions.TutumAuthError, exceptions.TutumApiError) as e:
        print e


def app_terminate(uuid):
    try:
        app_detail = tutum.Application.fetch(uuid)
        result = app_detail.delete()
        if result:
            print app_detail.uuid
    except (exceptions.TutumAuthError, exceptions.TutumApiError) as e:
        print e


def app_update(uuid, target_num_containers, web_public_dns):
    try:
        app_detail = tutum.Application.fetch(uuid)
        if target_num_containers:
            app_detail.target_num_containers = target_num_containers
        if web_public_dns:
            app_detail.web_public_dns = web_public_dns
        if target_num_containers or web_public_dns:
            result = app_detail.save()
            if result:
                print app_detail.uuid
    except (exceptions.TutumAuthError, exceptions.TutumApiError) as e:
        print e


def app_create(**kwargs):
    try:
        app = tutum.Application.create(**kwargs)
        result = app.save()
        if result:
            print app.uuid
    except (exceptions.TutumAuthError, exceptions.TutumApiError) as e:
        print e