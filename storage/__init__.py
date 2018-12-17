import configparser
import importlib
import os

import click
import pandas as pd
import pika
import pyarrow.parquet as pq
from jsonschema import ValidationError
from pandas import datetime
from sqlalchemy import create_engine
from sqlalchemy import exc
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

from storage.db import Smappee
from .db import Base


def _get_engine(ctx):
    config_root = ctx.obj['CONFIG_ROOT']
    root = ctx.obj['ROOT']

    if 'database_uri' not in root.keys():
        raise Exception('key {} is missing in section {}.'.format('database_uri', config_root))

    return create_engine(root.get('database_uri', raw=True))


def _get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session


def _load_config_file(config_root, application_setting_path):
    if application_setting_path is None:
        if 'APP_SETTINGS' not in os.environ:
            raise Exception('APP_SETTINGS env variable is {} missing.'.format(config_root))

        application_setting_path = os.environ['APP_SETTINGS']

    config = configparser.ConfigParser()
    config.read(application_setting_path)

    if config_root not in config:
        raise Exception('section {} missing.'.format(config_root))

    return config[config_root]


@click.group()
@click.pass_context
@click.option('--config_root', default='Smappee')
@click.option('--application_setting_path')
def cli(ctx, config_root, application_setting_path):
    ctx.obj['CONFIG_ROOT'] = config_root
    ctx.obj['SETTING_PATH'] = application_setting_path
    ctx.obj['ROOT'] = _load_config_file(config_root, application_setting_path)


@cli.command()
@click.pass_context
def create_table(ctx):
    """ create db table """

    engine = _get_engine(ctx)

    Base.metadata.create_all(engine)


@cli.command()
@click.pass_context
def start(ctx):
    """ start application """

    config_root = ctx.obj['CONFIG_ROOT']
    root = ctx.obj['ROOT']

    invalid_keys = [i for i in ('rabbitmq_user', 'rabbitmq_password', 'rabbitmq_host', 'transform_method',
                                'rabbitmq_exchange', 'rabbitmq_routing_key', 'database_uri') if i not in root.keys()]

    for key in invalid_keys:
        raise Exception('key {} is missing in section {}.'.format(key, config_root))

    Session = _get_session(_get_engine(ctx))

    credentials = pika.PlainCredentials(root['rabbitmq_user'], root.get('rabbitmq_password', raw=True))
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=root['rabbitmq_host'], credentials=credentials))

    channel = connection.channel()

    queue = channel.queue_declare(exclusive=True)
    channel.queue_bind(exchange=root['rabbitmq_exchange'],
                       queue=queue.method.queue, routing_key=root['rabbitmq_routing_key'])

    try:
        path = root['transform_method']
        module_name, _, func_name = path.rpartition('.')
        transform = getattr(importlib.import_module(module_name), func_name)
    except AttributeError as ex:
        raise Exception('method {} not found'.format(path))

    # RabbitMQ callback method
    def callback(ch, method, properties, body):
        try:
            session = Session()
            session.add(transform(body))
            session.commit()

        except (ValidationError, exc.SQLAlchemyError) as ex:
            click.echo(ex, err=True)

        ch.basic_ack(delivery_tag=method.delivery_tag)  # we always confirm the message

    channel.basic_consume(callback, queue=queue.method.queue)

    try:
        click.echo('start receiving on {}'.format(queue.method.queue))
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()

    connection.close()


@cli.command()
@click.pass_context
def process(ctx):
    """
        Join parquet files to display count, min, max, mean
    """
    path = os.path.join(os.getcwd(), 'cold_backup')
    click.echo('Load parquet files from folder {}'.format(path))

    df = pd.DataFrame()

    # load history records
    for dirpath, dirnames, files in os.walk(os.path.abspath(path)):
        for name in files:
            if name.endswith('.gzip'):
                filename = os.path.join(dirpath, name)
                click.echo('load file {}'.format(filename))

                table = pq.read_table(filename, columns=['utc_timestamp', 'total_power'])
                click.echo('rows found {}'.format(table.num_rows))

                df = df.append(table.to_pandas())

    # create day column
    df['day'] = df["utc_timestamp"].apply(lambda d: datetime(year=d.year, month=d.month, day=d.day))

    # load current data (sql)
    engine = _get_engine(ctx)
    session = _get_session(engine)()
    query = session.query(func.TIMESTAMP(func.DATE(Smappee.utc_timestamp)).label('day'),
                          func.count(Smappee.total_power).label('count'),
                          func.min(Smappee.total_power).label('min'),
                          func.max(Smappee.total_power).label('max'),
                          func.avg(Smappee.total_power).label('mean'))\
        .group_by(func.TIMESTAMP(func.DATE(Smappee.utc_timestamp)))

    pd_df = pd.read_sql(query.statement, engine, index_col=['day'])
    click.echo('{} rows selected from db'.format(len(pd_df)))

    df.set_index(df["day"], inplace=True)

    # aggregate old records
    power_overview = df['total_power'].resample('D').agg(['count', 'min', 'max', 'mean'])

    # union the aggregated new records with the old ones
    power_overview = power_overview.append(pd_df)

    click.echo(power_overview.round(2))


def main():
    """ console command entry point """
    cli(obj={})
