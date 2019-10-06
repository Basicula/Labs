from tablecontroller import *

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class TableCreateWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Create table")

        self.setGeometry(200, 200, 400, 400)

        self.tableController = TableController()

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
        self.tableController.addColumnData(self.columnHeaderEditor.text(), self.columnTypeEditor.currentIndex())
        if self.columnTypeEditor.currentIndex() == 5:
            bottom = float("-inf")
            top = float("inf")
            if float(self.intervalBottomEditor.text()):
                bottom = float(self.intervalBottomEditor.text())
            if float(self.intervalTopEditor.text()):
                top = float(self.intervalTopEditor.text())
            if bottom < top:
                self.tableController.table.columns[-1].optionalInfo = ['interval', [bottom, top]]
        self.intervalBottomEditor.clear()
        self.intervalTopEditor.clear()
        self.columnHeaderEditor.clear()

    def updateIntervalInfo(self, type):
        visible = False
        if type == "RealInvl" or type == 5:
            visible = True
        self.intervalInfoLabel.setVisible(visible)
        self.intervalBottomLabel.setVisible(visible)
        self.intervalBottomEditor.setVisible(visible)
        self.intervalTopLabel.setVisible(visible)
        self.intervalTopEditor.setVisible(visible)

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
        self.columnTypeEditor.currentIndexChanged.connect(self.updateIntervalInfo)
        self.columnTypeInfoLayout.addWidget(self.columnTypeEditor)

        self.columnEditorLayout.addLayout(self.columnTypeInfoLayout)

        self.intervalInfoLayout = QVBoxLayout()
        self.intervalInfoLabel = QLabel("Real interval")
        self.intervalInfoLabel.setAlignment(Qt.AlignCenter)
        self.intervalInfoLabel.setVisible(False)
        self.intervalInfoLayout.addWidget(self.intervalInfoLabel)

        self.intervalBottomLayout = QHBoxLayout()
        self.intervalBottomLabel = QLabel("Bottom:")
        self.intervalBottomLabel.setVisible(False)
        self.intervalBottomLayout.addWidget(self.intervalBottomLabel)
        self.intervalBottomEditor = QLineEdit()
        self.intervalBottomEditor.setValidator(QDoubleValidator())
        self.intervalBottomEditor.setVisible(False)
        self.intervalBottomLayout.addWidget(self.intervalBottomEditor)
        self.intervalInfoLayout.addLayout(self.intervalBottomLayout)

        self.intervalTopLayout = QHBoxLayout()
        self.intervalTopLabel = QLabel("Top:")
        self.intervalTopLabel.setVisible(False)
        self.intervalTopLayout.addWidget(self.intervalTopLabel)
        self.intervalTopEditor = QLineEdit()
        self.intervalTopEditor.setValidator(QDoubleValidator())
        self.intervalTopEditor.setVisible(False)
        self.intervalTopLayout.addWidget(self.intervalTopEditor)
        self.intervalInfoLayout.addLayout(self.intervalTopLayout)

        self.columnEditorLayout.addLayout(self.intervalInfoLayout)

    def tableColumns(self):
        self.columnInfo()

        self.addColumnButton = QPushButton("Add column")
        self.addColumnButton.clicked.connect(self.addColumn)
        self.columnEditorLayout.addWidget(self.addColumnButton)
        self.mainLayout.addLayout(self.columnEditorLayout)

    def create(self):
        # TODO check is valid table
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
