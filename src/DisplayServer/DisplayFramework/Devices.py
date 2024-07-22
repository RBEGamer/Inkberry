import os
import random
from enum import Enum
from pathlib import Path

import pysondb.db
import yaml
from pysondb import db

from DisplayFramework import ImplementedDevices, DeviceLookUpTable, DeviceSpecification, BaseTile





class Devices:
    _instance = None

    DATABASE_FILE_NAME: str = "devices.json"
    DATABSE_FILE_ABS_PATH: str = "./devices.json"
    @staticmethod
    def SetDatabaseFolder(_db_folder: str):
        if len(_db_folder) <= 0:
            return

        if not _db_folder.endswith(".json"):
            if not _db_folder.endswith("/"):
                _db_folder += "/"
            _db_folder += Devices.DATABASE_FILE_NAME

        Path(os.path.dirname(_db_folder)).mkdir(parents=True, exist_ok=True)

        Devices.DATABSE_FILE_ABS_PATH = _db_folder
        print("Devices.DATABSE_FILE_ABS_PATH = {}".format(Devices.DATABSE_FILE_ABS_PATH))

    @staticmethod
    def getDB() -> pysondb.db.JsonDatabase:
        return db.getDb(Devices.DATABSE_FILE_ABS_PATH)
    @staticmethod
    def CheckForUpdatedData(_id: str) -> bool:
        return True

    @staticmethod
    def GetDeviceRecord(_id: str) -> dict:
        try:
            if not Devices.CheckDeviceExists(_id):
                return {}
            return Devices.getDB().getBy({"device_id": _id})[0]
        except Exception as e:
            print(e)
            return {}


    @staticmethod
    def GetRegisteredDevicesOfHardwareType(_hardware_type: ImplementedDevices.ImplementedDevices, _device_id_to_exclude: str = None, _skip_devices_with_set_parent: bool = False) -> list:

        try:
            rt: list = []
            qr: list = Devices.getDB().getBy({"mark_deleted": False, "hardware": _hardware_type.value})
            if _device_id_to_exclude is None or len(_device_id_to_exclude) <= 0:
                for d in qr:

                    if _skip_devices_with_set_parent and (d["parent_id"] is not None):
                        if len(d["parent_id"]) > 0:
                            continue

                    rt.append({'id': d["device_id"], 'name': d["device_id"] + " @ " + d["allocation"]})
            else:
                for d in qr:
                    if _device_id_to_exclude == d["device_id"]:
                        continue

                    if _skip_devices_with_set_parent and (d["parent_id"] is not None):
                        if len(d["parent_id"]) > 0:
                            continue
                    rt.append({'id': d["device_id"], 'name': d["device_id"] + " @ " + d["allocation"]})
            return rt
        except Exception as e:
            print(e)
            return []
    @staticmethod
    def GetRegisteredDeviceIds(_include_only_not_deleted: bool = False, _include_only_enabled_devices: bool = False) -> list:
        try:
            rt: list = []
            qr: list = []
            if _include_only_not_deleted:
                qr = Devices.getDB().getBy({"mark_deleted": False})
            elif _include_only_enabled_devices:
                qr = Devices.getDB().getBy({"mark_deleted": False, "enabled": True})
            else:
                qr = Devices.getDB().getAll()

            for d in qr:
                rt.append({'id': d["device_id"], 'name': d["allocation"]})
            return rt
        except Exception as e:
            print(e)
            return []
    @staticmethod
    def GetRandomDeviceRecord() -> dict:
        k = random.choice(Devices.getDB().getBy({"mark_deleted": False}))
        if k is None or 'device_id' not in k or not Devices.CheckDeviceExists(k['device_id']):
            return {}
        return k

    @staticmethod
    def GetRandomDeviceSpecification() -> DeviceSpecification.DeviceSpecification:
        d: dict = Devices.GetRandomDeviceRecord()
        if d is not None and 'device_id' in d:
            return Devices.GetDeviceSpecification(d['device_id'])
        else:
            return None

    @staticmethod
    def GetDeviceSpecification(_id: str) -> DeviceSpecification.DeviceSpecification:
        d: DeviceSpecification.DeviceSpecification = DeviceSpecification.DeviceSpecification(Devices.GetDeviceRecord(_id))
        return d

    @staticmethod
    def DeleteDevice(_id: str):
        spec = Devices.GetDeviceSpecification(_id)
        if spec is not None:
            spec.mark_deleted = True
            spec.enabled = False
            spec.device_id = "__DELETED__" + spec.device_id
            Devices.UpdateDeviceSpecification(spec, _id)
            # TODO REWORK ADD DIRECT QUERY
            # DELETE PARENT DEVICE TOO
            for d in Devices.GetRegisteredDeviceIds():
                rec: DeviceSpecification.DeviceSpecification = Devices.GetDeviceSpecification(d)
                if rec.parent_id is not None:
                    if len(rec.parent_id) > 0:
                        spec.mark_deleted = True
                        spec.enabled = False
                        spec.device_id = "__DELETED__" + spec.device_id
                        Devices.UpdateDeviceSpecification(spec, _id)


    @staticmethod
    def CheckDeviceExists(_id: str) -> bool:
        if len(Devices.getDB().getBy({"device_id": _id})) > 0:
            return True
        return False

    @staticmethod
    def CheckDeviceEnabled(_id: str) -> bool:
        r: dict = Devices.GetDeviceRecord(_id)
        if 'enabled' in r:
            return bool(r.get('enabled'))
        return False

    @staticmethod
    def UpdateDeviceSpecification(spec: DeviceSpecification.DeviceSpecification, _alternative_device_id: str = None) -> bool:
        did: str = spec.device_id
        if _alternative_device_id is not None:
            did = _alternative_device_id

        if Devices.CheckDeviceExists(did):
            dr: dict = {}
            original_record = Devices.GetDeviceRecord(did)
            update_data = spec.to_dict()

            dr.update(original_record)

            dr.update(update_data)
            result = Devices.getDB().updateByQuery({"device_id": did}, dr)

            if result is None:
                return True

        return False
    @staticmethod
    def UpdateDeviceStatus(_id: str, _last_request: str, _dict: dict) -> bool:
        spec = Devices.GetDeviceSpecification(_id)
        spec.last_request = _last_request

        #spec.additional_information = _dict

        return Devices.UpdateDeviceSpecification(spec)



    @staticmethod
    def CreateDeviceFromName(_hardware_name: str, _id: str, _allocation: str = "undefined", _force: bool = False, _orientation: DeviceSpecification.DisplayOrientation = DeviceSpecification.DisplayOrientation.DP_HORIZONTAL) -> DeviceSpecification.DeviceSpecification:
        return Devices.CreateDevice(ImplementedDevices.ImplementedDevices.from_name(_hardware_name), _id, _allocation, _force)

    @staticmethod
    def CreateDevice(hardware_type: ImplementedDevices, _id: str, _allocation: str = "undefined", _force: bool = False, _orientation: DeviceSpecification.DisplayOrientation = DeviceSpecification.DisplayOrientation.DP_HORIZONTAL) -> DeviceSpecification.DeviceSpecification:

        if len(_id) <= 0:
            raise Exception("id is empty")

        if _force:
            # also removes duplicate entries
            ids: [] = Devices.getDB().getBy({"device_id": _id})
            for e in ids:
                id: int = e.get("id")
                if id:
                    Devices.getDB().deleteById(id)


        # CREATE DEVICE ENTRY
        device_definition: DeviceSpecification.DeviceSpecification = DeviceLookUpTable.DeviceLookUpTable.get_hardware_definition(hardware_type)
        device_definition.set_hardware_type(hardware_type)
        device_definition.device_id = _id
        device_definition.enabled = True
        device_definition.allocation = _allocation
        device_definition.display_orientation = _orientation


        device_definition_json: dict = device_definition.to_dict()
        try:
            # STORE IN DATABASE
            if not Devices.CheckDeviceExists(_id):
                Devices.getDB().add(device_definition_json)
            else:
                did: int = Devices.GetDeviceRecord(_id)['id']
                Devices.getDB().updateById(did, device_definition_json)
            return device_definition
        except Exception as e:
            print(e)
            return None
        return None










    def __init__(self):
        pass

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Devices, cls).__new__(cls)
            # Put any initialization here.
        return cls._instance

