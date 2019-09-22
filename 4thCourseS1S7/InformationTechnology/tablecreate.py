from tablecontroller import *

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class TableCreatWindow(QWidget):
	def __init__(self,tableController):
		super().__init__()
		
		self.setWindowTitle("Create table")
		
		self.setGeometry(200, 200, 400, 400)
		
		self.tableController = tableController
		
		self.initUI()
		
	def changeTableName(self):
		self.tableController.setName(self.nameEdit.text())
		
	def tableName(self):
		self.nameEditLayout = QHBoxLayout()
		self.nameLabel = QLabel("Table name:")
		self.nameEditLayout.addWidget(self.nameLabel)
		self.nameEdit = QLineEdit()
		self.nameEdit.textChanged.connect(self.changeTableName)
		self.nameEditLayout.addWidget(self.nameEdit)
		self.mainLayout.addLayout(self.nameEditLayout)
		
	def tablePreview(self):
		self.tablePreviewLayout = QVBoxLayout()
		self.tablePreviewLayout.addWidget(self.tableController.tableWidget)
		self.mainLayout.addLayout(self.tablePreviewLayout)
		
	def addColumn(self):
		self.tableController.addColumn(self.columnHeaderEditor.text(),self.columnTypeEditor.currentIndex())
		self.columnHeaderEditor.clear()
		
	def columnInfo(self):
		self.columnEditorLayout = QVBoxLayout()
		
		self.columnHeaderInfoLayout = QHBoxLayout()
		self.columnHeaderLabel = QLabel("Column header:")
		self.columnHeaderInfoLayout.addWidget(self.columnHeaderLabel)
		self.columnHeaderEditor = QLineEdit()
		self.columnHeaderInfoLayout.addWidget(self.columnHeaderEditor)
		
		self.columnEditorLayout.addLayout(self.columnHeaderInfoLayout)
		
		self.columnTypeInfoLayout = QHBoxLayout()
		self.columnTypeLabel = QLabel("Data type for column:")
		self.columnTypeInfoLayout.addWidget(self.columnTypeLabel)
		self.columnTypeEditor = QComboBox()
		self.columnTypeEditor.addItems(DataType.asList())
		self.columnTypeInfoLayout.addWidget(self.columnTypeEditor)
		
		self.columnEditorLayout.addLayout(self.columnTypeInfoLayout)
		
	def tableColumns(self):
		self.columnInfo()
		
		self.addColumnButton = QPushButton("Add column")
		self.addColumnButton.clicked.connect(self.addColumn)
		self.columnEditorLayout.addWidget(self.addColumnButton)
		self.mainLayout.addLayout(self.columnEditorLayout)
		
		
	def create(self):
		#TODO check is valid table
		self.close()
	
	def tableCreate(self):
		self.createButton = QPushButton("Create")
		self.createButton.clicked.connect(self.create)
		self.mainLayout.addWidget(self.createButton)
		
	def initUI(self):
		self.mainLayout = QVBoxLayout()
		
		self.tableName()
		self.tablePreview()
		self.tableColumns()
		self.tableCreate()
		
		self.setLayout(self.mainLayout)