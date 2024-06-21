from DisplayFramework import ImplementedDevices

class DeviceLookUpTable(object):
    # TODO REWORK TO FILE BASED TEMPLATES
    @staticmethod
    def get_hardware_definition(_hardware_type: ImplementedDevices) -> dict:
        res: dict = {
            'screen_size_w': 0,
            'screen_size_h': 0,
            'wakeup_interval': -1
        }

        if _hardware_type == ImplementedDevices.ImplementedDevices.SIMULATED:
            res.update({})
        elif _hardware_type == ImplementedDevices.ImplementedDevices.ARDUINO_INKPLATE10 or _hardware_type == ImplementedDevices.ImplementedDevices.ARDUINO_INKPLATE10V2:
            res.update({'screen_size_w': 1200, 'screen_size_h': 825, 'wakeup_interval':10})
        elif _hardware_type == ImplementedDevices.ImplementedDevices.ARDUINO_INKPLATE6:
            res.update({'screen_size_w': 800, 'screen_size_h': 600, 'wakeup_interval':10})
        elif _hardware_type == ImplementedDevices.ImplementedDevices.ARDUINO_ESP32_7_5_INCH:
            res.update({'screen_size_w': 800, 'screen_size_h': 480, 'wakeup_interval': 1})



        return res

    @staticmethod
    def get_screen_size_w(_hardware_type: ImplementedDevices) -> int:
        return DeviceLookUpTable.get_hardware_definition(_hardware_type)['screen_size_w']

    @staticmethod
    def get_screen_size_h(_hardware_type: ImplementedDevices) -> int:
        return DeviceLookUpTable.get_hardware_definition(_hardware_type)['screen_size_h']
