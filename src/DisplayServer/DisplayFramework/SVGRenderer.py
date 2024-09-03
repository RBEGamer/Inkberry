import io
import math
import traceback
from io import BytesIO
import cairosvg
from PIL import Image
import wand.image
from svgpathtools import svg2paths
from svgwrite import Drawing
from wand.color import Color
from wand.drawing import Drawing
from wand.display import display

from DisplayFramework import DeviceSpecification, SVGHelper

from enum import Enum




class SVG_ExportTypes(Enum):
    BMP = 1,
    PNG = 2,
    PDF = 3,
    SVG = 4,
    PS = 5,
    EPS = 6,
    JPG = 7,
    CalEPD = 8,


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
        try:
            svg_size_w, svg_size_h = SVGRenderer.SVGGetSize(_svg)
        except Exception as e:
            print("".join(traceback.format_exception_only(type(e), e)))
            return scale_factor

        if svg_size_w != _device.screen_size_w or svg_size_h != _device.screen_size_h:
            scale_factor = max([0.1, min([_device.screen_size_w / svg_size_w, _device.screen_size_h / svg_size_h])])

        return scale_factor




    @staticmethod
    def SVG2Image(_svg: str, _device: DeviceSpecification.DeviceSpecification, _export_type: SVG_ExportTypes) -> BytesIO:
        img_io = io.BytesIO(_svg.encode(encoding="UTF-8"))

        scale_factor = SVGRenderer.calculateNeededSVGScaleFactorForImageConversion(_svg, _device)
        # CONVERT THE SVG TO THE TARGET IMAGE TYPE
        if _export_type == SVG_ExportTypes.BMP or _export_type == SVG_ExportTypes.CalEPD:

            png_bytes = io.BytesIO()
            cairosvg.svg2png(file_obj=img_io, write_to=png_bytes, output_width=_device.screen_size_w, parent_height=_device.screen_size_h, scale=scale_factor)
            png_bytes.seek(0)
            # CONVERT PNG TO BMP
            return_bytes = io.BytesIO()
            with wand.image.Image(file=png_bytes,) as img:
                img.resolution = (72, 72)
                # Apply dithering
                img.antialias = False

                if _device.image_filter == DeviceSpecification.DisplayImageFilters.DIF_DITHER:
                    img.dither = True
                else:
                    img.dither = False

                # Convert the image to 4-bit depth
                img.depth = 4
                num_colors = None
                max_colors: int = img.colors

                # Create a custom colormap with only black and white
                if _device.colorspace == DeviceSpecification.DisplaySupportedColors.DSC_BW:
                    num_colors = min([2, max_colors]) # BLACK WHITE
                    img.depth = 4
                    img.type = 'palette'
                    img.color_map(0, wand.color.Color('#000000'))
                    img.color_map(1, wand.color.Color('#FFFFFF'))
                elif _device.colorspace == DeviceSpecification.DisplaySupportedColors.DSC_BWR:
                    # FOR RED BLACK WHITE, A ADDITIONAL COLOR PALETTE IS GENERATED FOR RED AND GRAY COLORS
                    num_colors = min([2*2, max_colors]) # 2 GRAY STEPS FOR BLACK AND RED TO WHITE
                    img.depth = 8
                    img.type = 'palette'
                    palette_index = 0

                    if num_colors > 2:
                        # ADD GRAY SHADED TO COLOR PALETTE
                        gray_steps: [str] = SVGHelper.SVGHelper.generate_gray_shades(math.floor(num_colors / 2))
                        for idx, red_step in enumerate(gray_steps):
                            img.color_map(idx, wand.color.Color(red_step))
                        palette_index = palette_index + len(gray_steps)

                        # ADD RED SHADES TO COLOR PALETTE
                        red_steps: [str] = SVGHelper.SVGHelper.generate_red_shades(math.floor(num_colors/2))
                        for idx, red_step in enumerate(red_steps):
                            img.color_map(idx+palette_index, wand.color.Color(red_step))
                    else:
                        img.color_map(0, wand.color.Color('#000000'))
                        img.color_map(1, wand.color.Color('#FFFFFF'))
                elif _device.colorspace == DeviceSpecification.DisplaySupportedColors.DSC_GRAY:
                    # FOR GRAY, A ADDITIONAL COLOR PALETTE IS GENERATED GRAY COLORS
                    num_colors = min([16, max_colors])
                    img.depth = 8
                    img.type = 'palette'
                    palette_index = 0

                    gray_steps: [str] = SVGHelper.SVGHelper.generate_gray_shades(math.floor(num_colors))
                    for idx, red_step in enumerate(gray_steps):
                        img.color_map(idx + palette_index, wand.color.Color(red_step))
                   

                elif _device.colorspace == DeviceSpecification.DisplaySupportedColors.DSC_7COLOR:
                    # FOR 7 COLOR DIPLAYS
                    num_colors = 2 # generate_seven_colors_colorpalette generates 7 colors so 16 shades of each color
                    img.depth = 8
                    img.type = 'palette'

                    color_palette = SVGHelper.SVGHelper.generate_seven_colors_colorpalette(num_colors)
                    for idx, hexcolor in enumerate(color_palette):
                        if idx > max_colors:
                            break
                        img.color_map(idx, wand.color.Color(hexcolor))



                # CONVERT IMAGE INTO THE SELECTED COLORSPACE
                if _device.colorspace == DeviceSpecification.DisplaySupportedColors.DSC_BW or _device.colorspace == DeviceSpecification.DisplaySupportedColors.DSC_BWR or _device.colorspace == DeviceSpecification.DisplaySupportedColors.DSC_GRAY:
                    # IF A COLOR PALETTE IS SET APPLY IT
                    if _device.colorspace == DeviceSpecification.DisplaySupportedColors.DSC_BW:
                        img.quantize(number_colors=num_colors, colorspace_type='gray', dither=img.dither)
                    elif _device.colorspace == DeviceSpecification.DisplaySupportedColors.DSC_BWR:
                        img.quantize(number_colors=num_colors, colorspace_type='rgb', dither=img.dither)
                    elif _device.colorspace == DeviceSpecification.DisplaySupportedColors.DSC_GRAY:
                        img.quantize(number_colors=num_colors, colorspace_type='gray', dither=img.dither)
                    elif _device.colorspace == DeviceSpecification.DisplaySupportedColors.DSC_7COLOR:
                        img.quantize(number_colors=num_colors, colorspace_type='rgb', dither=img.dither)
                    else:
                        img.transform_colorspace('gray')

                elif _device.colorspace == DeviceSpecification.DisplaySupportedColors.DSC_COLOR:
                    img.depth = 24
                    img.transform_colorspace('rgb')
                else:
                    raise Exception("Unsupported color space")

                # EXPORT AS BMP
                img.format = 'bmp'
                img.compression = 'no'  # This ensures no compression

                img.save(file=return_bytes)
                return_bytes.seek(0)
                return return_bytes

        elif _export_type == SVG_ExportTypes.JPG:
            return_bytes = io.BytesIO()
            # FIRST DO PNG CONVERSION
            png_bytes = io.BytesIO()
            cairosvg.svg2png(file_obj=img_io, write_to=png_bytes, output_width=_device.screen_size_w, parent_height=_device.screen_size_h, scale=scale_factor)
            png_bytes.seek(0)
            # CONVERT PNG TO JPEG
            im = Image.open(png_bytes)
            rgb_im = im.convert('RGB')
            rgb_im.save(return_bytes, format='JPEG', quality=95)
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


    def __init__(self):
        pass

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SVGRenderer, cls).__new__(cls)
            # Put any initialization here.
        return cls._instance
