from __future__ import absolute_import, unicode_literals
from storage.celery import app
from sqlalchemy import create_engine
from sqlalchemy import func
from . import config
import pandas as pd
from sqlalchemy.orm import sessionmaker
from storage.db import Smappee
from celery.schedules import crontab
import os


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=6, minute=0, day_of_month=1), cleanup_db.s(), name='clean the last month')


@app.task
def cleanup_db():
    engine = create_engine(config['Celery'].get('database_uri', raw=True))
    Session = sessionmaker(bind=engine)
    session = Session()

    # filenaming
    month, year = session.query(
        func.MONTH(func.min(Smappee.utc_timestamp)).label('first_month'),
        func.YEAR(func.min(Smappee.utc_timestamp)).label('first_year')
    ).one()

    query = session.query(Smappee) \
        .filter(func.MONTH(Smappee.utc_timestamp) == month) \
        .filter(func.YEAR(Smappee.utc_timestamp) == year)

    # sql to dataframe to parquet file
    df = pd.read_sql(query.statement, engine)

    cwd = os.getcwd()
    df.to_parquet(os.path.join(cwd, '/cold_backup/{}-{}.gzip'.format(month, year)), compression='gzip')

    # delete the last month
    query.delete(synchronize_session=False)

