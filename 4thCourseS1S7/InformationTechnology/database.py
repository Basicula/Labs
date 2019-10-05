from table import *

import json

class DataBase:
	def __init__(self,name=""):
		self.tables = []
		self.name = name				
			
	def newTable(self,name):
		newTable = Table(name)
		self.tables.append(newTable)
	
	def addTable(self,table):
		if type(table) is Table:
			self.tables.append(table)
		else:
			raise Exception("Given table is not a Table object")
			
	@property
	def __dict__(self):
		return {
				'name' : self.name,
				'tables' : self.tables
				}
				
	@staticmethod
	def fromDict(dict):
		db = DataBase(dict['name'])
		for table in dict['tables']:
			db.tables.append(Table.fromDict(table))
		return db
				