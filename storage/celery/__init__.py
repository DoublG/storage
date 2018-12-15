from celery import Celery
import os
import configparser

if 'APP_SETTINGS' not in os.environ:
    raise Exception('APP_SETTINGS env variable is {} missing.'.format('APP_SETTINGS'))

application_setting_path = os.environ['APP_SETTINGS']

config = configparser.ConfigParser()
config.read(application_setting_path)

app = Celery('storage', include=['storage.celery.tasks'], broker=config['Celery']['broker_url'],
             backend=config['Celery']['result_backend'])

app.conf.broker_use_ssl = True