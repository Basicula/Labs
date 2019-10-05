from row import *
from column import *

class Table:
	def __init__(self,name=""):
		self.name = name
		self.columns = []
		self.rows = []		
		
	@property
	def __dict__(self):
		return {
				'name' : self.name,
				'columns' : self.columns,
				'rows' : self.rows
				}
				
	@staticmethod
	def fromDict(dict):
		table = Table(dict['name'])
		for column in dict['columns']:
			table.columns.append(Column.fromDict(column))
		for row in dict['rows']:
			table.rows.append(Row.fromDict(row))
		return table
		
	def addColumn(self,header,type):
		self.columns.append(Column(header,type))
		
	def addRowData(self,data):
		cells = []
		for i in range(len(data)):
			if Cell.isValidData(data[i],self.columns[i].type):
				cells.append(Cell(data[i],self.columns[i].type))
		self.rows.append(Row(cells))
		
	def addRow(self,row):
		self.rows.append(Row(row))
		
	def getHeaders(self):
		headers = []
		for column in self.columns:
			headers.append(column.header)
		return headers