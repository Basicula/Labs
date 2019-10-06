from database import *
from tablecontroller import *

from PyQt5.QtWidgets import QTabWidget, QTableWidget


class DataBaseController:
    def __init__(self):
        self.tabWidget = QTabWidget()
        self.tableControllers = []
        self.database = DataBase()

        self.tabWidget.currentChanged.connect(self.update)

    def changeName(self, name):
        self.database.name = name

    def addTable(self, table):
        self.database.addTable(table)
        self.tableControllers.append(TableController())
        self.tableControllers[-1].addTable(table)
        self.tabWidget.addTab(self.tableControllers[-1].tableWidget, table.name)
        self.tableControllers[-1].tableWidget.cellChanged.connect(self.update)
        
    def removeTable(self,table):
        for controller in self.tableControllers:
            if controller.table == table:
                self.tableControllers.remove(controller)
                return        

    def getTableNamesList(self):
        res = []
        for table in self.database.tables:
            res.append(table.name)
        return res

    def mergeTables(self, table_names,new_name=""):
        new_table = self.database.mergeTables(table_names.copy(),new_name)
        k = 0
        for i in range(len(self.tableControllers)):
            controller = self.tableControllers[i-k]
            if controller.table.name in table_names:
                controller.tableWidget.deleteLater()
                self.tableControllers.remove(controller)
                k+=1
        self.tableControllers.append(TableController())
        self.tableControllers[-1].addTable(new_table)
        self.tabWidget.addTab(self.tableControllers[-1].tableWidget, new_table.name)
        self.tableControllers[-1].tableWidget.cellChanged.connect(self.update)
        
    def update(self):
        for tbcontroller in self.tableControllers:
            tbcontroller.addEmptyRow()

    def saveDB(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.database, file, default=lambda o: o.__dict__, indent=4)

    def loadDB(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            self.database = DataBase.fromDict(data)
        self.tabWidget = QTabWidget()
        self.tableControllers = []
        for table in self.database.tables:
            self.tableControllers.append(TableController())
            self.tableControllers[-1].addTable(table)
            self.tableControllers[-1].addEmptyRow()
            self.tableControllers[-1].tableWidget.cellChanged.connect(self.update)
            self.tabWidget.addTab(self.tableControllers[-1].tableWidget, table.name)
        self.tabWidget.currentChanged.connect(self.update)
