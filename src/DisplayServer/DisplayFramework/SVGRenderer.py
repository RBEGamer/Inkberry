import io
from io import BytesIO
import cairosvg

import wand.image
from svgpathtools import svg2paths
from svgwrite import Drawing
from wand.color import Color
from wand.drawing import Drawing
from wand.display import display
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
    def test() -> BytesIO:
        width = 800
        height = 480
        dpi = 75

        with wand.image.Image(width=width, height=height, background=wand.color.Color('white')) as img:
            # Set the DPI of the image
            img.compression = 'no'  # This ensures no compression
            img.resolution = (dpi, dpi)

            # Draw something on the image
            with wand.drawing.Drawing() as draw:
                draw.fill_color = Color('black')
                draw.circle((400, 240), (400, 340))  # Draw a black circle in the center
                draw(img)

            # Convert the image to grayscale and reduce depth to 4-bit (16 colors)
            #img.type = 'grayscale'
            #img.depth = 4
            #img.channel_depths = 4
            #img.channel_images = 1

            # Apply dithering and quantize to 16 colors (4-bit)
            #img.dither = True
            #img.quantize(number_colors=16, dither_method='FloydSteinberg')

            # Ensure the image is saved in BMP format

            img.format = 'bmp'


            # Save the image as BMP
            return_bytes = io.BytesIO()
            img.save(file=return_bytes)
            return_bytes.seek(0)

            return return_bytes
    @staticmethod
    def SVG2Image(_svg: str, _device: DeviceSpecification.DeviceSpecification, _export_type: SVG_ExportTypes) -> BytesIO:
        img_io = io.BytesIO(_svg.encode(encoding="UTF-8"))

        scale_factor = SVGRenderer.calculateNeededSVGScaleFactorForImageConversion(_svg, _device)
        # SET OUTPUT IMAGE SIZEc



        if _export_type == SVG_ExportTypes.BMP:


            return_bytes = io.BytesIO()
            png_bytes = io.BytesIO()
            cairosvg.svg2png(file_obj=img_io, write_to=png_bytes, output_width=_device.screen_size_w, parent_height=_device.screen_size_h, scale=scale_factor)
            png_bytes.seek(0)
            # CONVERT PNG TO BMP
            return_bytes = io.BytesIO()
            with wand.image.Image(file=png_bytes,) as img:
                img.resolution = (75, 75)
                # Apply dithering
                img.antialias = False

                if _device.image_filter == DeviceSpecification.DisplayImageFilters.DIF_DITHER:
                    img.dither = True
                else:
                    img.dither = False


                # Convert the image to 4-bit depth
                img.depth = 4
                num_colors = None


                if _device.colorspace == DeviceSpecification.DisplaySupportedColors.DSC_BW or _device.colorspace == DeviceSpecification.DisplaySupportedColors.DSC_BWR:
                    img.type = 'palette'

                # Create a custom colormap with only black and white
                if _device.colorspace == DeviceSpecification.DisplaySupportedColors.DSC_BW:
                    num_colors = 2
                    img.type = 'palette'
                    img.color_map(0, wand.color.Color('#000000'))
                    img.color_map(1, wand.color.Color('#FFFFFF'))
                elif _device.colorspace == DeviceSpecification.DisplaySupportedColors.DSC_BWR:
                    num_colors = 3
                    img.type = 'palette'
                    img.color_map(0, wand.color.Color('#000000'))
                    img.color_map(1, wand.color.Color('#FFFFFF'))
                    img.color_map(2, Color('#FF0000'))

                if _device.colorspace == DeviceSpecification.DisplaySupportedColors.DSC_BW or _device.colorspace == DeviceSpecification.DisplaySupportedColors.DSC_BWR:
                    
                    img.transform_colorspace('gray')
                    img.quantize(number_colors=num_colors, colorspace_type='gray', dither=img.dither)
                elif _device.colorspace == DeviceSpecification.DisplaySupportedColors.DSC_COLOR:
                    img.transform_colorspace('rgb', dither=img.dither)
                else:
                    raise Exception("Unsupported color space")




                img.format = 'bmp'
                img.compression = 'no'  # This ensures no compression

                img.save(filename='t.bmp')
                img.save(file=return_bytes)

            return_bytes.seek(0)
            return return_bytes
        elif _export_type == SVG_ExportTypes.PNG:
            return_bytes = io.BytesIO()
            cairosvg.svg2png(file_obj=img_io, write_to=return_bytes, output_width=_device.screen_size_w, parent_height=_device.screen_size_h, scale=scale_factor)
            return_bytes.seek(0)
            return return_bytes
        elif _export_type == SVG_ExportTypes.PDF:
            return_bytes = io.BytesIO()
            cairosvg.svg2pdf(file_obj=img_io, write_to=return_bytes, output_width=_device.screen_size_w, parent_height=_device.screen_size_h, scale=scale_factor)
            return_bytes.seek(0)
            return return_bytes
        elif _export_type == SVG_ExportTypes.SVG:
            return_bytes = io.BytesIO()
            cairosvg.svg2svg(file_obj=img_io, write_to=return_bytes, output_width=_device.screen_size_w, parent_height=_device.screen_size_h, scale=scale_factor)
            return_bytes.seek(0)
            return return_bytes
        elif _export_type == SVG_ExportTypes.PS:
            return_bytes = io.BytesIO()
            cairosvg.svg2ps(file_obj=img_io, write_to=return_bytes, output_width=_device.screen_size_w, parent_height=_device.screen_size_h, scale=scale_factor)
            return_bytes.seek(0)
            return return_bytes
        elif _export_type == SVG_ExportTypes.EPS:
            return_bytes = io.BytesIO()
            cairosvg.svg2eps(file_obj=img_io, write_to=return_bytes, output_width=_device.screen_size_w, parent_height=_device.screen_size_h, scale=scale_factor)
            return_bytes.seek(0)
            return return_bytes
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
