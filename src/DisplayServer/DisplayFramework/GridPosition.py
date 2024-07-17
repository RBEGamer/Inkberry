class GridPosition:

    pos_x: int = 0
    pos_y: int = 0
    size_w: int = 0
    size_h: int = 0
    _valid: bool = True

    def to_dict(self) -> dict:
        return self.__dict__()

    def __dict__(self) -> dict:
        return {
            'pos_x': self.pos_x,
            'pos_y': self.pos_y,
            'size_w': self.size_w,
            'size_h': self.size_h
        }

    def from_dict(self, _dict: dict):
        errors = 0
        if 'pos_x' in _dict:
            self.pos_x = int(_dict['pos_x'])
            errors = errors + 1
        if 'pos_y' in _dict:
            self.pos_y = int(_dict['pos_y'])
            errors = errors + 1
        if 'size_w' in _dict:
            self.size_w = int(_dict['size_w'])
            errors = errors + 1
        if 'size_h' in _dict:
            self.size_h = int(_dict['size_h'])
            errors = errors + 1

        if errors > 0:
            self._valid = True

    def __init__(self, _load_from_dict: dict = None):
        if _load_from_dict is not None:
            self.from_dict(_load_from_dict)