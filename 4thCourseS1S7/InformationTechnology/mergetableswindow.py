from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class MergeTablesWindow(QWidget):
    def __init__(self, tables):
        super().__init__()

        self.setWindowTitle("Merge tables")

        self.setGeometry(100, 100, 400, 400)

        self.tables = tables
        self.initUI()

    def initUI(self):
        self.mainLayout = QVBoxLayout()
        self.checkBoxList = []

        for table in self.tables:
            self.checkBoxList.append(QCheckBox(table))
            self.mainLayout.addWidget(self.checkBoxList[-1])

        self.newNameLayout = QHBoxLayout()
        self.newNameLabel = QLabel("New table name:")
        self.newNameEdit = QLineEdit()
        self.newNameLayout.addWidget(self.newNameLabel)
        self.newNameLayout.addWidget(self.newNameEdit)
        self.mainLayout.addLayout(self.newNameLayout)

        self.mergeButton = QPushButton("Merge")
        self.mergeButton.clicked.connect(self.close)
        self.mainLayout.addWidget(self.mergeButton)

        self.setLayout(self.mainLayout)
