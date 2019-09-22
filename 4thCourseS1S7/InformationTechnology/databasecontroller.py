from database import *

from PyQt5.QtWidgets import QTabWidget

class DataBaseController:
	def __init__(self):
		self.tabWidget = QTabWidget()
		self.database = DataBase()
		
	def changeName(self,name):
		self.database.name = name
		
	def addTable(self,table):
		self.database.addTable(table)
	
	def addTableController(self,controller):
		self.database.addTable(controller.table)
		self.tabWidget.addTab(controller.tableWidget,controller.table.name)