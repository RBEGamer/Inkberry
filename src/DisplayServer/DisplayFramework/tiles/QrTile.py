import PIL.Image
from DisplayFramework import BaseTile, DeviceSpecification, TileSpecification
from DisplayFramework.tiles import ImageTile
from DisplayFramework.pysvg import structure



import qrcode
import qrcode.image.svg
import qrcode.image.pil

class QrTile(BaseTile.BaseTile):

    DEFAULT_PARAMETER: dict = {
        "types": {
            "url": BaseTile.TileParameterTypes.STRING,
            "scale_factor": BaseTile.TileParameterTypes.FLOAT
        }, "default": {
            "url": "",
            "scale_factor": 0.5
        }
    }

    def __init__(self, _hardware: DeviceSpecification.DeviceSpecification, _specification: TileSpecification.TileSpecification):
        super().__init__(_hardware, _specification)

    def update(self) -> bool:
       return False

    def render(self) -> structure.Svg:

        # CREATE URL QR ELEMENT
        url: str = self.spec.parameters.get('url', '')
        # CREATE QR CODE IMAGE
        img: PIL.Image = qrcode.make("{}".format(url), image_factory=qrcode.image.pil.PilImage)


        # USE A IMAGE TILE AS BASE TO GENERATE THE SVG FILE OF THE QR IMAGE
        # CURRENTLY THIS WAY IS USED TO ALWAYS USE THE LATEST TILE SPECIFICATION
        img_tile: ImageTile.ImageTile = ImageTile.ImageTile(self.hardware_spec, self.spec)
        return ImageTile.ImageTile.generate_image_container(img, img_tile.spec, _scale_factor=self.get_spec_parameters('scale_factor', 1.0))