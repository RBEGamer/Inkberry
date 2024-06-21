

from DisplayFramework.pysvg import builders, structure, text, style

from DisplayFramework import DeviceSpecification, TileFactory, BaseTile
from DisplayFramework.pysvg.builders import TransformBuilder


class SVGTemplates:

    @staticmethod
    def GenerateCurrentDeviceScreen(_id: str, _device: DeviceSpecification.DeviceSpecification) -> str:
        document: structure.Svg = SVGTemplates.getEmptyTeamplate(_device)

        # APPEND TILES INTO TO FINAL DEVICE SCREEN SVG
        tiles: [] = TileFactory.TileFactory.GetTiles(_device)
        for t in tiles:
            t: BaseTile.BaseTile
            if t.spec.enabled:
                t.update()
                svg = t.render()
                document.addElement(svg)

        return document.getXML()

    @staticmethod
    def GenerateDeviceSetupScreen(_id: str, _device: DeviceSpecification.DeviceSpecification) -> str:
        return SVGTemplates.GenerateDeviceDisabledScreen(_id,  _device)

    @staticmethod
    def GenerateDeviceDisabledScreen(_id: str, _device: DeviceSpecification.DeviceSpecification) -> str:
        document: structure.Svg = SVGTemplates.getEmptyTeamplate(_device)

        document = SVGTemplates.getSystemStautsScreen(document, _device , _title="IntelliBoard ePaper Door Sign")
        xml: str = document.getXML()
        return xml

    @staticmethod
    def getSystemStautsScreen(_svg: structure.Svg, _device: DeviceSpecification.DeviceSpecification, _title: str = "---", _size: int = 3) -> structure.Svg:
        headline_offset_multiplier: int = 20
        headline_line_offset: int = 20
        headline_line_width: int = 10
        s: builders.StyleBuilder = builders.StyleBuilder({})
        s.setTextAnchor("middle")
        s.setDisplayAlign("middle")
        s.setFontFamily(fontfamily="Verdana")
        s.setFontSize('{}em'.format(_size))

        t = text.Text(_title, '50%', headline_offset_multiplier*_size)
        t.set_style(s.getStyle())
        _svg.addElement(t)
        # ADD H LINE
        shape_builder: builders.ShapeBuilder = builders.ShapeBuilder()
        cy: int = headline_offset_multiplier*_size + headline_line_offset
        l: builders.ShapeBuilder = shape_builder.createRect(x=0, y=cy, width=_device.screen_size_w, height=headline_line_width, fill='black')
        _svg.addElement(l)

        # ADD SYSTEM INFO
        info_text: str = ""

        for k, v in _device.to_dict().items():
            info_text = "{}={}".format(k, v)

            cy += headline_line_offset* 1.5
            _svg.addElement(text.Text(info_text, 10, cy))
        return _svg
    @staticmethod
    def getEmptyTeamplate(_device: DeviceSpecification.DeviceSpecification) -> structure.Svg:
        w: int = _device.screen_size_w
        h: int = _device.screen_size_h

        # SETUP DOCUMENT
        svg_document: structure.Svg = structure.Svg()




        svg_document.set_x(0)
        svg_document.set_y(0)
        svg_document.set_width(w)
        svg_document.set_height(h)
        svg_document.set_viewBox("{} {} {} {}".format(0, 0, w, h))
        # ADD CONTENT RECT
        shape_builder: builders.ShapeBuilder = builders.ShapeBuilder()

        scale_transform = TransformBuilder()
        scale_transform.setScaling(_device.content_scale, _device.content_scale)
        svg_document.set_transform(scale_transform.getTransform())

        # ADD RECT FOR CONTENT TO LIVE IN
        content_rect = shape_builder.createRect(0, 0, w, h, strokewidth=1,stroke="black", fill="rgb(250, 250, 250)")
        svg_document.addElement(content_rect)
        return svg_document
