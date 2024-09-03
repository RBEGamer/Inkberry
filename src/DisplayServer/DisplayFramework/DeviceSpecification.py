from DisplayFramework import ImplementedDevices, TileSpecification, DeviceLookUpTable, SVGHelper
from enum import IntEnum

class DisplayOrientation(IntEnum):
    DP_HORIZONTAL = 0,
    DP_VERTICAL = 1

    @staticmethod
    def from_int(_val: int):
        try:
            return DisplayOrientation(_val)
        except:
            return DisplayOrientation.DP_HORIZONTAL
class DisplaySupportedColors(IntEnum):
    DSC_BW = 0,
    DSC_BWR = 1,
    DSC_GRAY = 2,
    DSC_COLOR = 3,
    DSC_7COLOR = 4

    @staticmethod
    def from_int(_val: int):
        try:
            return DisplaySupportedColors(_val)
        except:
            return DisplaySupportedColors.DSC_BW

class DisplayImageFilters(IntEnum):
    DIF_NONE = 0,
    DIF_DITHER = 1

    @staticmethod
    def from_int(_val: int):
        try:
            return DisplayImageFilters(_val)
        except:
            return DisplayImageFilters.DIF_NONE
class DeviceSpecification:

    hardware: ImplementedDevices.ImplementedDevices = ImplementedDevices.ImplementedDevices.MINIMAL
    colorspace: DisplaySupportedColors = DisplaySupportedColors.DSC_COLOR
    image_filter: DisplayImageFilters = DisplayImageFilters.DIF_NONE
    device_id: str = ""
    enabled: bool = False
    auth_token: str = ""
    allocation: str = "undefined"
    last_request: str = ""
    screen_size_w: int = 1200
    screen_size_h: int = 825
    wakeup_interval: int = 10
    content_scale: float = 1.0
    display_orientation: DisplayOrientation = DisplayOrientation.DP_HORIZONTAL
    tile_specifications: [TileSpecification.TileSpecification] = []
    current_content_hash: str = ""
    last_served_content_hash: str = ""
    current_content_svg: str = ""
    mark_deleted: bool = False
    parent_id: str = None
    _valid: bool = True


    def __dict__(self) -> dict:

        sp: [] = []
        for e in self.tile_specifications:
            sp.append(e.to_dict())

        return {
            'hardware': self.hardware.value,
            'device_id': self.device_id,
            'enabled': self.enabled,
            'allocation': self.allocation,
            'last_request': self.last_request,
            'screen_size_w': self.screen_size_w,
            'screen_size_h': self.screen_size_h,
            'wakeup_interval': self.wakeup_interval,
            'display_orientation': self.display_orientation.value,
            'tile_specifications': sp,
            'content_scale': self.content_scale,
            'auth_token': self.auth_token,
            'colorspace': self.colorspace.value,
            'image_filter': self.image_filter.value,
            'current_content_hash': self.current_content_hash,
            'last_served_content_hash': self.last_served_content_hash,
            'current_content_svg': self.current_content_svg,
            'mark_deleted': self.mark_deleted,
            'parent_id': self.parent_id
        }

    def get_hardware_type(self) -> ImplementedDevices.ImplementedDevices:
        return self.hardware
    def set_hardware_type(self, value: ImplementedDevices.ImplementedDevices):
        self.hardware = value
    def is_valid(self) -> bool:
        return self._valid

    def to_dict(self) -> dict:
        return self.__dict__()

    def from_dict(self, _dict: dict):
        errors = 0
        if 'hardware' in _dict:
            self.hardware = ImplementedDevices.ImplementedDevices.from_int(_dict['hardware'])
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
        if 'auth_token' in _dict:
            self.auth_token = _dict['auth_token']
            errors = errors + 1
        if 'content_scale' in _dict:
            self.content_scale = float(_dict['content_scale'])
            errors = errors + 1
        if 'tile_specifications' in _dict:
            self.tile_specifications = []
            for e in _dict['tile_specifications']:
                self.tile_specifications.append(TileSpecification.TileSpecification(e))
            errors = errors + 1
        if 'colorspace' in _dict:
            self.colorspace = DisplaySupportedColors.from_int(_dict['colorspace'])
        if 'image_filter' in _dict:
            self.image_filter = DisplayImageFilters.from_int(_dict['image_filter'])
        if 'current_content_hash' in _dict:
            self.current_content_hash = _dict['current_content_hash']
        if 'last_served_content_hash' in _dict:
            self.last_served_content_hash = _dict['last_served_content_hash']
        if 'current_content_svg' in _dict:
            self.current_content_svg = _dict['current_content_svg']
        if 'mark_deleted' in _dict:
            self.enabled = bool(_dict['mark_deleted'])
        if 'parent_id' in _dict:
            self.parent_id = _dict['parent_id']




        if errors > 0:
            self._valid = True


    def __init__(self, _load_from_dict: dict = None):
        if _load_from_dict is not None:
            self.from_dict(_load_from_dict)
        else:
            default_device: ImplementedDevices = ImplementedDevices.ImplementedDevices.MINIMAL
            DeviceLookUpTable.DeviceLookUpTable.get_hardware_definition(default_device, self)
