from table import *

from PyQt5.QtWidgets import QTableWidget

class TableController:
	def __init__(self):
		self.table = Table()
		self.tableWidget = QTableWidget()
		
	def setName(self,name):
		self.table.name = name
		
	def addColumn(self,data,type):
		self.table.addColumn(data,type)
		self.tableWidget.setColumnCount(len(self.table.columns))
		self.tableWidget.setHorizontalHeaderLabels(self.table.getHeaders())