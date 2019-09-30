from cell import *

from PyQt5.QtWidgets import QTableWidgetItem, QLineEdit
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class CellController:
	def __init__(self):
		self.cellWidget = QLineEdit()
		self.cell = Cell()
		
	def setType(self,type):
		if type == DataType.Integer:
			self.cellWidget.setValidator(QIntValidator())
		elif type == DataType.Real:
			self.realValidator = QDoubleValidator()
			self.realValidator.setNotation(QDoubleValidator.StandardNotation)
			self.cellWidget.setValidator(self.realValidator)
		elif type == DataType.Char:
			pass
		elif type == DataType.String:
			pass
		elif type == DataType.Picture:
			pass
		elif type == DataType.RealInvl:
			self.rangeValidator = QDoubleValidator()
			self.rangeValidator.setRange(0,100,6)
			self.rangeValidator.setNotation(QDoubleValidator.StandardNotation)
			self.cellWidget.setValidator(self.rangeValidator)
			
		self.cell = Cell("",type)