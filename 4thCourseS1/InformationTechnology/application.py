from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from dbcreate import *
from mergetableswindow import *
from tablecreate import *

class Application(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "SuperMegaHit"
        self.left = 50
        self.top = 50
        self.width = 800
        self.height = 600

        self.initControllers(DataBaseController())
        self.initActions()
        self.initPalettes()
        self.initUI()

    # Palettes Themes
    def initPalettes(self):
        self.dark_palette = QPalette()
        self.dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        self.dark_palette.setColor(QPalette.WindowText, Qt.white)
        self.dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        self.dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        self.dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        self.dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        self.dark_palette.setColor(QPalette.Text, Qt.white)
        self.dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        self.dark_palette.setColor(QPalette.ButtonText, Qt.white)
        self.dark_palette.setColor(QPalette.BrightText, Qt.red)
        self.dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        self.dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        self.dark_palette.setColor(QPalette.HighlightedText, Qt.black)

        self.default_palette = QApplication.palette()

        self.current_palette = self.default_palette

        self.setPalette(self.current_palette)

    # Actions
    def updateDBView(self):
        self.table_layout.itemAt(0).widget().deleteLater()
        self.dbController.update()
        self.table_layout.addWidget(self.dbController.tabWidget)

    def newDB(self):
        self.dbController = DataBaseController()
        self.createWindow = CreateDBWindow()
        self.createWindow.setPalette(self.palette())
        self.createWindow.show()
        self.createWindow.createButton.clicked.connect(lambda _: self.initControllers(self.createWindow.dbController))
        self.createWindow.createButton.clicked.connect(self.updateDBView)

    def initNewDBAction(self):
        self.new_db_action = QAction("New")
        self.new_db_action.setShortcut("Ctrl+N")
        self.new_db_action.triggered.connect(self.newDB)

    def save(self):
        file = QFileDialog.getSaveFileName(self, 'Save data base', filter='*.json')
        if file[0]:
            self.dbController.saveDB(file[0])
        self.dbController = DataBaseController()
        self.updateDBView()

    def initSaveAction(self):
        self.save_action = QAction("Save")
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.triggered.connect(self.save)

    def open(self):
        self.dbController = DataBaseController()
        file = QFileDialog.getOpenFileName(self, 'Load data base', filter='*.json')
        if file[0]:
            self.dbController.loadDB(file[0])
        self.updateDBView()

    def initOpenAction(self):
        self.open_action = QAction("Open")
        self.open_action.setShortcut("Ctrl+O")
        self.open_action.triggered.connect(self.open)

    def delete(self):
        self.dbController = DataBaseController()
        self.updateDBView()

    def initDeleteAction(self):
        self.delete_action = QAction("Delete")
        self.delete_action.setShortcut("Ctrl+D")
        self.delete_action.triggered.connect(self.delete)

    def initExitAction(self):
        self.exit_action = QAction("Exit")
        self.exit_action.triggered.connect(qApp.quit)

    def addTable(self):
        self.addTableWindow = TableCreateWindow()
        self.addTableWindow.setPalette(self.palette())
        self.addTableWindow.createButton.clicked.connect(
            lambda _: self.dbController.addTable(self.addTableWindow.tableController.table))
        self.addTableWindow.show()

    def initAddTableAction(self):
        self.add_table_action = QAction("Add table")
        self.add_table_action.setShortcut("Ctrl+A")
        self.add_table_action.triggered.connect(self.addTable)

    def mergeTables(self):
        table_list = self.dbController.getTableNamesList()
        if len(table_list) == 0:
            return
        self.mergeTablesWindow = MergeTablesWindow(table_list)

        def getTablesForMerge():
            tables_for_merge = []
            new_name = self.mergeTablesWindow.newNameEdit.text()
            for checkBox in self.mergeTablesWindow.checkBoxList:
                if checkBox.checkState():
                    tables_for_merge.append(checkBox.text())
            self.dbController.mergeTables(tables_for_merge)

        self.mergeTablesWindow.show()
        self.mergeTablesWindow.mergeButton.clicked.connect(getTablesForMerge)

    def initMergeTablesAction(self):
        self.merge_tables_action = QAction("Merge tables")
        self.merge_tables_action.setShortcut("Ctrl+M")
        self.merge_tables_action.triggered.connect(self.mergeTables)

    def changeTheme(self):
        if self.current_palette == self.default_palette:
            self.current_palette = self.dark_palette
        else:
            self.current_palette = self.default_palette
        self.setPalette(self.current_palette)

    def initChangeThemeAction(self):
        self.change_theme_action = QAction("Change Theme")
        self.change_theme_action.triggered.connect(self.changeTheme)

    def initActions(self):
        self.initNewDBAction()
        self.initSaveAction()
        self.initOpenAction()
        self.initDeleteAction()
        self.initExitAction()

        self.initAddTableAction()
        self.initMergeTablesAction()

        self.initChangeThemeAction()

    # Controllers
    def initControllers(self, dbController):
        self.dbController = dbController

    # UI
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.initLayouts()

        self.initMenuBar()

        self.table_layout.addWidget(self.dbController.tabWidget)

    def initLayouts(self):
        self.main_layout = QGridLayout()

        self.table_layout = QVBoxLayout()
        self.main_layout.addLayout(self.table_layout, 1, 0)

        self.setLayout(self.main_layout)

    # Menu
    def initMenuBar(self):
        self.menubar = QMenuBar()
        self.main_layout.addWidget(self.menubar, 0, 0)

        actionFile = self.menubar.addMenu("File")
        actionFile.addAction(self.new_db_action)
        actionFile.addAction(self.open_action)
        actionFile.addAction(self.save_action)
        actionFile.addAction(self.delete_action)
        actionFile.addSeparator()
        actionFile.addAction(self.exit_action)

        actionEdit = self.menubar.addMenu("Edit")
        actionEdit.addAction(self.add_table_action)
        actionEdit.addAction(self.merge_tables_action)

        self.menubar.addAction(self.change_theme_action)


if __name__ == '__main__':
    _ = QApplication([])
    _.setStyle("Fusion")
    app = Application()
    app.show()
    _.exec_()
