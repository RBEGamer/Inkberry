import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from DisplayFramework import TileSpecification, SVGHelper, Helper, DeviceSpecification
from DisplayFramework.pysvg import structure

class TileParameterTypes:
    STRING: str = "str"
    INTEGER: str = "int"
    FLOAT: str = "float"
    BOOL: str = "bool"


class BaseTileSettings:
    _instance = None

    RESOURCE_FOLDER = "./"
    def __init__(self):
        pass

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BaseTileSettings, cls).__new__(cls)
            # Put any initialization here.
        return cls._instance

    @staticmethod
    def SetResourceFolder(_folder: str):
        if len(_folder) <= 0:
            return


        if not _folder.endswith("/"):
            _folder += "/"

        Path(os.path.dirname(_folder)).mkdir(parents=True, exist_ok=True)
        BaseTileSettings.RESOURCE_FOLDER = _folder

        print("BaseTileSettings.RESOURCE_FOLDER = {}".format(BaseTileSettings.RESOURCE_FOLDER))

class BaseTile:

    DEFAULT_PARAMETER: dict = {
        "types": {},
        "default": {}
    }

    spec: TileSpecification.TileSpecification = TileSpecification.TileSpecification()
    hardware_spec: DeviceSpecification.DeviceSpecification = DeviceSpecification.DeviceSpecification()
    def tile_init(self):
        self.spec = self.prepare_spec_parameters(self.spec)

    def prepare_spec_parameters(self, _specification: TileSpecification.TileSpecification) -> TileSpecification.TileSpecification:
        # FILL DEFAULT PARAMETER IF KEYS NOT PRESNET
        for k in self.DEFAULT_PARAMETER['default']:
            if k not in _specification.parameters:
                t = self.DEFAULT_PARAMETER['default'][k]
                _specification.parameters[k] = t
        # TODO MOVE TO TILESPECIFICATION
        # SANITIZE PARAMETERS
        for k in _specification.parameters:
            user_parameter: str = str(_specification.parameters[k])
            user_parameter = self.replace_hardware_information_in_user_string(user_parameter)

            _specification.parameters[k] = SVGHelper.SVGHelper.sanitize_svg_input(user_parameter)
        return _specification

    def replace_hardware_information_in_user_string(self, _usertext: str):

        _usertext = _usertext.replace("%%allocation%%", "{}".format(self.hardware_spec.allocation))
        _usertext = _usertext.replace("%%deviceid%%", "{}".format(self.hardware_spec.device_id))

        return _usertext

    def __init__(self, _hardware: DeviceSpecification.DeviceSpecification, _specification: TileSpecification.TileSpecification):
        self.spec = _specification
        self.hardware_spec = _hardware
        self.tile_init()



    def update_parameters(self, _parameter: dict):
        for k, v in _parameter.items():
            if k in self.spec.parameters:
                self.spec.parameters[k] = v

        self.spec = self.prepare_spec_parameters(self.spec)

    def update(self) -> bool:
        return False


    def render(self) -> structure.Svg:
        pass


    def get_parameter_types(self) -> dict:
        return self.DEFAULT_PARAMETER['types']


    def get_parameter_defaults(self) -> dict:
        return self.DEFAULT_PARAMETER['default']


    def get_parameter_current(self) -> dict:
        return self.spec.parameters

    def get_spec_parameters(self, _key: str, _default: Any = None) -> Any:


        if _default is None:
            if _key in self.DEFAULT_PARAMETER["default"]:
                _default = self.DEFAULT_PARAMETER["default"]
            else:
                _default = ""

        if _key in self.spec.parameters:
            s_value: Any = self.spec.parameters.get(_key, "")

            if not s_value or s_value == "":
                return _default

            if _key in self.get_parameter_types():
                s_type: str = self.get_parameter_types().get(_key, "")

                if s_type == TileParameterTypes.STRING:
                    return str(s_value)
                elif s_type == TileParameterTypes.INTEGER:
                    return int(s_value)
                elif s_type == TileParameterTypes.FLOAT:
                    return float(s_value)
                elif s_type == TileParameterTypes.BOOL:
                    return Helper.Helper.parse_to_bool(str(s_value))
            return self.spec.parameters[_key]
        return _default