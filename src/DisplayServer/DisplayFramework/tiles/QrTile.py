import PIL.Image
from DisplayFramework import BaseTile
from DisplayFramework.tiles import ImageTile
from DisplayFramework.pysvg import structure



import qrcode
import qrcode.image.svg
import qrcode.image.pil

class QrTile(BaseTile.BaseTile):

    DEFAULT_PARAMETER: dict = {
        "types": {
            "url": "str",
            "scale_factor": "int"
        }, "default": {
            "url": "",
            "scale_factor": 0.5
        }
    }


    def update(self):
       pass

    def get_parameter_types(self) -> dict:
        return self.DEFAULT_PARAMETER['types']

    def get_parameter_defaults(self) -> dict:
        return self.DEFAULT_PARAMETER['default']

    def get_parameter_current(self) -> dict:
        return self.spec.parameters


    def render(self) -> structure.Svg:

        # CREATE URL QR ELEMENT
        url: str = self.spec.parameters.get('url', '')
        # CREATE QR CODE IMAGE
        img: PIL.Image = qrcode.make("{}".format(url), image_factory=qrcode.image.pil.PilImage)


        # USE A IMAGE TILE AS BASE TO GENERATE THE SVG FILE OF THE QR IMAGE
        # CURRENTLY THIS WAY IS USED TO ALWAYS USE THE LATEST TILE SPECIFICATION
        img_tile: ImageTile.ImageTile = ImageTile.ImageTile(self.spec)
        img_tile.update_parameters({'scale_factor': self.get_parameter_current()['scale_factor']})

        return ImageTile.ImageTile.generate_image_container(img, img_tile.spec)