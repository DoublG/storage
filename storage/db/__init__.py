from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import composite

Base = declarative_base()


class Smappee(Base):
    __tablename__ = 'smappee'

    utc_timestamp = Column(DateTime, primary_key=True)
    total_power = Column(Integer)
    total_reactive_power = Column(Integer)
    total_export_energy = Column(Integer)
    total_import_energy = Column(Integer)
    monitor_status = Column(Integer)

    ct_input0 = Column(Integer)
    power0 = Column(Integer)
    export_energy0 = Column(Integer)
    import_energy0 = Column(Integer)
    phase_id0 = Column(Integer)
    current0 = Column(Integer)

    ct_input1 = Column(Integer)
    power1 = Column(Integer)
    export_energy1 = Column(Integer)
    import_energy1 = Column(Integer)
    phase_id1 = Column(Integer)
    current1 = Column(Integer)

    ct_input2 = Column(Integer)
    power2 = Column(Integer)
    export_energy2 = Column(Integer)
    import_energy2 = Column(Integer)
    phase_id2 = Column(Integer)
    current2 = Column(Integer)

    ct_input3 = Column(Integer)
    power3 = Column(Integer)
    export_energy3 = Column(Integer)
    import_energy3 = Column(Integer)
    phase_id3 = Column(Integer)
    current3 = Column(Integer)

    ct_input4 = Column(Integer)
    power4 = Column(Integer)
    export_energy4 = Column(Integer)
    import_energy4 = Column(Integer)
    phase_id4 = Column(Integer)
    current4 = Column(Integer)

    ct_input5 = Column(Integer)
    power5 = Column(Integer)
    export_energy5 = Column(Integer)
    import_energy5 = Column(Integer)
    phase_id5 = Column(Integer)
    current5 = Column(Integer)

    volt0 = Column(Integer)
    phase_id0 = Column(Integer)

    volt1 = Column(Integer)
    phase_id1 = Column(Integer)

    volt2 = Column(Integer)
    phase_id2 = Column(Integer)