from table import *
from datatype import *
from cellcontroller import *

from PyQt5.QtWidgets import QTableWidget

class TableController:
	def __init__(self):
		self.table = Table()
		self.tableWidget = QTableWidget()
		self.cellControllers = []
		
	def setName(self,name):
		self.table.name = name
		
	def addTable(self,table):
		self.table = table
		self.updateWidget()
		
	def addEmptyRow(self):
		currRowCount = self.tableWidget.rowCount()
		self.tableWidget.insertRow(currRowCount)
		row = []
		for i in range(len(self.table.columns)):
			cell = CellController()
			cell.setType(self.table.columns[i].type)
			row.append(cell)
			self.tableWidget.setCellWidget(currRowCount,i,cell.cellWidget)
		self.cellControllers.append(row)
		
	def addColumn(self,data,type):
		if type == 0:
			type = DataType.Integer
		elif type == 1:
			type = DataType.Real
		elif type == 2:
			type = DataType.Char
		elif type == 3:
			type = DataType.String
		elif type == 4:
			type = DataType.Picture
		elif type == 5:
			type = DataType.RealInvl
		else:
			raise Exception("Incorrect type")
		self.table.addColumn(data,type)
		self.updateWidget()
	
	def updateWidget(self):
		self.tableWidget.setColumnCount(len(self.table.columns))
		self.tableWidget.setHorizontalHeaderLabels(self.table.getHeaders())