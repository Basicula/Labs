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
		self.update()
		
	def isNeedEmptyRow(self):
		currRowCount = self.tableWidget.rowCount()
		if currRowCount == 0:
			return True
		ok = True
		for cell in self.cellControllers[-1]:
			ok &= cell.isPresentData()
		return ok
		
	def addEmptyRow(self):
		if not self.isNeedEmptyRow():
			return
		currRowCount = self.tableWidget.rowCount()
		self.tableWidget.insertRow(currRowCount)
		row = []
		table_row = []
		for i in range(len(self.table.columns)):
			cell = CellController()
			cell.setType(self.table.columns[i].type)
			cell.addOptional(self.table.columns[i].optionalInfo)
			def updateCell():
				self.tableWidget.cellChanged.emit(currRowCount,i)
			cell.cellWidget.editingFinished.connect(updateCell)
			row.append(cell)
			table_row.append(cell.cell)
			self.tableWidget.setCellWidget(currRowCount,i,cell.cellWidget)
		self.cellControllers.append(row)
		self.table.addRow(table_row)
		
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
		self.update()
	
	def update(self):
		self.tableWidget.setColumnCount(len(self.table.columns))
		self.tableWidget.setHorizontalHeaderLabels(self.table.getHeaders())
		for row in self.table.rows:
			currRowCount = self.tableWidget.rowCount()
			self.tableWidget.insertRow(currRowCount)
			rw = []
			for i,cell in enumerate(row.cells):
				c = CellController(cell)
				def updateCell():
					self.tableWidget.cellChanged.emit(currRowCount,i)
				c.cellWidget.editingFinished.connect(updateCell)
				rw.append(c)
			self.tableWidget.setCellWidget(currRowCount,i,c.cellWidget)
			self.cellControllers.append(rw)