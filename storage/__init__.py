from storage.db import Smappee
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import configparser
import os
import pika
from .db import Base
import click
import importlib
from jsonschema import ValidationError


@click.group()
def cli():
    pass


@cli.command()
@click.option('--config_root',default='Smappee')
@click.option('--application_setting_path')
def create_table(config_root, application_setting_path):

    if application_setting_path is None:
        if 'APP_SETTINGS' not in os.environ:
            raise Exception('APP_SETTINGS env variable is {} missing.'.format(config_root))

        application_setting_path = os.environ['APP_SETTINGS']

    config = configparser.ConfigParser()
    config.read(application_setting_path)

    if config_root not in config:
        raise Exception('section {} missing.'.format(config_root))

    root = config[config_root]

    for key in ('database_uri',) not in root.items(config_root)[1:]:

        raise Exception('key {} is missing in section {}.'.format(key, config_root))

    some_engine = create_engine(config_root['database_uri'])
    Base.metadata.create_all(some_engine)


@cli.command()
@click.option('--config_root', default='Smappee')
@click.option('--application_setting_path')
def start(config_root, application_setting_path):

    if application_setting_path is None:
        if 'APP_SETTINGS' not in os.environ:
            raise Exception('APP_SETTINGS env variable is {} missing.'.format(config_root))

        application_setting_path = os.environ['APP_SETTINGS']

    config = configparser.ConfigParser()
    config.read(application_setting_path)

    if config_root not in config:
        raise Exception('section {} missing.'.format(config_root))

    root = config[config_root]

    invalid_keys = [i for i in ('rabbitmq_user', 'rabbitmq_password', 'rabbitmq_host', 'transform_method',
                                'rabbitmq_exchange', 'rabbitmq_routing_key', 'database_uri') if i not in root.keys()]

    for key in invalid_keys:
        raise Exception('key {} is missing in section {}.'.format(key, config_root))

    some_engine = create_engine(root.get('database_uri', raw=True))

    Session = sessionmaker(bind=some_engine)

    credentials = pika.PlainCredentials(root['rabbitmq_user'], root.get('rabbitmq_password', raw=True))
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=root['rabbitmq_host'], credentials=credentials))

    channel = connection.channel()

    queue = channel.queue_declare(exclusive=True)
    channel.queue_bind(exchange=root['rabbitmq_exchange'],
                       queue=queue.method.queue, routing_key=root['rabbitmq_routing_key'])

    path = root['transform_method']
    module_name, _, func_name = path.rpartition('.')
    transform = getattr(importlib.import_module(module_name), func_name)

    def callback(ch, method, properties, body):
        try:
            session = Session()
            session.add(transform(body))
            session.commit()

            ch.basic_ack(delivery_tag=method.delivery_tag)
        except ValidationError:
            click.echo('Message validation failed', err=True)

    channel.basic_consume(callback, queue=queue.method.queue)

    try:
        click.echo('start_consuming ...')
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()

    connection.close()


def main():
    """ console command entry point """
    cli()
