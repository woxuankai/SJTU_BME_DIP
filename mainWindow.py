#!/usr/bin/python3

import os,sys

from PyQt5.QtWidgets import QGridLayout, \
        QDesktopWidget, QMainWindow, QApplication, qApp, \
        QDockWidget, QWidget, QAction, QTableWidget, QTableWidgetItem, \
        QMenu, QPushButton, \
        QVBoxLayout, QHBoxLayout, \
        QFileDialog, QMessageBox, QDialog
from PyQt5.QtCore import Qt, pyqtSlot, QSize

from imageProcessor import processor
from project1Widget import project1Widget

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