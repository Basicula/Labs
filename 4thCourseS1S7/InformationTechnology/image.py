from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Image(QLabel):
	editingFinished = pyqtSignal()

	def __init__(self):
		QWidget.__init__(self)
		self.picture = QPixmap("default.bmp")

	def setPath(self, path):
		self.picture = QPixmap(path)
	
	def paintEvent(self, event):
		painter = QPainter(self)
		painter.drawPixmap(0, 0, self.picture)