from cell import *
from validators import *
from image import *

from PyQt5.QtWidgets import QTableWidgetItem, QLineEdit
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class CellController:
	def __init__(self,cell=Cell()):
		self.cell = cell
		self.cellWidget = QLineEdit(cell.data)
		
	def setType(self,type):
		self.cell = Cell("",type)
		if type == DataType.Integer:
			self.cellWidget.setValidator(QIntValidator())
		elif type == DataType.Real:
			self.realValidator = QDoubleValidator()
			self.realValidator.setNotation(QDoubleValidator.StandardNotation)
			self.cellWidget.setValidator(self.realValidator)
		elif type == DataType.Char:
			self.charValidator = CharValidator()
			self.cellWidget.setValidator(self.charValidator)
		elif type == DataType.String:
			pass
		elif type == DataType.Picture:
			self.cellWidget = Image() 
		elif type == DataType.RealInvl:
			self.rangeValidator = RealInvlValidator(self.cellWidget)
			self.rangeValidator.setRange(0,1)
			self.addOptional(['interval',[0,1]])
			self.cellWidget.setValidator(self.rangeValidator)
		self.cellWidget.editingFinished.connect(self.setData)
		
	def setData(self):
		self.cell.setData(self.cellWidget.text())
		
	def addOptional(self,optional):
		if optional == None:
			return
		self.cell.optionalInfo = optional
		self.rangeValidator = RealInvlValidator(self.cellWidget)
		self.rangeValidator.setRange(optional[1][0],optional[1][1])
		self.cellWidget.setValidator(self.rangeValidator)
		
	def isPresentData(self):
		return self.cell.isPresentData()