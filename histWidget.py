#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QSizePolicy
from PyQt5.QtCore import pyqtSignal

import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

class histWidget(FigureCanvas):
    def __init__(self, parent=None):
        self.__fig = Figure()
        super(histWidget, self).__init__(self.__fig)
        self.__axes = self.__fig.subplots()
        self.__line = None
        self.setParent(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.valueChanged = pyqtSignal(float)
        self.mpl_connect('button_press_event',  self.__onMousePress)        
        self.__value = None
    
    def __drawLine(self, value):
        if self.__line is not None:
            self.__line.remove()
        ylim = self.__axes.get_ylim()
        self.__line = Line2D([value, value], ylim, color='red')
        #print('drawing ylim'+str(ylim))
        self.__axes.add_line(self.__line)
        self.draw()
        #self.draw_idle()
    
    def __drawHist(self, x):
        self.__axes.cla()
        return self.__axes.hist(x, density=True)
    
    def __onMousePress(self, event):
        #print('you pressed', event.button, event.xdata, event.ydata)
        xdata = event.xdata
        if xdata is not None:
            self.__drawLine(event.xdata)
    
    def setValue(self, value):
        self.__value = value
        self.__drawLine(value)
        self.valueChanged.emit(value)
    
    def setImage(self, image):
        self.__drawHist(image.ravel())
    
if __name__ == '__main__':
    import sys, os
    from PyQt5.QtWidgets import QApplication
    from imageProcessor import basicImage
    imgPath = 'pics/Lenna.png'
    if len(sys.argv) > 1:
        imgPath = sys.argv[1]
    processor = basicImage()
    processor.loadImage(imgPath)
    image = processor.getImage()

    app = QApplication(sys.argv)
    ex = histWidget()
    ex.setGeometry(300, 300, 600, 600)
    ex.setImage(image)
    ex.show()
    sys.exit(app.exec_())
