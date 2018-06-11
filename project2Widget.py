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
        

class project2Widget(QWidget):
    def __init__(self, processor, parent=None):
        super(project2Widget, self).__init__(parent=parent)
        self.processor = processor
        self.imageViewer = imageViewerWidget()
        self.LabelEdge = QLabel('Edge Detection: ')
        self.LabelDenoising = QLabel('Denoising: ')
        self.btnRobert = QPushButton('Robert')
        self.btnPrewitt = QPushButton('Prewitt')
        self.btnSobel = QPushButton('Sobel')
        self.btnGaussian = QPushButton('Gaussian (kernel=0.5)')
        self.btnMedian = QPushButton('Median (footprint=3*3)')
        vbox = QVBoxLayout()
        vbox.addWidget(self.imageViewer)
        hbox = QHBoxLayout()
        hbox.addWidget(self.LabelEdge)
        hbox.addWidget(self.btnRobert)
        hbox.addWidget(self.btnPrewitt)
        hbox.addWidget(self.btnSobel)
        vbox.addLayout(hbox)
        hbox = QHBoxLayout()
        hbox.addWidget(self.LabelDenoising)
        hbox.addWidget(self.btnGaussian)
        hbox.addWidget(self.btnMedian)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.btnRobert.clicked.connect(lambda \
                p=self.processor, v=self.imageViewer: v.setImage(\
                (255*roberts(processor.getImage())).astype(np.uint8)))
        self.btnPrewitt.clicked.connect(lambda \
                p=self.processor, v=self.imageViewer: v.setImage(\
                (255*prewitt(processor.getImage())).astype(np.uint8)))
        self.btnSobel.clicked.connect(lambda \
                p=self.processor, v=self.imageViewer: v.setImage(\
                (255*sobel(processor.getImage())).astype(np.uint8)))
        self.btnGaussian.clicked.connect(lambda \
                p=self.processor, v=self.imageViewer: \
                v.setImage(filters.gaussian_filter( \
                processor.getImage(), sigma=0.5)))
        self.btnMedian.clicked.connect(lambda \
                p=self.processor, v=self.imageViewer: \
                v.setImage(filters.median_filter( \
                processor.getImage(), footprint=np.ones((3,3)))))


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
