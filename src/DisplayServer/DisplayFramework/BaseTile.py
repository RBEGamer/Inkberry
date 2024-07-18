import os
from abc import ABC, abstractmethod
from pathlib import Path

from DisplayFramework import TileSpecification
from DisplayFramework.pysvg import structure


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

    def __init__(self, _specification: TileSpecification.TileSpecification):
        self.spec = _specification

        # FILL DEFAULT PARAMETER IF KEYS NOT PRESNET
        for k in self.DEFAULT_PARAMETER['default']:
            if k not in self.spec.parameters:
                self.spec.parameters[k] = self.DEFAULT_PARAMETER['default'][k]



    def update_parameters(self, _parameter: dict):
        for k, v in _parameter.items():
            if k in self.spec.parameters:
                self.spec.parameters[k] = v


    def update(self):
        pass


    def render(self) -> structure.Svg:
        pass


    def get_parameter_types(self) -> dict:
        return self.DEFAULT_PARAMETER['types']


    def get_parameter_defaults(self) -> dict:
        return self.DEFAULT_PARAMETER['default']


    def get_parameter_current(self) -> dict:
        return self.spec.parameters