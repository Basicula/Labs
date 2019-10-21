from table import *

import json


class DataBase:
    def __init__(self, name=""):
        self.tables = []
        self.name = name

    def newTable(self, name):
        newTable = Table(name)
        self.tables.append(newTable)

    def addTable(self, table):
        if type(table) is Table:
            self.tables.append(table)
        else:
            raise Exception("Given table is not a Table object")
            
    def getTable(self,name):
        for table in self.tables:
            print("blabla",name,table.name)
            if table.name == name:
                return table
        return None
            
    def mergeTables(self,table_names,new_name=""):
        if new_name == "":
            new_name = ' + '.join(table_names)
        new_table = Table(new_name)
        pre_row = []
        k = 0
        for i in range(len(self.tables)):
            table = self.tables[i-k]
            if table.name in table_names:
                table_names.remove(table.name)
                rows = []
                for row in table.rows:
                    rw = pre_row.copy()
                    for cell in row:
                        rw.append(cell)
                    rows.append(rw)
                for column in table.columns:
                    new_table.addColumn(column)
                    for row in new_table.rows:
                        row.append(Cell("",column.type))
                    pre_row.append(Cell("",column.type))
                for row in rows:
                    new_table.addRow(row)
                self.tables.remove(table)
                k+=1
        self.addTable(new_table)
        return new_table

    @property
    def __dict__(self):
        return {
            'name': self.name,
            'tables': self.tables
        }

    @staticmethod
    def fromDict(dict):
        db = DataBase(dict['name'])
        for table in dict['tables']:
            db.tables.append(Table.fromDict(table))
        return db
