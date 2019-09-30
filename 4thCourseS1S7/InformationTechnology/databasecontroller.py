from database import *
from tablecontroller import *

from PyQt5.QtWidgets import QTabWidget,QTableWidget

class DataBaseController:
	def __init__(self):
		self.tabWidget = QTabWidget()
		self.tableControllers = []
		self.database = DataBase()
		
	def changeName(self,name):
		self.database.name = name
		
	def addTable(self,table):
		self.database.addTable(table)
		self.tableControllers.append(TableController())
		self.tableControllers[-1].addTable(table)
		self.tableControllers[-1].addEmptyRow()
		self.tabWidget.addTab(self.tableControllers[-1].tableWidget,table.name)
		
	def saveDB(self,filename):
		self.database.save(filename)
		
	def loadDB(self,filename):
		self.tabWidget = QTabWidget()
		self.tableControllers = []
		self.database = DataBase.load(filename)
		for table in self.database.tables:
			self.tableControllers.append(TableController())
			self.tableControllers[-1].addTable(table)
			self.tableControllers[-1].addEmptyRow()
			self.tabWidget.addTab(self.tableControllers[-1].tableWidget,table.name)