import base64
from io import BytesIO

import PIL.Image

from DisplayFramework import BaseTile, TileSpecification, ResourceHelper
from DisplayFramework.pysvg import structure, builders, text

import shutil
import requests
from PIL import Image


class ImageTile(BaseTile.BaseTile):

    DEFAULT_PARAMETER: dict = {
        "types": {
            "url": "str",
            "rotation": "int",
            "preserve_aspect_ratio": "bool",
            "image_rotation": "int",
            "scale_factor": "float"
        },"default":{
            "url": "",
            "rotation": "0",
            "preserve_aspect_ratio": 1,
            "image_rotation": 0,
            "scale_factor": 1.0
        }
    }



    def update_parameters(self, _parameter: dict):
        for k, v in _parameter.items():
            self.spec.parameters['k'] = v

    def update(self) -> bool:
       return False





    def get_parameter_types(self) -> dict:
        return self.DEFAULT_PARAMETER['types']

    def get_parameter_defaults(self) -> dict:
        return self.DEFAULT_PARAMETER['default']

    def get_parameter_current(self) -> dict:
        return self.spec.parameters

    @staticmethod
    def generate_image_container(_image: PIL.Image, _spec: TileSpecification.TileSpecification) -> structure.Svg:
        svg_document: structure.Svg = structure.Svg()
        svg_document.set_id(_spec.name)
        svg_document.set_x(_spec.position.pos_x)
        svg_document.set_y(_spec.position.pos_y)

        if int(_spec.parameters.get('rotation', 0)) > 0:
            svg_document.set_transform("rotate(-{})".format(_spec.parameters.get('rotation', 0)))


        image_rotation: int = int(_spec.parameters.get('image_rotation', 1)) % 360
        if image_rotation != 0:
            _image = _image.rotate(image_rotation, expand=True)

        # SCALE IMAGE
        width_org, height_org = _image.size
        scale_factor: float = abs(float(_spec.parameters.get('scale_factor', 1.0)))
        # CALCULATE NEW SVG BOX
        loaded_image = _image.resize((int(width_org * scale_factor), int(height_org * scale_factor)))
        # GET NEW IMAGE SIZE
        width, height = loaded_image.size

        # RESIZE SVG CONTAINER TO FIT IMAGE
        #if _spec.position.size_w <= 0 or _spec.position.size_w <= 0:
        #    _spec.position.size_w = width
        #    _spec.position.size_h = height

        svg_document.set_width(width)
        svg_document.set_height(height)

        # FINALLY CREATE IMAGE SVG ELEMENT
        preserve_aspect_ration: bool = True
        if not bool(int(_spec.parameters.get('preserve_aspect_ration', 1))):
            preserve_aspect_ration = False

        i = structure.Image('0%', '0%', width=width, height=height, preserveAspectRatio=preserve_aspect_ration)

        # LINK IMAGE DATA USING EMBEDDED BASE64 PNG STRING
        buffered = BytesIO()
        loaded_image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        img_data: str = "data:image/png;base64," + img_str
        i.set_xlink_href(img_data)

        # ADD CENTER STYLING
        # TODO NEEDED ?
        s: builders.StyleBuilder = builders.StyleBuilder({})
        s.setDisplayAlign("left")

        i.set_style(s.getStyle())

        svg_document.addElement(i)
        return svg_document

    def render(self) -> structure.Svg:

        # FETCH IMAGE RESOURCE
        image_path: str = ResourceHelper.ResourceHelper.FetchContent(self.spec.parameters.get('url', ''), self.spec.name)
        # CREATE IMAGE ELEMENT
        loaded_image = Image.open(image_path)

        return ImageTile.generate_image_container(loaded_image, self.spec)
