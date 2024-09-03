import base64
from io import BytesIO

import PIL.Image

from DisplayFramework import BaseTile, TileSpecification, ResourceHelper, DeviceSpecification
from DisplayFramework.pysvg import structure, builders, text

import shutil
import requests
from PIL import Image


class ImageTile(BaseTile.BaseTile):

    DEFAULT_PARAMETER: dict = {
        "types": {
            "url": BaseTile.TileParameterTypes.STRING,
            "rotation": BaseTile.TileParameterTypes.INTEGER,
            "preserve_aspect_ratio": BaseTile.TileParameterTypes.BOOL,
            "image_rotation": BaseTile.TileParameterTypes.INTEGER,
            "scale_factor": BaseTile.TileParameterTypes.FLOAT
        }, "default": {
            "url": "",
            "rotation": 0,
            "preserve_aspect_ratio": 1,
            "image_rotation": 0,
            "scale_factor": 1.0
        }
    }


    def __init__(self, _hardware: DeviceSpecification.DeviceSpecification, _specification: TileSpecification.TileSpecification):
        super().__init__(_hardware, _specification)

    def update(self) -> bool:
       return False




    @staticmethod
    def generate_image_container(_image: PIL.Image, _spec: TileSpecification.TileSpecification,  _rotation: int = 0, _image_rotation: int = 0, _scale_factor: float = 1.0, _preserve_aspect_ratio: bool = True) -> structure.Svg:



        svg_document: structure.Svg = structure.Svg()
        svg_document.set_id(_spec.name)
        svg_document.set_x(_spec.position.pos_x)
        svg_document.set_y(_spec.position.pos_y)

        if _rotation > 0:
            svg_document.set_transform("rotate(-{})".format(_rotation))


        if _image_rotation != 0:
            _image = _image.rotate(_image_rotation, expand=True)

        # SCALE IMAGE
        width_org, height_org = _image.size

        # CALCULATE NEW SVG BOX
        loaded_image = _image.resize((int(width_org * _scale_factor), int(height_org * _scale_factor)))
        # GET NEW IMAGE SIZE
        width, height = loaded_image.size

        # RESIZE SVG CONTAINER TO FIT IMAGE
        #if _spec.position.size_w <= 0 or _spec.position.size_w <= 0:
        #    _spec.position.size_w = width
        #    _spec.position.size_h = height

        svg_document.set_width(width)
        svg_document.set_height(height)

        # FINALLY CREATE IMAGE SVG ELEMENT
        i = structure.Image('0%', '0%', width=width, height=height, preserveAspectRatio=_preserve_aspect_ratio)

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

        url: str = self.get_spec_parameters('url')
        rotation: int = self.get_spec_parameters('rotation',)
        image_rotation: int = self.get_spec_parameters('image_rotation') % 360
        scale_factor: float = abs(self.get_spec_parameters('scale_factor'))
        preserve_aspect_ratio: bool = self.get_spec_parameters('preserve_aspect_ratio')
        # FETCH IMAGE RESOURCE
        image_path: str = ResourceHelper.ResourceHelper.FetchContent(url, self.spec.name)
        # CREATE IMAGE ELEMENT
        loaded_image = Image.open(image_path)

        return ImageTile.generate_image_container(loaded_image, self.spec, rotation, image_rotation, scale_factor, preserve_aspect_ratio)
