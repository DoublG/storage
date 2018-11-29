from .db import Smappee
from datetime import datetime
from jsonschema import validate
import json

# {"totalPower": 653,
#  "totalReactivePower": 501,
#  "totalExportEnergy": 0,
#  "totalImportEnergy": 864146084,
#  "monitorStatus": 0,
#  "utcTimeStamp": 1543156626563,
#  "channelPowers": [
#      {"ctInput": 0, "power": 101, "exportEnergy": 0, "importEnergy": 220879977, "phaseId": 0, "current": 5},
#      {"ctInput": 1, "power": 184, "exportEnergy": 0, "importEnergy": 307981528, "phaseId": 1, "current": 12},
#      {"ctInput": 2, "power": 368, "exportEnergy": 0, "importEnergy": 335286286, "phaseId": 2, "current": 18},
#      {"ctInput": 3, "power": 0, "exportEnergy": 0, "importEnergy": 898, "phaseId": 0, "current": 0},
#      {"ctInput": 4, "power": 0, "exportEnergy": 17727, "importEnergy": 13940069, "phaseId": 1, "current": 1},
#      {"ctInput": 5, "power": 69, "exportEnergy": 2068841, "importEnergy": 245618083, "phaseId": 2, "current": 10}],
#  "voltages": [{"voltage": 236, "phaseId": 0}]}

validation = {
    "type": "object",
    "properties": {
        "totalPower": {"type": "number"},
        "totalReactivePower": {"type": "number"},
        "totalExportEnergy": {"type": "number"},
        "monitorStatus": {"type": "number"},
        "utcTimeStamp": {"type": "number"},
        "channelPowers": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "ctInput": {"type": "number"},
                    "power": {"type": "number"},
                    "exportEnergy": {"type": "number"},
                    "importEnergy": {"type": "number"},
                    "phaseId": {"type": "number"},
                    "current": {"type": "number"},
                }
            }
        },
        "voltages": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "voltage": {"type": "number"},
                    "phaseId": {"type": "number"}
                }
            }
        }
    }
}


def _external_to_internal(external_dict: dict) -> dict:
    """
    Transform incoming message to a format that the db can understand.
    :param external_dict: external message format
    :return: internal message format
    """
    result = dict(
        utc_timestamp=datetime.fromtimestamp(external_dict.get('utcTimeStamp') / 1000),
        total_power=external_dict.get('totalPower'),
        total_reactive_power=external_dict.get('totalReactivePower'),
        total_export_energy=external_dict.get('totalExportEnergy'),
        total_import_energy=external_dict.get('totalImportEnergy'),
        monitor_status=external_dict.get('monitorStatus'))

    # Channel Power
    for power in external_dict.get('channelPowers'):
        i = power.get('ctInput')
        result.update({
            'ct_input{}'.format(i): power.get('ctInput'),
            'power{}'.format(i): power.get('power'),
            'export_energy{}'.format(i): power.get('exportEnergy'),
            'import_energy{}'.format(i): power.get('importEnergy'),
            'phase_id{}'.format(i): power.get('phaseId'),
            'current{}'.format(i): power.get('current')})

    # Voltages
    for voltage in external_dict.get('voltages'):
        i = power.get('phaseId')
        result.update({
            'volt{}'.format(i): voltage.get('voltage'),
            'phase_id{}'.format(i): voltage.get('phaseId')})

    return result


def transform_smappee(message: dict) -> object:
    message_dict = json.loads(message.decode())
    validate(message_dict, validation)

    return Smappee(**_external_to_internal(message_dict))
