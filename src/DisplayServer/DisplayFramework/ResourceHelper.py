import shutil
import bleach
import requests
import magic

from enum import Enum
from DisplayFramework import BaseTile



class ResourceHelper:

    @staticmethod
    def FetchContent(_url: str, _tile_name: str) -> str:
        '''
        Downloads a remote file into given resource folder
        :param _url: source url to download content from
        :param _tile_name:  prefix name
        :return: local downloaded filepath with an added extension if not present
        '''

        if len(_url) <= 0:
            raise  Exception("FetchContent: _url is empty")

        _url = bleach.clean(_url)
        _tile_name = _tile_name.replace(" ", "_").replace("/", "")
        local_url: str = _url
        # RENDERER NEEDS LOCAL FILES
        if _url.startswith("https://") or _url.startswith("http://"):
            local_url: str = _url.split('/')[-1]


            if _tile_name not in local_url:
                local_url = "{}_{}".format(_tile_name, local_url)

            # DANGEROUS :)
            if not local_url.startswith("/"):
                local_url = BaseTile.BaseTileSettings.RESOURCE_FOLDER + local_url

            # DOWNLOAD FILE
            response: requests.Response = requests.get(_url, stream=True)
            with open(local_url, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response

            # CHECK TYPE
            # TODO REWORK
            if "." not in local_url:
                detected_mimetype: str = magic.from_file(local_url, mime=True)
                # check for mimetype image/png and get the extention
                if "/" in detected_mimetype:
                    extention: str = detected_mimetype.split('/')[-1]
                    local_url_with_added_extention: str = "{}.{}".format(local_url, extention)
                    # MOVE FILE TO NEW LOCATION
                    shutil.move(local_url, local_url_with_added_extention)
                    # SAVE NEW URL
                    local_url = local_url_with_added_extention
        else:
            # DANGEROUS :)
            if _url.startswith("/"):
                local_url = _url
            else:
                local_url = BaseTile.BaseTileSettings.RESOURCE_FOLDER + _url

        return local_url