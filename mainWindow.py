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

from imageViewerWidget import imageViewerWidget
from histWidget import histWidget
from imageProcessor import binaryImage as processor

        

class project1Widget(QWidget):
    def __init__(self, processor, parent=None):
        super(project1Widget, self).__init__(parent=parent)
        self.processor = processor()
        self.histViewer = histWidget()
        #self.imageViewer = imageViewerWidget()
        #self.imageViewer
        

# center widget
class basicImageWidget(QWidget):
    pass


class mainWindow(QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        
if __name__ == '__main__':
    imgPath = 'pics/lenna.png'
    if len(sys.argv) > 1:
        imgPath = sys.argv[1]
    app = QApplication(sys.argv)
    mainWindow = mainWindow()
    mainWindow.actLoadImage(imgPath)
    sys.exit(app.exec_())
