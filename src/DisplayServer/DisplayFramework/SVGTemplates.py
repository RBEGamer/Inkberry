

from DisplayFramework.pysvg import builders, structure, text, style
from DisplayFramework import DeviceSpecification, TileFactory, BaseTile, TileSpecification, SVGHelper, Devices
from DisplayFramework.tiles import QrTile
from DisplayFramework.pysvg.builders import TransformBuilder


class SVGTemplates:



    @staticmethod
    def GetScaledSVGContent(_svg: structure.Svg, _target_width) -> structure.Svg:
        if not _target_width or _target_width <= 0:
            return _svg

        origin_w: int = _svg.get_width()
        origin_h: int = _svg.get_height()

        scale_factor: float = _target_width / origin_w

        # SCALE CONTENT

        # SET NEW SVG SIZE TO RENDER IN CORRECT DIMENSIONS
        new_w: int = int(origin_w * scale_factor)
        new_h: int = int(origin_h * scale_factor)
        _svg.set_x(0)
        _svg.set_y(0)
        _svg.set_width(new_w)
        _svg.set_height(new_h)
        _svg.set_viewBox("{} {} {} {}".format(0, 0, new_w, new_h))

        return _svg
    @staticmethod
    def GenerateCurrentDeviceScreen(_id: str, _device: DeviceSpecification.DeviceSpecification, _target_width: int = 0) -> str:

        # IF A PARENT IS SET MODIFY THE SPECIFICATION
        if _device.parent_id is not None:
            if len(_device.parent_id) > 0:
                if Devices.Devices.CheckDeviceExists(_device.parent_id):
                    parent_spec: DeviceSpecification.DeviceSpecification = Devices.Devices.GetDeviceSpecification(_device.parent_id)

                    if not Devices.Devices.CheckDeviceEnabled(parent_spec.device_id):
                        return SVGTemplates.GenerateDeviceDisabledScreen(_id, _device, _target_width, _headline_text_addition=" [PARENT]")

                    # UPDATE PARENT TILESPECIFICATION UPDATE ENTRY
                    _device.tile_specifications = parent_spec.tile_specifications

                    # UPDATE PARAMETER DICT TOO TODO


        document: structure.Svg = SVGTemplates.getEmptyTeamplate(_device)
         # APPEND TILES INTO TO FINAL DEVICE SCREEN SVG
        tiles: [] = TileFactory.TileFactory.GetTiles(_device)
        for t in tiles:
            t: BaseTile.BaseTile
            if t.spec.enabled:
                t.update()
                svg = t.render()
                document.addElement(svg)

        if _target_width and _target_width > 0:
            document = SVGTemplates.GetScaledSVGContent(document, _target_width)

        return document.getXML()

    @staticmethod
    def GenerateDeviceSetupScreen(_id: str, _device: DeviceSpecification.DeviceSpecification, _target_width: int = 0, _qrcode_url: str = "inkberry.marcelochsendorf.com") -> str:
        _device.image_filter = DeviceSpecification.DisplayImageFilters.DIF_NONE
        _device.colorspace = DeviceSpecification.DisplaySupportedColors.DSC_BW
        document: structure.Svg = SVGTemplates.getEmptyTeamplate(_device)
        document = SVGTemplates.getSystemStautsScreen(document, _device, _title="SETUP:{}".format(_id), _qrcode_url=_qrcode_url)

        if _target_width and _target_width > 0:
            document = SVGTemplates.GetScaledSVGContent(document, _target_width)

        xml: str = document.getXML()
        return xml

    @staticmethod
    def GenerateDeviceDisabledScreen(_id: str, _device: DeviceSpecification.DeviceSpecification, _target_width: int = 0, _qrcode_url: str = "inkberry.marcelochsendorf.com", _headline_text_addition: str = "") -> str:
        _device.image_filter = DeviceSpecification.DisplayImageFilters.DIF_NONE
        _device.colorspace = DeviceSpecification.DisplaySupportedColors.DSC_BW
        document: structure.Svg = SVGTemplates.getEmptyTeamplate(_device)
        document = SVGTemplates.getSystemStautsScreen(document, _device , _title="DISABLED{}:{}".format(_id, _headline_text_addition), _qrcode_url=_qrcode_url)

        if _target_width and _target_width > 0:
            document = SVGTemplates.GetScaledSVGContent(document, _target_width)

        xml: str = document.getXML()
        return xml

    @staticmethod
    def getSystemStautsScreen(_svg: structure.Svg, _device: DeviceSpecification.DeviceSpecification, _title: str = "---", _headline_size: int = 3, _list_text_site: int = 2, _qrcode_url: str = None) -> structure.Svg:
        headline_offset_multiplier: int = 15
        headline_line_offset: int = 5
        headline_line_width: int = 5
        s: builders.StyleBuilder = builders.StyleBuilder({})
        s.setTextAnchor("left")
        s.setDisplayAlign("left")
        s.setFontFamily(fontfamily="Verdana")
        s.setFontSize('{}em'.format(_headline_size))

        t = text.Text(_title, '5%', headline_offset_multiplier*_headline_size)
        t.set_style(s.getStyle())
        _svg.addElement(t)
        # ADD H LINE
        shape_builder: builders.ShapeBuilder = builders.ShapeBuilder()
        cy: int = headline_offset_multiplier*_headline_size + headline_line_offset
        l: builders.ShapeBuilder = shape_builder.createRect(x=0, y=cy, width=_device.screen_size_w, height=headline_line_width, fill='black')



        # ADD QR CODE FOR EASY SETUP
        if _qrcode_url is not None:
            qrctsp: TileSpecification.TileSpecification = TileSpecification.TileSpecification()
            qrctsp.position.size_w = _device.screen_size_h / 2
            qrctsp.position.size_h = _device.screen_size_h / 2
            qrctsp.parameters['scale_factor'] = 0.3

            qrctsp.position.pos_x = 10
            qrctsp.position.pos_y = headline_line_offset * headline_offset_multiplier
            qrcode: QrTile.QrTile = QrTile.QrTile(qrctsp)

            qrcode.update_parameters({'url': _qrcode_url})
            _svg.addElement(qrcode.render())






        # ADD SYSTEM INFO
        info_text: str = ""

        #info_style : builders.StyleBuilder = builders.StyleBuilder({})
        #info_style.setFontSize('{}em'.format(_list_text_site))
        #for k, v in _device.to_dict().items():
        #    info_text = "{}={}".format(k, v)
        #    cy += headline_line_offset * 1.5
        #    list_text_element = text.Text(info_text, 10, cy)
        #    list_text_element.set_style(info_style.getStyle())
        #    _svg.addElement(list_text_element)

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
