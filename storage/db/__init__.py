from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime

Base = declarative_base()


class Smappee(Base):
    __tablename__ = 'smappee'

    utc_timestamp = Column(DateTime, primary_key=True)
    total_power = Column(Integer)
    total_reactive_power = Column(Integer)
    total_export_energy = Column(Integer)
    total_import_energy = Column(Integer)
    monitor_status = Column(Integer)

    for i in range(6):  # 6 connections
        locals()['ct_input{}'.format(i)] = Column(Integer)
        locals()['power{}'.format(i)] = Column(Integer)
        locals()['export_energy{}'.format(i)] = Column(Integer)
        locals()['import_energy{}'.format(i)] = Column(Integer)
        locals()['phase_id{}'.format(i)] = Column(Integer)
        locals()['current{}'.format(i)] = Column(Integer)

    for i in range(3):  # 3 phases
        locals()['volt{}'.format(i)] = Column(Integer)
        locals()['phase_id{}'.format(i)] = Column(Integer)
