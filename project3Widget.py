#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, \
        QHBoxLayout, QVBoxLayout, QSizePolicy 
from PyQt5.QtCore import Qt, pyqtSlot, QPoint

import numpy as np
from scipy.ndimage import filters
from skimage.filters import roberts, sobel, prewitt

from imageViewerWidget import imageViewerWidget
from histWidget import histWidget
        

class project3Widget(QWidget):
    def __init__(self, processor, parent=None):
        super(project3Widget, self).__init__(parent=parent)
        self.processor = processor
        self.imageViewer = imageViewerWidget()
        self.btnDilation = QPushButton('Dilation')
        self.btnErosion = QPushButton('Erosion')
        self.btnOpening = QPushButton('Opening')
        self.btnClosing = QPushButton('Closing')
        self.btnDistance = QPushButton('Distance Transform')
        self.btnSkeleton = QPushButton('Skeleton')
        self.btnRestoration = QPushButton('Restoration')
        vbox = QVBoxLayout()
        vbox.addWidget(self.imageViewer)
        hbox = QHBoxLayout()
        hbox.addWidget(self.btnDilation)
        hbox.addWidget(self.btnErosion)
        hbox.addWidget(self.btnOpening)
        hbox.addWidget(self.btnClosing)
        vbox.addLayout(hbox)
        hbox = QHBoxLayout()
        hbox.addWidget(self.btnDistance)
        hbox.addWidget(self.btnSkeleton)
        hbox.addWidget(self.btnRestoration)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.btnDilation.clicked.connect(lambda x, \
                p=self.processor, v=self.imageViewer: \
                v.setImage(p.binary_dilation()))
        self.btnErosion.clicked.connect(lambda x,\
                p=self.processor, v=self.imageViewer: \
                v.setImage(p.binary_erosion()))
        self.btnOpening.clicked.connect(lambda x,\
                p=self.processor, v=self.imageViewer: \
                v.setImage(p.binary_opening()))
        self.btnClosing.clicked.connect(lambda x,\
                p=self.processor, v=self.imageViewer: \
                v.setImage(p.binary_closing()))
        self.btnDistance.clicked.connect(lambda x,\
                p=self.processor, v=self.imageViewer: \
                v.setImage(p.distance()))
        self.btnSkeleton.clicked.connect(lambda x,\
                p=self.processor, v=self.imageViewer: \
                v.setImage(p.skeletonize()))
        self.btnRestoration.clicked.connect(lambda x,\
                p=self.processor, v=self.imageViewer: \
                v.setImage(p.restoration()))


if __name__ == '__main__':
    import sys, os
    from PyQt5.QtWidgets import QApplication
    from imageProcessor import imageProcessor
    imgPath = 'pics/Lenna.png'
    if len(sys.argv) > 1:
        imgPath = sys.argv[1]
    processor = imageProcessor()

    app = QApplication(sys.argv)
    ex = project3Widget(processor)
    ex.setGeometry(300, 300, 600, 600)
    ex.show()
    processor.loadImage(imgPath)
    processor.setThreshold(128)
    sys.exit(app.exec_())
