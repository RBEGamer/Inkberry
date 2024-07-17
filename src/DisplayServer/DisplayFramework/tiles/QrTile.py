import PIL.Image
from DisplayFramework.tiles import ImageTile
from DisplayFramework.pysvg import structure



import qrcode
import qrcode.image.svg
import qrcode.image.pil

class QrTile(ImageTile.ImageTile):

    DEFAULT_PARAMETER: dict = {
        "types": {
            "url": "str",
            "width": "int"
        }, "default": {
            "url": "",
            "width": 10
        }
    }




    def update_parameters(self, _parameter: dict):
        for k, v in _parameter.items():
            pass

    def update(self):
       pass

    def get_parameter_types(self) -> dict:
        return self.DEFAULT_PARAMETER['types']

    def get_parameter_defaults(self) -> dict:
        return self.DEFAULT_PARAMETER['default']

    def get_parameter_current(self) -> dict:
        return self.spec.parameters


    def render(self) -> structure.Svg:

        # CREATE QR ELEMENT
        url: str = self.spec.parameters.get('url', '')

        img: PIL.Image = qrcode.make("{}".format(url), image_factory=qrcode.image.pil.PilImage)
        width, height = img.size
        #im = img.resize((width // 2, height // 2))
        #t = 0
        #buffered: BytesIO = BytesIO()
        #img.save(buffered)
        #qr_svg_text: str = buffered.getvalue().decode('utf-8')

        # REMOVE <?xml version='1.0' encoding='UTF-8'?>
        #sp: [str] = qr_svg_text.split('\n')
        #if len(sp) > 1:
        #    if '<?xml' in sp[0]:
        #        sp.pop(0)
        #    qr_svg_text = ''.join(sp)

        #svg_document: structure.Svg = structure.Svg()
        #svg_document.set_id(self.spec.name)
        #svg_document.set_x(self.spec.position.pos_x)
        #svg_document.set_y(self.spec.position.pos_y)
        #svg_document.addElement(structure.BaseElement(self.spec.name))

        return ImageTile.ImageTile.generate_image_container(img, self.spec)