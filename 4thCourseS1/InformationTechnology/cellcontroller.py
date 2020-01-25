from cell import *
from validators import *
from image import *

from PyQt5.QtWidgets import QTableWidgetItem, QLineEdit
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class CellController:
    def __init__(self, cell=None):
        if cell is None:
            self.cell = Cell()
        else:
            self.cell = cell
        self.cellWidget = QLineEdit(self.cell.data)
        self.setType(self.cell.type)

    def setType(self, type):
        self.cell.type = type
        if type == DataType.Integer:
            self.cellWidget.setValidator(QIntValidator())
            self.cellWidget.editingFinished.connect(self.setData)
        elif type == DataType.Real:
            self.realValidator = QDoubleValidator()
            self.realValidator.setNotation(QDoubleValidator.StandardNotation)
            self.cellWidget.setValidator(self.realValidator)
            self.cellWidget.editingFinished.connect(self.setData)
        elif type == DataType.Char:
            self.charValidator = CharValidator()
            self.cellWidget.setValidator(self.charValidator)
            self.cellWidget.editingFinished.connect(self.setData)
        elif type == DataType.String:
            self.cellWidget.editingFinished.connect(self.setData)
        elif type == DataType.Picture:
            self.cellWidget = Image(self.cell.data)
            self.cellWidget.mousePressEvent = lambda _:self.setPicture()
        elif type == DataType.RealInvl:
            self.rangeValidator = RealInvlValidator(self.cellWidget)
            self.rangeValidator.setRange(0, 1)
            self.addOptional(['interval', [0, 1]])
            self.cellWidget.setValidator(self.rangeValidator)
            self.cellWidget.editingFinished.connect(self.setData)

    def setData(self):
        self.cell.setData(self.cellWidget.text())
        
    def setPicture(self):
        file = QFileDialog.getOpenFileName(None, 'Load picture', filter='*.png')
        if file[0]:
            self.cell.setData(file[0])
            self.cellWidget.setPath(file[0])

    def addOptional(self, optional):
        if optional == None:
            return
        self.cell.optionalInfo = optional
        self.rangeValidator = RealInvlValidator(self.cellWidget)
        self.rangeValidator.setRange(optional[1][0], optional[1][1])
        self.cellWidget.setValidator(self.rangeValidator)

    def isPresentData(self):
        return self.cell.isPresentData()
