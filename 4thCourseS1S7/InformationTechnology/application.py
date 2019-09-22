from databasecontroller import *
from dbcreate import *

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Application(QWidget):
	def __init__(self):
		super().__init__()
		self.title = "SuperMegaHit"
		self.left = 50
		self.top = 50
		self.width = 800
		self.height = 600
		
		self.initControllers()
		self.initActions()
		self.initPalettes()
		self.initUI()
	
	#Palettes Themes
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
	
	#Actions
	def newDB(self):
		self.dbController = DataBaseController()
		self.createWindow = CreateDBWindow(self.dbController)
		self.createWindow.setPalette(self.palette())
		self.createWindow.show()
		
	def initNewDBAction(self):
		self.new_db_action = QAction("New")
		self.new_db_action.triggered.connect(self.newDB)
	
	def save(self):
		pass
		
	def initSaveAction(self):
		self.save_action = QAction("Save")
		self.save_action.triggered.connect(self.save)
		
	def open(self):
		pass
	
	def initOpenAction(self):
		self.open_action = QAction("Open")	
		self.open_action.triggered.connect(self.open)
	
	def initExitAction(self):
		self.exit_action = QAction("Exit")
		self.exit_action.triggered.connect(qApp.quit)
		
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
		self.initExitAction()
		self.initChangeThemeAction()
		
	#UI
	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		
		self.initLayouts()
		
		self.initMenuBar()
	
		self.table_layout.addWidget(self.dbController.tabWidget)
		
	def initLayouts(self):
		self.main_layout = QGridLayout()
		
		
		self.table_layout = QVBoxLayout()
		self.main_layout.addLayout(self.table_layout,1,0)
		
		self.setLayout(self.main_layout)
	
	#Controllers
	def initControllers(self):
		self.dbController = DataBaseController()
	
	#Menu
	def initMenuBar(self):
		self.menubar = QMenuBar()
		self.main_layout.addWidget(self.menubar, 0, 0)
		
		actionFile = self.menubar.addMenu("File")
		actionFile.addAction(self.new_db_action)
		actionFile.addAction(self.open_action)
		actionFile.addAction(self.save_action)
		actionFile.addSeparator()
		actionFile.addAction(self.exit_action)
		
		actionChangeTheme = self.menubar.addAction(self.change_theme_action)
	
if __name__ == '__main__':
	_ = QApplication([])
	_.setStyle("Fusion")
	app = Application()
	app.show()
	_.exec_()
 