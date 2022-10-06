# config.py
import json


def get_app_config(env_name):

    with open('config/app_config.json', 'r') as f:
        app_cfg = json.load(f)

    class app_config(object):

        SECRET_KEY = 'DEFAULT_CS_KEY'
        FIRST_NAME = app_cfg[env_name]['DEFAULTS']['FIRST_NAME']
        LAST_NAME = app_cfg[env_name]['DEFAULTS']['LAST_NAME']
        USER_EMAIL = app_cfg[env_name]['DEFAULTS']['USER_EMAIL']

        # flask
        DEBUG = app_cfg[env_name]['FLASK']['DEBUG']
        HOST = app_cfg[env_name]['FLASK']['HOST']
        ENV = app_cfg[env_name]['FLASK']['ENV']
        ASSETS_DEBUG = bool(app_cfg[env_name]['FLASK']['ASSETS_DEBUG'])
        EXPLAIN_TEMPLATE_LOADING = bool(app_cfg[env_name]['FLASK']['EXPLAIN_TEMPLATE_LOADING'])

    AppConfig = app_config()

    return AppConfig
