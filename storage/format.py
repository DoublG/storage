import json
from datetime import datetime

import glom
from glom import Coalesce, Check

from .db import Smappee

spec = {
    'utc_timestamp': ('utcTimeStamp', lambda x: datetime.fromtimestamp(x / 1000)),
    'total_power': ('totalPower', Check(type=int)),
    'total_reactive_power': ('totalReactivePower', Check(type=int)),
    'total_export_energy': ('totalExportEnergy', Check(type=int)),
    'total_import_energy': ('totalImportEnergy', Check(type=int)),
    'monitor_status': ('monitorStatus', Check(type=int)),
}

# Channel Power
for i in range(6):
    spec.update({
        'ct_input{}'.format(i): ('channelPowers.{}.ctInput'.format(i), Check(type=int)),
        'power{}'.format(i): ('channelPowers.{}.power'.format(i), Check(type=int)),
        'export_energy{}'.format(i): ('channelPowers.{}.exportEnergy'.format(i), Check(type=int)),
        'import_energy{}'.format(i): ('channelPowers.{}.importEnergy'.format(i), Check(type=int)),
        'phase_id{}'.format(i): ('channelPowers.{}.phaseId'.format(i), Check(type=int)),
        'current{}'.format(i): ('channelPowers.{}.current'.format(i), Check(type=int))
    })

# Voltages
for i in range(3):
    spec.update({
        'volt{}'.format(i): Coalesce('voltages.{}.voltage'.format(i), default=None, validate=Check(type=int)),
        'phase_id{}'.format(i): Coalesce('voltages.{}.phaseId'.format(i), default=None, validate=Check(type=int))
    })


def _external_to_internal(external_dict: dict) -> dict:
    """
    Transform incoming message to a format that the db can understand.
    :param external_dict: external message format
    :return: internal message format
    """
    return glom(external_dict, spec)


def transform_smappee(message: dict) -> object:
    message_dict = json.loads(message.decode())
    return Smappee(**_external_to_internal(message_dict))
