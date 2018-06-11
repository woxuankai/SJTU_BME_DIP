#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QSizePolicy
from PyQt5.QtCore import pyqtSignal

import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
import matplotlib.backends.backend_qt5agg.FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class histWidget(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure()
        super(histWidget, self).__init__(self.fig)
        self.setParent(parent)
        self.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.__hist = None
        self.__value = None
        self.valueChanged = pyqtSignal(float)
        self.mpl_connect('button_press_event',  self.__onMousePress)        
    
    def __drawLine(self, value):
        pass
    
    def __drawHist(self, hist):
        pass
    
    def __setValue(self, value):
        # draw line here
        pass
    
    def __setHist(self, image):
        pass
 
    def __onMousePress(self, event):
        print('you pressed', event.button, event.xdata, event.ydata)
        self.__setValue(self, event.xdata)
    
    def setValue(self, value):
        self.__setValue(value)
        self.valueChanged.emit(value)
    
    def setHist(self, image):
        self.__setHist(image)
    
 if __name__ == '__main__':
    import sys, os
    from PyQt5.QtWidgets import QApplication
    from imageProcessor import basicImage
    imgPath = 'pics/lenna.png'
    if len(sys.argv) > 1:
        imgPath = sys.argv[1]
    processor = basicImage()
    processor.loadImage(imgPath)
    image = processor.getImage()

    app = QApplication(sys.argv)
    ex = imageViewerWidget()
    ex.setGeometry(300, 300, 600, 600)
    ex.setImage(image)
    ex.show()
    sys.exit(app.exec_())
