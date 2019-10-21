from tablecreate import *
from databasecontroller import *

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class CreateDBWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create new data base")

        self.setGeometry(100, 100, 400, 400)

        self.dbController = DataBaseController()

        self.initUI()

    def initUI(self):
        self.mainLayout = QVBoxLayout()

        self.nameEditLayout = QHBoxLayout()
        self.nameLabel = QLabel("Database name:")
        self.nameEditLayout.addWidget(self.nameLabel)
        self.nameEdit = QLineEdit()
        self.nameEdit.textChanged.connect(self.changeTableName)
        self.nameEditLayout.addWidget(self.nameEdit)
        self.mainLayout.addLayout(self.nameEditLayout)

        self.tableListLayout = QVBoxLayout()
        self.tableListLayout.addWidget(self.dbController.tabWidget)
        self.mainLayout.addLayout(self.tableListLayout)

        self.buttonsLayout = QHBoxLayout()
        self.addTableButton = QPushButton("Add table")
        self.addTableButton.clicked.connect(self.addTable)
        self.buttonsLayout.addWidget(self.addTableButton)
        self.createButton = QPushButton("Create")
        self.createButton.clicked.connect(self.create)
        self.buttonsLayout.addWidget(self.createButton)
        self.mainLayout.addLayout(self.buttonsLayout)

        self.setLayout(self.mainLayout)
        
    def changeTableName(self):
        self.dbController.changeName(self.nameEdit.text())

    def create(self):
        self.close()

    def addTable(self):
        self.addTableWindow = TableCreateWindow()
        self.addTableWindow.setPalette(self.palette())
        self.addTableWindow.createButton.clicked.connect(
            lambda _: self.dbController.addTable(self.addTableWindow.tableController.table))
        self.addTableWindow.show()
