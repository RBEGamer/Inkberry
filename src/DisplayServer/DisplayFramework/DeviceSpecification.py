from DisplayFramework import ImplementedDevices, TileSpecification
from enum import  Enum

class DisplayOrientation(Enum):
    DP_HORIZONTAL = 0
    DP_VERTICAL = 1

    @staticmethod
    def from_int(_val: int):
        try:
            return DisplayOrientation(_val)
        except:
            return DisplayOrientation.DP_HORIZONTAL


class DeviceSpecification:

    hardware: int  = ImplementedDevices.ImplementedDevices.SIMULATED.value
    device_id: str = ""
    enabled: bool = False
    allocation: str = "undefined"
    last_request: str = ""
    screen_size_w: int = 1200
    screen_size_h: int = 825
    wakeup_interval: int = 10
    content_scale: float = 1.0
    display_orientation: DisplayOrientation = DisplayOrientation.DP_HORIZONTAL
    tile_specifications: [TileSpecification.TileSpecification] = []
    _valid: bool = True

    def __dict__(self) -> dict:

        sp: [] = []
        for e in self.tile_specifications:
            sp.append(e.to_dict())

        return {
            'hardware': self.hardware,
            'device_id': self.device_id,
            'enabled': self.enabled,
            'allocation': self.allocation,
            'last_request': self.last_request,
            'screen_size_w': self.screen_size_w,
            'screen_size_h': self.screen_size_h,
            'wakeup_interval': self.wakeup_interval,
            'display_orientation': self.display_orientation.value,
            'tile_specifications': sp,
            'content_scale': self.content_scale
        }

    def get_hardware_type(self) -> ImplementedDevices.ImplementedDevices:
         return ImplementedDevices.ImplementedDevices.from_int(self.hardware)
    def set_hardware_type(self, value: ImplementedDevices.ImplementedDevices):
        self.hardware = value.value
    def is_valid(self) -> bool:
        return self._valid

    def to_dict(self) -> dict:
        return self.__dict__()

    def from_dict(self, _dict: dict):
        errors = 0
        if 'hardware' in _dict:
            self.hardware = ImplementedDevices.ImplementedDevices.from_int(_dict['hardware']).value
            errors = errors + 1
        if 'device_id' in _dict:
            self.device_id = _dict['device_id']
            errors = errors + 1
        if 'enabled' in _dict:
            self.enabled = bool(_dict['enabled'])
            errors = errors + 1
        if 'allocation' in _dict:
            self.allocation = _dict['allocation']
            errors = errors + 1
        if 'last_request' in _dict:
            self.last_request = _dict['last_request']
            errors = errors + 1
        if 'screen_size_w' in _dict:
            self.screen_size_w = int(_dict['screen_size_w'])
            errors = errors + 1
        if 'screen_size_h' in _dict:
            self.screen_size_h = int(_dict['screen_size_h'])
            errors = errors + 1
        if 'wakeup_interval' in _dict:
            self.wakeup_interval = int(_dict['wakeup_interval'])
            errors = errors + 1
        if 'display_orientation' in _dict:
            self.display_orientation = DisplayOrientation.from_int(_dict['display_orientation'])
            errors = errors + 1
        if 'content_scale' in _dict:
            self.content_scale = float(_dict['content_scale'])
            errors = errors + 1
        if 'tile_specifications' in _dict:
            self.tile_specifications = []
            for e in _dict['tile_specifications']:
                 self.tile_specifications.append(TileSpecification.TileSpecification(e))
            errors = errors + 1
        if errors > 0:
            self._valid = True





    def __init__(self, _load_from_dict: dict = None):
        if _load_from_dict is not None:
            self.from_dict(_load_from_dict)