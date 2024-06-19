import sys
from types import ModuleType

from DisplayFramework import DeviceSpecification, TileSpecification
from importlib import import_module
from DisplayFramework import BaseTile

from DisplayFramework.tiles import *


class TileFactory:


    @staticmethod
    def GetTiles(_description: DeviceSpecification.DeviceSpecification) -> [BaseTile]:

        tiles: [] = []
        for e in _description.tile_specifications:
            e: TileSpecification.TileSpecification
            if e.module_name == "":
                raise ImportError("Module Name empty")


            module_path: str = "DisplayFramework"
            class_name: str = "BaseTile"
            module: ModuleType = None
            # IMPORT MODULE IF NEEDED
            if e.module_name not in sys.modules:
                if "." in e.module_name:
                    module_path, class_name = e.module_name.rsplit('.', 1)

            try:
                module = import_module(module_path)
            except (ImportError, AttributeError) as ex:
                raise ImportError(ex)

            # CREATE INSTANCE
            try:
                tile_class = getattr(module, class_name)
                tile_class_instance: BaseTile = tile_class(e)
                tiles.append(tile_class_instance)
            except Exception as exi:
                raise ImportError(exi)



        return tiles

