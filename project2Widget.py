#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, \
        QHBoxLayout, QVBoxLayout, QSizePolicy 
from PyQt5.QtCore import Qt, pyqtSlot, QPoint


from imageViewerWidget import imageViewerWidget
from histWidget import histWidget
        

class project2Widget(QWidget):
    def __init__(self, processor, parent=None):
        super(project2Widget, self).__init__(parent=parent)


if __name__ == '__main__':
    import sys, os
    from PyQt5.QtWidgets import QApplication
    from imageProcessor import binaryImage
    imgPath = 'pics/Lenna.png'
    if len(sys.argv) > 1:
        imgPath = sys.argv[1]
    processor = binaryImage()

    app = QApplication(sys.argv)
    ex = project2Widget(processor)
    ex.setGeometry(300, 300, 600, 600)
    ex.show()
    processor.loadImage(imgPath)
    sys.exit(app.exec_())
