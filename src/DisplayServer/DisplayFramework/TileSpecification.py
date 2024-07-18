from DisplayFramework import GridPosition
class TileSpecification:

    name: str = ""
    module_name: str = ""
    parameters: dict = {}
    position: GridPosition.GridPosition = GridPosition.GridPosition()
    enabled: bool = True
    _valid: bool = True


    def is_valid(self) -> bool:
        return self._valid

    def to_dict(self) -> dict:
        return self.__dict__()

    def from_dict(self, _dict: dict):
        errors = 0
        if 'name' in _dict:
            self.name = _dict['name']
            errors = errors + 1
        if 'module_name' in _dict:
            self.module_name = _dict['module_name']
            errors = errors + 1
        if 'parameters' in _dict:
            self.parameters = _dict['parameters']
            errors = errors + 1
        if 'position' in _dict:
            self.position = GridPosition.GridPosition(_dict['position'])
        if 'enabled' in _dict:
            self.enabled = _dict['enabled']
        if errors > 0:
            self._valid = True


    def __dict__(self) -> dict:
        return {
            'name': self.name,
            'module_name': self.module_name,
            'parameters': self.parameters,
            'position': self.position.to_dict(),
            'enabled': self.enabled
        }


    def __init__(self, _load_from_dict: dict = None):
        if _load_from_dict is not None:
            self.from_dict(_load_from_dict)