#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os,sys

from PyQt5.QtWidgets import QGridLayout, \
        QDesktopWidget, QMainWindow, QApplication, qApp, \
        QDockWidget, QWidget, QAction, QTableWidget, QTableWidgetItem, \
        QMenu, QPushButton, \
        QVBoxLayout, QHBoxLayout, \
        QFileDialog, QMessageBox, QDialog
from PyQt5.QtCore import Qt, pyqtSlot, QSize

from PyQt5.QtWidgets import QWidget, QSlider, QLabel, \
        QHBoxLayout, QVBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSlot, QPoint

from imageProcessor import imageProcessor
from imageViewerWidget import imageViewerWidget
from project1Widget import project1Widget
from project2Widget import project2Widget
from project3Widget import project3Widget
from project4Widget import project4Widget


class biImageViewerWidget(imageViewerWidget):
    def __init__(self, processor, parent=None):
        super(biImageViewerWidget, self).__init__(parent)
        self.processor = imageProcessor()
        self.grayViewer = imageViewerWidget()
        self.binaryViewer = imageViewerWidget()
        vbox = QVBoxLayout()
        vbox.addWidget(self.grayViewer)
        vbox.addWidget(self.binaryViewer)
        self.setLayout(vbox)
        # signals
        self.processor.imageChanged.connect(lambda \
                p = self.processor, gv = self.grayViewer: \
                gv.setImage(p.getImage()))
        self.processor.imageChanged.connect(lambda \
                bv = self.binaryViewer: \
                bv.reset())
        self.processor.thresholdChanged.connect(lambda value, \
                p = self.processor, bv = self.binaryViewer: \
                gv.setImage(p.getBinaryImage()))


class mainWindow(QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        self.processor = imageProcessor()
        self.imageViewer = biImageViewerWidget(self.processor, None)
        self.setCentralWidget(self.imageViewer)
        self.project1 = project1Widget(self.processor, None)
        self.dockProject1 = QDockWidget("Project 1", self)
        self.dockProject1.setObjectName("dock Project 1")
        self.addDockWidget(Qt.RightDockWidgetArea, self.dockProject1)
        self.dockProject1.setWidget(self.project1)
        self.project2 = project2Widget(self.processor, None)
        self.dockProject2 = QDockWidget("Project 2", self)
        self.dockProject2.setObjectName("dock Project 2")
        self.addDockWidget(Qt.RightDockWidgetArea, self.dockProject2)
        self.dockProject2.setWidget(self.project2)
        self.project3 = project3Widget(self.processor, None)
        self.dockProject3 = QDockWidget("Project 3", self)
        self.dockProject3.setObjectName("dock Project 3")
        self.addDockWidget(Qt.RightDockWidgetArea, self.dockProject3)
        self.dockProject3.setWidget(self.project3)
        self.project4 = project4Widget(self.processor, None)
        self.dockProject4 = QDockWidget("Project 4", self)
        self.dockProject4.setObjectName("dock Project 4")
        self.addDockWidget(Qt.RightDockWidgetArea, self.dockProject4)
        self.dockProject4.setWidget(self.project4)
        self.tabifyDockWidget(self.dockProject1, self.dockProject2)
        self.tabifyDockWidget(self.dockProject2, self.dockProject3)
        self.tabifyDockWidget(self.dockProject3, self.dockProject4)
        
if __name__ == '__main__':
    imgPath = 'pics/Lenna.png'
    if len(sys.argv) > 1:
        imgPath = sys.argv[1]
    app = QApplication(sys.argv)
    mainWindow = mainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
