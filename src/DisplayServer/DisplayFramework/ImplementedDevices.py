from enum import Enum, IntEnum
class ImplementedDevices(IntEnum):
    INVALID = 99,
    MINIMAL = 0,
    SIMULATED = 1,
    INKPLATE10 = 3,
    INKBERRY_75_LAMINATED_BW = 4,
    INKBERRY_75_RBW = 5,
    INKBERRY_73_7COLOR = 6


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
