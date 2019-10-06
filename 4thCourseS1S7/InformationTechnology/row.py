from cell import *


class Row:
    def __init__(self, cells):
        self.cells = cells
        
    def isEmpty(self):
        for cell in cells:
            if cell.data != "":
                return False
        return True

    @property
    def __dict__(self):
        if self.isEmpty():
            return {}
        return {
            'cells': self.cells
        }

    @staticmethod
    def fromDict(dict):
        cells = []
        for cell in dict['cells']:
            cells.append(Cell.fromDict(cell))
        return Row(cells)
