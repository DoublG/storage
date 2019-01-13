import unittest
from datetime import datetime
from unittest.mock import patch

from storage.format import transform_smappee


class TestValidateFormat(unittest.TestCase):

    def test_errors(self):

        with self.assertRaises(TypeError):
            result = transform_smappee("{}".encode('utf-8'))

        with self.assertRaises(ValueError):
            result = transform_smappee('{"utcTimeStamp": 1543156626563, channelPowers:[]}'.encode('utf-8'))

    @patch('storage.format.Smappee')
    def test_validate_message(self, mock_smappee):
        message = """
            {"totalPower": 653,
                   "totalReactivePower": 501,
                   "totalExportEnergy": 0,
                   "totalImportEnergy": 864146084,
                   "monitorStatus": 0,
                   "utcTimeStamp": 1543156626563,
                   "channelPowers": [
                       {"ctInput": 0, "power": 101, "exportEnergy": 0, "importEnergy": 220879977, "phaseId": 0,
                        "current": 5},
                       {"ctInput": 1, "power": 184, "exportEnergy": 0, "importEnergy": 307981528, "phaseId": 1,
                        "current": 12},
                       {"ctInput": 2, "power": 368, "exportEnergy": 0, "importEnergy": 335286286, "phaseId": 2,
                        "current": 18},
                       {"ctInput": 3, "power": 0, "exportEnergy": 0, "importEnergy": 898, "phaseId": 0, "current": 0},
                       {"ctInput": 4, "power": 0, "exportEnergy": 17727, "importEnergy": 13940069, "phaseId": 1,
                        "current": 1},
                       {"ctInput": 5, "power": 69, "exportEnergy": 2068841, "importEnergy": 245618083, "phaseId": 2,
                        "current": 10}],
                   "voltages": [{"voltage": 236, "phaseId": 0}]} """.encode('utf-8')

        result = transform_smappee(message)

        mock_smappee.assert_called_once_with(
            ct_input0=0, ct_input1=1, ct_input2=2, ct_input3=3, ct_input4=4, ct_input5=5, current0=5, current1=12,
            current2=18, current3=0, current4=1, current5=10, export_energy0=0, export_energy1=0, export_energy2=0,
            export_energy3=0, export_energy4=17727, export_energy5=2068841, import_energy0=220879977,
            import_energy1=307981528, import_energy2=335286286, import_energy3=898, import_energy4=13940069,
            import_energy5=245618083, monitor_status=0, phase_id0=0, phase_id1=1, phase_id2=0, phase_id3=0, phase_id4=1,
            phase_id5=2, power0=101, power1=184, power2=368, power3=0, power4=0, power5=69, total_export_energy=0,
            total_import_energy=864146084, total_power=653, total_reactive_power=501,
            utc_timestamp=datetime(2018, 11, 25, 15, 37, 6, 563000), volt2=236
        )
