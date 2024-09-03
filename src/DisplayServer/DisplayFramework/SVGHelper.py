import colorsys
import hashlib
import re
import html
class SVGHelper:




    def sanitize_svg_input(_textinput: str) -> str:

        t = html.escape(_textinput)
        return t



    @staticmethod
    def generate_sha1_hash(input_string):
        # Create a new sha1 hash object
        sha1_hash = hashlib.sha1()

        # Update the hash object with the bytes of the input string
        sha1_hash.update(input_string.encode('utf-8'))

        # Get the hexadecimal digest of the hash
        hex_digest = sha1_hash.hexdigest()

        return hex_digest

    @staticmethod
    def GetSVGGroupContentString(_svg_str: str):
        START: str = '<g '
        END: str = '</g>'
        if _svg_str.startswith(START):
            _svg_str = _svg_str[len(START):]
        head, sep, tail = _svg_str.partition(START)
        svg_str: str = START + tail
        svg_str = svg_str[::-1]  # REVERSE
        head, sep, tail = svg_str.partition(END[::-1])  # GET EVERYTHING
        svg_str = tail[::-1]
        return svg_str

    @staticmethod
    def RemoveSVGPreamble(_svg_str: str):
        START: str = '<svg '
        END: str = '</g>'
        if _svg_str.startswith(START):
            _svg_str = _svg_str[len(START):]
        head, sep, tail = _svg_str.partition(START)
        svg_str: str = START + tail
        return svg_str

    @staticmethod
    def generate_red_shades(num_shades: int = 8):
        red_shades: [str] = []
        for i in range(num_shades):
            # Calculate the red value, incrementally increasing from light to full red
            red_value = int(255 * (i + 1) / num_shades)
            # Convert the RGB value to hex format
            hex_color = f'#{red_value:02X}0000'
            red_shades.append(hex_color)
        return red_shades

    @staticmethod
    def generate_gray_shades(num_shades: int = 8):
        red_shades: [str] = []
        for i in range(num_shades):
            # Calculate the red value, incrementally increasing from light to full red
            red_value = int(255 * (i + 1) / num_shades)
            # Convert the RGB value to hex format
            hex_color = f'#{red_value:02X}{red_value:02X}{red_value:02X}'
            red_shades.append(hex_color)
        return red_shades


    @staticmethod
    def hex_color_from_rgb(r: float, g: float, b: float) -> str:
        return "#{:02x}{:02x}{:02x}".format(int(r * 255), int(g * 255), int(b * 255))

    @staticmethod
    def generate_seven_colors_colorpalette(total_colors: int):
        if total_colors <= 0:
            total_colors = 1


        base_hues: dict = {
            "Black": 0,  # Not used since black has no hue
            "White": 0,  # Not used since white has no hue
            "Red": 0,
            "Yellow": 60 / 360,
            "Blue": 240 / 360,
            "Green": 120 / 360,
            "Orange": 30 / 360
        }

        total_colors = total_colors * len(base_hues.keys())

        colors: [str] = []

        for color_name, hue in base_hues.items():
            for i in range(total_colors):
                saturation: float = i / (total_colors - 1) if total_colors > 1 else 0  # To avoid division by zero
                lightness: float = 0.5  # Fixed lightness for simplicity

                # Convert HSL to RGB
                r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)
                # Convert RGB to HEX
                hex_color: str = SVGHelper.hex_color_from_rgb(r, g, b)
                colors.append(hex_color)

        return colors