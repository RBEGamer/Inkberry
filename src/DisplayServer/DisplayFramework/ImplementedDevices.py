from enum import Enum
class ImplementedDevices(Enum):
    INVALID = 99,
    SIMULATED = 0,
    INKPLATE10 = 3,
    INKBERRY_75_LAMINATED_BW = 4,
    INKBERRY_75_RBW = 5,


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
