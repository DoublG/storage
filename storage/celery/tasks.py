from __future__ import absolute_import, unicode_literals

import os

import pandas as pd
from celery.schedules import crontab
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

from storage.celery import app
from storage.db import Smappee
from . import config

logger.add("logs/storage_tasks.log", rotation="1 hour")


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=6, minute=0, day_of_month=1, day_of_week='*', month_of_year="*"), cleanup_db.s(),
        name='Store the oldest month in a parquet file')


@app.task(time_limit=3600)
@logger.catch
def cleanup_db():
    engine = create_engine(config['Celery'].get('database_uri', raw=True))
    Session = sessionmaker(bind=engine)
    session = Session()

    # filenaming
    month, year = session.query(
        func.MONTH(func.min(Smappee.utc_timestamp)).label('first_month'),
        func.YEAR(func.min(Smappee.utc_timestamp)).label('first_year')
    ).one()

    cwd = os.getcwd()

    query = session.query(Smappee) \
        .filter(func.MONTH(Smappee.utc_timestamp) == month) \
        .filter(func.YEAR(Smappee.utc_timestamp) == year)

    chunk_size = config['Celery'].get('chunk_size')
    columns_to_fetch = [c.name for c in Smappee.__table__.columns]
    total_rows = query.count()

    logger.debug('{} rows found - will generate {} files with {chunk} records and 1 file with {} records',
                 total_rows, *divmod(total_rows, chunk_size), chunk=chunk_size)

    def _get_fields(row):
        return tuple(map(lambda column: getattr(row, column), columns_to_fetch))

    def _get_chucks(q):
        """
        Return the query in batches
        :param q: SQLAlchemy Query
        :return: list of records
        """
        e = iter(q.yield_per(chunk_size))
        while True:
            result = []
            for i in range(chunk_size):
                try:
                    row = next(e)
                except StopIteration:
                    yield result
                    return

                result.append(_get_fields(row))

            yield result

    logger.debug('Starting fetching data')

    for idx, chunk in enumerate(_get_chucks(query)):
        logger.debug('Start chunk {}', idx)
        logger.debug('{} rows to store', len(chunk))

        df = pd.DataFrame(chunk, columns=columns_to_fetch)

        filename = os.path.join(cwd, 'cold_backup/{}-{}-{}.gzip'.format(month, year, idx))
        logger.debug('{} write file', filename)

        df.to_parquet(filename, compression='gzip')

        # delete the last month
        query.delete(synchronize_session=False)

    logger.debug('End of data storage')
