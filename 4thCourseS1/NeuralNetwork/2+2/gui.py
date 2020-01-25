import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from neuralnetwork import *

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
from keras.models import load_model
import random

def scale_image(image,old_w,old_h,new_w,new_h):
    res = []
    x_ratio = old_w/new_w
    y_ratio = old_h/new_h
    for y in range(new_h):
        row = []
        for x in range(new_w):
            row.append(image[int(y*y_ratio)][int(x*x_ratio)])
        res.append(row)
    return res

class BBox:
    def __init__(self):
        self.minx = float("inf")
        self.miny = float("inf")
        self.maxx = float("-inf")
        self.maxy = float("-inf")
        
    def addPoint(self, point):
        if type(point) is QPoint:
            point = [point.x(),point.y()]
        self.minx = min(self.minx, point[0])
        self.miny = min(self.miny, point[1])
        self.maxx = max(self.maxx, point[0])
        self.maxy = max(self.maxy, point[1])
        
        
class MainWidget(QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        
        self.initBrush()
        self.initPaintingCanvas()
        self.initPlotCanvas()
        self.initLayouts()
        
        self.items = []
        self.currItem = []
        self.currbbox = BBox()
        
        self.perceptron = Perceptron([784,30,10])
        self.perceptron.load("digit_recognition_coefs.txt")
        
        self.convolution = load_model("digit_recognition.nn")
        
    def initPlotCanvas(self):
        self.perceptronLabel = QLabel("")
        self.perceptronLabel.setAlignment(Qt.AlignVCenter)
        self.perceptronLabel.setStyleSheet("font: 25pt Comic Sans MS")
        self.convolutionLabel = QLabel("")
        self.convolutionLabel.setAlignment(Qt.AlignVCenter)
        self.convolutionLabel.setStyleSheet("font: 25pt Comic Sans MS")
        
        self.figure = plt.figure()
        self.plot = self.figure.add_subplot()
        self.plotCanvas = FigureCanvas(self.figure)
    
    def initPaintingCanvas(self):
        self.drawing = False
        self.paintingCanvas = QLabel()
        self.paintingCanvas.mousePressEvent = self.mousePressEvent
        self.paintingCanvas.mouseMoveEvent = self.mouseMoveEvent
        self.paintingCanvas.mouseReleaseEvent = self.mouseReleaseEvent
        
        self.image = QPixmap(800,600)
        self.image.fill(Qt.white)
        self.paintingCanvas.setPixmap(self.image)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()
            self.currItem = [self.lastPoint]
 
    def mouseMoveEvent(self, event):
        if(event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.paintingCanvas.pixmap())
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            painter.end()
            self.lastPoint = event.pos()
            self.currItem.append(self.lastPoint)
            self.update()
            
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False
            bbox = BBox()
            for point in self.currItem:
                bbox.addPoint(point)
            bbox.minx -= 15
            bbox.miny -= 15
            bbox.maxx += 15
            bbox.maxy += 15
            file = str(len(self.items)) + ".png"
            width = bbox.maxx - bbox.minx
            height = bbox.maxy - bbox.miny
            pixmap = QPixmap(width,height)
            pixmap.fill(Qt.white)
            for i in range(1,len(self.currItem)):
                painter = QPainter(pixmap)
                painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                painter.drawLine(QPoint(self.currItem[i].x() - bbox.minx,self.currItem[i].y() - bbox.miny), QPoint(self.currItem[i-1].x() - bbox.minx,self.currItem[i-1].y() - bbox.miny))
                painter.end()
            self.update()
            image = pixmap.toImage()
            bits = image.bits()
            bits.setsize(width*height*4)
            arr = np.frombuffer(bits, np.uint8).reshape((height, width,4))
            bitmask = []
            for row in arr:
                maskrow = []
                for pixel in row:
                    maskrow.append(0.0 if pixel[0] > 0 or pixel[1] > 0 or pixel[2] > 0 else 1.0)
                bitmask.append(maskrow)
            
            new_width = 28
            new_height = 28
            
            bitmask = scale_image(bitmask,width,height,new_width,new_height)
            self.figure.canvas.flush_events()
            self.plot.imshow(bitmask,cmap='gray')
            self.figure.canvas.draw()
            #print(np.array(bitmask))
            input = np.reshape(np.array(bitmask),(1,784))
            perceptron_prediction = self.perceptron.predict(input)
            convolution_prediction = self.convolution.predict(np.reshape(bitmask,(1,28,28,1)))
            self.perceptronLabel.setText("Perceptron prediction: "+str(np.argmax(perceptron_prediction)))
            self.convolutionLabel.setText("Convolution prediction: "+str(np.argmax(convolution_prediction)))
            self.items.append(self.currItem)
            
    def undo(self):
        if len(self.items) > 0:
            self.items.pop()
        
        self.image = QPixmap(800,600)
        self.image.fill(Qt.white)
        self.paintingCanvas.setPixmap(self.image)
        for item in self.items:
            for i in range(1,len(item)):
                painter = QPainter(self.paintingCanvas.pixmap())
                painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                painter.drawLine(item[i], item[i-1])
                painter.end()
        
        
    def initBrush(self):
        self.brushSize = 2
        self.brushColor = Qt.black
        self.lastPoint = QPoint()
        
        
    def threePixel(self):
        self.brushSize = 3
 
    def fivePixel(self):
        self.brushSize = 5
 
    def sevenPixel(self):
        self.brushSize = 7
 
    def ninePixel(self):
        self.brushSize = 9
 
 
    def blackColor(self):
        self.brushColor = Qt.black
 
    def whiteColor(self):
        self.brushColor = Qt.white
 
    def redColor(self):
        self.brushColor = Qt.red
 
    def greenColor(self):
        self.brushColor = Qt.green
 
    def yellowColor(self):
        self.brushColor = Qt.yellow

        
    def initLayouts(self):
        self.mainLayout = QHBoxLayout()
        
        self.mainLayout.addWidget(self.paintingCanvas)
        
        self.plotCanvasLayout = QVBoxLayout()
        self.responseLayout = QVBoxLayout()
        self.responseLayout.addWidget(self.perceptronLabel)
        self.responseLayout.addWidget(self.convolutionLabel)
        self.plotCanvasLayout.addLayout(self.responseLayout)
        self.plotCanvasLayout.addWidget(self.plotCanvas)
        self.mainLayout.addLayout(self.plotCanvasLayout)
        
        self.setLayout(self.mainLayout)

class Window(QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        
        self.setWindowTitle("2+2")
        self.setGeometry(100, 100, 800, 600)
        
        self.mainWidget = MainWidget()
        self.setCentralWidget(self.mainWidget)
        
        self.initMenuBar()
        
        
    def clear(self):
        self.image.fill(Qt.white)
        self.update()    
        
        
    def initMenuBar(self):
        mainMenu = self.menuBar()
        
        fileMenu = mainMenu.addMenu("File")
        
        saveAction = QAction( "Save",self)
        saveAction.setShortcut("Ctrl+S")
        fileMenu.addAction(saveAction)
 
        clearAction = QAction( "Clear", self)
        clearAction.setShortcut("Ctrl+C")
        fileMenu.addAction(clearAction)
        clearAction.triggered.connect(self.clear)
        
        undoAction = QAction("Undo", self)
        undoAction.setShortcut("Ctrl+Z")
        fileMenu.addAction(undoAction)
        undoAction.triggered.connect(self.mainWidget.undo)
        
        brushSize = mainMenu.addMenu("Brush Size")
        
        threepxAction = QAction(  "3px", self)
        brushSize.addAction(threepxAction)
        threepxAction.triggered.connect(self.mainWidget.threePixel)
 
        fivepxAction = QAction( "5px", self)
        brushSize.addAction(fivepxAction)
        fivepxAction.triggered.connect(self.mainWidget.fivePixel)
 
        sevenpxAction = QAction("7px", self)
        brushSize.addAction(sevenpxAction)
        sevenpxAction.triggered.connect(self.mainWidget.sevenPixel)
 
        ninepxAction = QAction("9px", self)
        brushSize.addAction(ninepxAction)
        ninepxAction.triggered.connect(self.mainWidget.ninePixel)        
        
        brushColor = mainMenu.addMenu("Brush Color")
 
        blackAction = QAction( "Black", self)
        blackAction.setShortcut("Ctrl+B")
        brushColor.addAction(blackAction)
        blackAction.triggered.connect(self.mainWidget.blackColor)
 
        whitekAction = QAction( "White", self)
        whitekAction.setShortcut("Ctrl+W")
        brushColor.addAction(whitekAction)
        whitekAction.triggered.connect(self.mainWidget.whiteColor)
 
        redAction = QAction( "Red", self)
        redAction.setShortcut("Ctrl+R")
        brushColor.addAction(redAction)
        redAction.triggered.connect(self.mainWidget.redColor)
 
        greenAction = QAction( "Green", self)
        greenAction.setShortcut("Ctrl+G")
        brushColor.addAction(greenAction)
        greenAction.triggered.connect(self.mainWidget.greenColor)
 
        yellowAction = QAction( "Yellow", self)
        yellowAction.setShortcut("Ctrl+Y")
        brushColor.addAction(yellowAction)
        yellowAction.triggered.connect(self.mainWidget.yellowColor)

        

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())