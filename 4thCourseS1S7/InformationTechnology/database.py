from table import *

import json

class DataBase:
	def __init__(self,name=""):
		self.tables = []
		self.name = name
		
	def save(self,filename):
		with open(filename,'w') as file:
			json.dump(self,file,default=lambda o: o.__dict__,indent=4)
			
	@staticmethod
	def load(filename):
		with open(filename,'r') as file:
			data = json.load(file)
			return DataBase.fromDict(data)
				
			
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
				
def createSampleDB():
	db = DataBase("Simple data base")
	db.newTable("Users")
	db.tables[-1].addColumn("Age",DataType.Integer)
	db.tables[-1].addColumn("Name",DataType.String)
	db.tables[-1].addRow([21,"Kek Kekovich"])
	db.tables[-1].addRow([23,"Jim"])
	return db
	
if __name__ == "__main__":
	db = createSampleDB()
	db.save("test.json")