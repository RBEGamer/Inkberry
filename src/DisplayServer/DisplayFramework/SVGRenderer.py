import io
from io import BytesIO
import cairosvg

import wand.image
from svgpathtools import svg2paths
from DisplayFramework import DeviceSpecification

from enum import Enum

class SVG_ExportTypes(Enum):
    BMP = 1,
    PNG = 2,
    PDF = 3,
    SVG = 4,
    PS = 5,
    EPS = 6,


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
    def calculateNeededSVGScaleFactorForImageConversion(_svg: str, _device: DeviceSpecification.DeviceSpecification = None) -> float:
        scale_factor: float = 1.0

        svg_size_w, svg_size_h = SVGRenderer.SVGGetSize(_svg)

        if svg_size_w != _device.screen_size_w or svg_size_h != _device.screen_size_h:
            scale_factor = max([0.1, min([_device.screen_size_w / svg_size_w, _device.screen_size_h / svg_size_h])])

        return scale_factor


    @staticmethod
    def SVG2Image(_svg: str, _device: DeviceSpecification.DeviceSpecification, _export_type: SVG_ExportTypes) -> BytesIO:
        img_io = io.BytesIO(_svg.encode(encoding="UTF-8"))

        scale_factor = SVGRenderer.calculateNeededSVGScaleFactorForImageConversion(_svg, _device)
        # SET OUTPUT IMAGE SIZEc
        rt = io.BytesIO()


        if _export_type == SVG_ExportTypes.BMP:
            cairosvg.svg2png(file_obj=img_io, write_to=rt, output_width=_device.screen_size_w, parent_height=_device.screen_size_h, scale=scale_factor)
            rt.seek(0)
            # CONVERT PNG TO BMP
            with wand.image.Image(file=rt) as img:
                img.format = 'bmp'
                img.save(file=rt)

        elif _export_type == SVG_ExportTypes.PNG:
            cairosvg.svg2png(file_obj=img_io, write_to=rt, output_width=_device.screen_size_w, parent_height=_device.screen_size_h, scale=scale_factor)
        elif _export_type == SVG_ExportTypes.PDF:
            cairosvg.svg2pdf(file_obj=img_io, write_to=rt, output_width=_device.screen_size_w, parent_height=_device.screen_size_h, scale=scale_factor)
        elif _export_type == SVG_ExportTypes.SVG:
            cairosvg.svg2svg(file_obj=img_io, write_to=rt, output_width=_device.screen_size_w, parent_height=_device.screen_size_h, scale=scale_factor)
        elif _export_type == SVG_ExportTypes.PS:
            cairosvg.svg2ps(file_obj=img_io, write_to=rt, output_width=_device.screen_size_w, parent_height=_device.screen_size_h, scale=scale_factor)
        elif _export_type == SVG_ExportTypes.EPS:
            cairosvg.svg2eps(file_obj=img_io, write_to=rt, output_width=_device.screen_size_w, parent_height=_device.screen_size_h, scale=scale_factor)
        else:
            raise Exception("SVG export type not supported")

        rt.seek(0)
        return rt



    def __init__(self):
        pass

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SVGRenderer, cls).__new__(cls)
            # Put any initialization here.
        return cls._instance
