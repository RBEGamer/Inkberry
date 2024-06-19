class SVGHelper:


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