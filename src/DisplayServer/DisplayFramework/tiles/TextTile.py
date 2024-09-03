from PIL import Image, ImageDraw, ImageFont
from DisplayFramework import BaseTile, TileSpecification, DeviceSpecification
from DisplayFramework.pysvg import structure, builders, text


class TextTile(BaseTile.BaseTile):
    DEFAULT_PARAMETER: dict = {
        "types": {
            "text": BaseTile.TileParameterTypes.STRING,
            "fontsize": BaseTile.TileParameterTypes.INTEGER,
            "rotation": BaseTile.TileParameterTypes.INTEGER,
        }, "default": {
            "text": "",
            "fontsize": 1,
            "rotation": 0,
        }
    }

    def __init__(self, _hardware: DeviceSpecification.DeviceSpecification, _specification: TileSpecification.TileSpecification):
        super().__init__(_hardware, _specification)


    def update(self) -> bool:
        return False



    def render(self) -> structure.Svg:


        rotation: int = self.get_spec_parameters('rotation')
        usertext: str = self.get_spec_parameters('text')
        fontsize: float = self.get_spec_parameters('fontsize')


        svg_document: structure.Svg = structure.Svg()
        svg_document.set_id(self.spec.name)
        svg_document.set_x(0)
        svg_document.set_y(0)
        svg_document.set_width(self.hardware_spec.screen_size_w)
        svg_document.set_height(self.hardware_spec.screen_size_h)

        if rotation > 0:
            svg_document.set_transform("rotate(-{})".format(rotation))


        s: builders.StyleBuilder = builders.StyleBuilder({})
        s.setTextAnchor("top")
        s.setDisplayAlign("left")
        s.setFontFamily(fontfamily="Verdana")
        s.setFontSize('{}pt'.format(fontsize))


        t = text.Text(usertext, '{}px'.format(self.spec.position.pos_x), '{}px'.format(self.spec.position.pos_y), rotate=rotation)
        t.set_style(s.getStyle())
        svg_document.addElement(t)

        # SET SVG DOCUMENT SIZE BASE ON THE BIGGEST VIEWBOX OF CONTAINONG ELEMENTS
        return svg_document
