from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Image(QLabel):
    editingFinished = pyqtSignal()

    def __init__(self,path=""):
        QWidget.__init__(self)
        self.picture = QPixmap()
        self.path = path

    def setPath(self, path):
        self.picture = QPixmap(path)
        self.setPixmap(self.picture)
        self.editingFinished.emit()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.picture)
