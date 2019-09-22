from row import *
from column import *

class Table:
	def __init__(self,name=""):
		self.name = name
		self.columns = []
		self.rows = []		
		
	def addColumn(self,header,type):
		self.columns.append(Column(header,type))
		
	def addRow(self,data):
		cells = []
		for i in range(len(data)):
			if Cell.isValidData(data[i],self.columns[i].type):
				cells.append(Cell(data[i],self.columns[i].type))
		self.rows.append(Row(cells))
		
	def getHeaders(self):
		headers = []
		for column in self.columns:
			headers.append(column.header)
		return headers