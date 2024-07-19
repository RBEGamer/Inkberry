import io
import math
from io import BytesIO
import cairosvg
from PIL import Image
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

        svg_size_w, svg_size_h = SVGRenderer.SVGGetSize(_svg)

        if svg_size_w != _device.screen_size_w or svg_size_h != _device.screen_size_h:
            scale_factor = max([0.1, min([_device.screen_size_w / svg_size_w, _device.screen_size_h / svg_size_h])])

        return scale_factor


    @staticmethod
    def generate_red_shades(num_shades=8):
        red_shades = []
        for i in range(num_shades):
            # Calculate the red value, incrementally increasing from light to full red
            red_value = int(255 * (i + 1) / num_shades)
            # Convert the RGB value to hex format
            hex_color = f'#{red_value:02X}0000'
            red_shades.append(hex_color)
        return red_shades

    @staticmethod
    def generate_gray_shades(num_shades=8):
        red_shades = []
        for i in range(num_shades):
            # Calculate the red value, incrementally increasing from light to full red
            red_value = int(255 * (i + 1) / num_shades)
            # Convert the RGB value to hex format
            hex_color = f'#{red_value:02X}{red_value:02X}{red_value:02X}'
            red_shades.append(hex_color)
        return red_shades

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


                # Create a custom colormap with only black and white
                if _device.colorspace == DeviceSpecification.DisplaySupportedColors.DSC_BW:
                    num_colors = 2
                    img.depth = 4
                    img.type = 'palette'
                    img.color_map(0, wand.color.Color('#000000'))
                    img.color_map(2, wand.color.Color('#FFFFFF'))
                elif _device.colorspace == DeviceSpecification.DisplaySupportedColors.DSC_BWR:
                    # FOR RED BLACK WHITE, A ADDITIONAL COLOR PALETTE IS GENERATED FOR RED AND GRAY COLORS
                    num_colors = 16
                    img.depth = 8
                    img.type = 'palette'
                    palette_index = 0

                    if num_colors > 2:
                        # ADD GRAY SHAED TO COLOR PALETTE
                        gray_steps: [str] = SVGRenderer.generate_gray_shades(math.floor(num_colors / 2))
                        for idx, red_step in enumerate(gray_steps):
                            img.color_map(idx+palette_index, wand.color.Color(red_step))
                        palette_index = palette_index + len(gray_steps)

                        # ADD RED SHADES TO COLOR PALETTE
                        red_steps: [str] = SVGRenderer.generate_red_shades(math.floor(num_colors/2))
                        for idx, red_step in enumerate(red_steps):
                            img.color_map(idx+palette_index, wand.color.Color(red_step))
                        palette_index = palette_index + len(red_steps)

                elif _device.colorspace == DeviceSpecification.DisplaySupportedColors.DSC_GRAY:
                    # FOR GRAY, A ADDITIONAL COLOR PALETTE IS GENERATED GRAY COLORS
                    num_colors = 16
                    img.depth = 8
                    img.type = 'palette'
                    palette_index = 0

                    gray_steps: [str] = SVGRenderer.generate_gray_shades(math.floor(num_colors))
                    for idx, red_step in enumerate(gray_steps):
                        img.color_map(idx + palette_index, wand.color.Color(red_step))
                    palette_index = palette_index + len(gray_steps)



                # CONVERT IMAGE INTO THE SELECTED COLORSPACE
                if _device.colorspace == DeviceSpecification.DisplaySupportedColors.DSC_BW or _device.colorspace == DeviceSpecification.DisplaySupportedColors.DSC_BWR or _device.colorspace == DeviceSpecification.DisplaySupportedColors.DSC_GRAY:
                    # IF A COLOR PALETTE IS SET APPLY IT
                    if _device.colorspace == DeviceSpecification.DisplaySupportedColors.DSC_BW:
                        img.quantize(number_colors=num_colors, colorspace_type='gray')
                    elif _device.colorspace == DeviceSpecification.DisplaySupportedColors.DSC_BWR:
                        img.quantize(number_colors=num_colors, colorspace_type='rgb')
                    elif _device.colorspace == DeviceSpecification.DisplaySupportedColors.DSC_GRAY:
                        img.quantize(number_colors=num_colors, colorspace_type='gray')
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

                img.save(filename='t.bmp')
                img.save(file=return_bytes)
                return_bytes.seek(0)

                return return_bytes
                #if _export_type == SVG_ExportTypes.BMP:
                #    return return_bytes
                #else:
                    # CAL EPD NEEDS A BIT MODIFIED BMP IMAGE
                #    pil_return_bytes: BytesIO = BytesIO()
                #    pilimg = Image.new('RGB', (255, 255), "black")  # Create a new black image
                #    pixels = img.load()  # Create the pixel map
                #    for i in range(img.size[0]):  # For every pixel:
                #        for j in range(img.size[1]):
                #            pixels[i, j] = (i, j, 100)  # Set the colour accordingly
                #    #if len(img.split()) == 4:
                #    #    r, g, b, a = pilimg.split()
                #    #    pilimg = Image.merge("RGB", (r, g, b))
                #    pilimg.save(pil_return_bytes, format='BMP')#

                #    pil_return_bytes.seek(0)
                #    return pil_return_bytes

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

        rt.seek(0)
        return rt



    def __init__(self):
        pass

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SVGRenderer, cls).__new__(cls)
            # Put any initialization here.
        return cls._instance
