from enum import Enum
class ImplementedDevices(Enum):
    INVALID = 99,
    SIMULATED = 0,
    ARDUINO_INKPLATE10 = 1,
    ARDUINO_INKPLATE10V2 = 2,
    ARDUINO_INKPLATE6 = 3,
    ARDUINO_ESP32_7_5_INCH = 4  # https://www.waveshare.com/7.5inch-e-paper-hat.htm


    @classmethod
    def from_name(cls, _name: str) -> Enum:
        _name = _name.lower().replace("_","")

        for s in ImplementedDevices:
            if _name in str(s.name).lower().replace("_",""):
                return s
        return ImplementedDevices.SIMULATED

    @staticmethod
    def from_int(_val: int):
        try:
            return ImplementedDevices(_val)
        except:
            return ImplementedDevices.INVALID
