import io
from io import BytesIO
import cairosvg

import wand.image
from svgpathtools import svg2paths
from DisplayFramework import DeviceSpecification
class SVGRenderer:

    @staticmethod
    def GenerateCurrentDeviceScreen():
        pass
        # TODO FOR EACH MODULE
        # CALCULATE GRIDSPACE

    @staticmethod
    def SVGGetSize(_svg: str) -> [int, int]:
        img_io = io.BytesIO(_svg.encode(encoding="UTF-8"))
        paths, attributes = svg2paths(img_io)

        svg_size_w: int = 0
        svg_size_h: int = 0
        for a in attributes:
            if 'width' in a and 'height' in a:
                svg_size_w = int(a['width'])
                svg_size_h = int(a['height'])
                break
        return svg_size_w, svg_size_h

    @staticmethod
    def SVG2BMP(_svg: str, _device: DeviceSpecification.DeviceSpecification = None)-> BytesIO:

        png_bytes: BytesIO = SVGRenderer.SVG2PNG(_svg, _device)
        bmp_bytes = io.BytesIO()

        with wand.image.Image(file=png_bytes) as img:
            img.format = 'bmp'
            img.save(file=bmp_bytes)

        bmp_bytes.seek(0)  # Move to the beginning of the stream
        return bmp_bytes

    @staticmethod
    def SVG2PNG(_svg: str, _device: DeviceSpecification.DeviceSpecification = None) -> BytesIO:
        img_io = io.BytesIO(_svg.encode(encoding="UTF-8"))

        # APPLY SCALE
        scale_factor: float = 1.0

        # GET SVG SIZE
        paths, attributes = svg2paths(img_io)
        img_io.seek(0)

        svg_size_w: int = 0
        svg_size_h: int = 0
        for a in attributes:
            if 'width' in a and 'height' in a:
                svg_size_w = int(a['width'])
                svg_size_h = int(a['height'])
                break
        #
        if svg_size_w != _device.screen_size_w or svg_size_h != _device.screen_size_h:
            scale_factor = max([0.1, min([_device.screen_size_w / svg_size_w, _device.screen_size_h / svg_size_h])])

        # SET OUTPUT IMAGE SIZEc
        rt = io.BytesIO()
        cairosvg.svg2png(file_obj=img_io, write_to=rt, output_width=_device.screen_size_w, parent_height=_device.screen_size_h, scale=scale_factor)

        rt.seek(0)
        return rt






    def __init__(self):
        pass

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SVGRenderer, cls).__new__(cls)
            # Put any initialization here.
        return cls._instance
