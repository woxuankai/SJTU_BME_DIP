#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QSizePolicy

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
    
    def setValue(self, value):
        passx
    
    def setImage(self, image):
        pass
    
    @pyqtSlot(int)
    def slotValueChanged(self, index):
        self.labelIndex.setText(str(index)+'/'+str(self.sliderIndex.maximum()))