from DisplayFramework import BaseTile, TileSpecification
from DisplayFramework.pysvg import structure, builders, text


class TextTile(BaseTile.BaseTile):

    DEFAULT_PARAMETER: dict = {
        "types": {
            "text": "str",
            "fontsize": "int",
            "charakter_rotation": "int"
        },"default": {
            "text": "",
            "fontsize": 1,
            "charakter_rotation": 0
        }
    }

    spec: TileSpecification.TileSpecification = TileSpecification.TileSpecification()

    def __init__(self, _specification: TileSpecification.TileSpecification):
        self.spec = _specification

        # FILL DEFAULT PARAMETER IF KEYS NOT PRESNET
        for k in self.DEFAULT_PARAMETER['default']:
            if k not in self.spec.parameters.keys():
                self.spec.parameters[k] = self.DEFAULT_PARAMETER['default'][k]





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
        svg_document: structure.Svg = structure.Svg()
        svg_document.set_id(self.spec.name)
        svg_document.set_x(self.spec.position.pos_x)
        svg_document.set_y(self.spec.position.pos_y)
        svg_document.set_width(self.spec.position.size_w)
        svg_document.set_height(self.spec.position.size_h)

        if int(self.spec.parameters.get('rotation', 0)) > 0:
            svg_document.set_transform("rotate(-{})".format(self.spec.parameters.get('rotation', 0)))
            self.spec.parameters.get('start', 0)

        # ADD CONTENT RECT
        shape_builder: builders.ShapeBuilder = builders.ShapeBuilder()

        s: builders.StyleBuilder = builders.StyleBuilder({})
        s.setTextAnchor("middle")
        s.setDisplayAlign("middle")
        s.setFontFamily(fontfamily="Verdana")
        s.setFontSize('{}em'.format(self.spec.parameters.get('fontsize', 2)))

        rotation = None
        if int(self.spec.parameters.get('charakter_rotation', 0)) > 0:
            rotation = int(self.spec.parameters.get('charakter_rotation', 0))

        t = text.Text(self.spec.parameters.get('text', ''), '50%', '50%', rotate=rotation)
        t.set_style(s.getStyle())
        svg_document.addElement(t)

        return svg_document