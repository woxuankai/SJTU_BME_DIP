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
        

class project4Widget(QWidget):
    def __init__(self, processor, parent=None):
        super(project4Widget, self).__init__(parent=parent)
        self.processor = processor
        self.imageViewer = imageViewerWidget()
        self.btnDilation = QPushButton('Dilation')
        self.btnErosion = QPushButton('Erosion')
        self.btnOpening = QPushButton('Opening')
        self.btnClosing = QPushButton('Closing')
        self.btnEdge = QPushButton('Morphological edge detection')
        self.btnMorphologicalGradient = QPushButton('Morphological gradient')
        self.btnRestoration = QPushButton('Morphological Reconstruction')
        self.btnConditionalDilation = QPushButton('Conditional dilation')
        #self.btnGreyscaleReconstruction = \
        #        QPushButton('Gray scale Reconstruction')
        vbox = QVBoxLayout()
        vbox.addWidget(self.imageViewer)
        hbox = QHBoxLayout()
        hbox.addWidget(self.btnDilation)
        hbox.addWidget(self.btnErosion)
        hbox.addWidget(self.btnOpening)
        hbox.addWidget(self.btnClosing)
        vbox.addLayout(hbox)
        hbox = QHBoxLayout()
        hbox.addWidget(self.btnEdge)
        hbox.addWidget(self.btnMorphologicalGradient)
        vbox.addLayout(hbox)
        hbox = QHBoxLayout()
        hbox.addWidget(self.btnConditionalDilation)
        hbox.addWidget(self.btnRestoration)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.btnDilation.clicked.connect(lambda x, \
                p=self.processor, v=self.imageViewer: \
                v.setImage(p.grey_dilation(size=(3,3))))
        self.btnErosion.clicked.connect(lambda x,\
                p=self.processor, v=self.imageViewer: \
                v.setImage(p.grey_erosion(size=(3,3))))
        self.btnOpening.clicked.connect(lambda x,\
                p=self.processor, v=self.imageViewer: \
                v.setImage(p.grey_opening(size=(3,3))))
        self.btnClosing.clicked.connect(lambda x,\
                p=self.processor, v=self.imageViewer: \
                v.setImage(p.grey_closing(size=(3,3))))
        self.btnEdge.clicked.connect(lambda x,\
                p=self.processor, v=self.imageViewer: \
                v.setImage(p.morphological_edge()))
        self.btnMorphologicalGradient.clicked.connect(lambda x,\
                p=self.processor, v=self.imageViewer: \
                v.setImage(p.morphological_gradient()))
        self.btnRestoration.clicked.connect(lambda x,\
                p=self.processor, v=self.imageViewer: \
                v.setImage(p.greyscale_reconstruction()))
        self.btnConditionalDilation.clicked.connect(lambda x,\
                p=self.processor, v=self.imageViewer: \
                v.setImage(p.conditional_dilation()))
        #self.btnGreyscaleReconstruction.clicked.connect(lambda x,\
        #        p=self.processor, v=self.imageViewer: \
        #        v.setImage(p.skeletonize()))


if __name__ == '__main__':
    import sys, os
    from PyQt5.QtWidgets import QApplication
    from imageProcessor import imageProcessor
    imgPath = 'pics/Lenna.png'
    if len(sys.argv) > 1:
        imgPath = sys.argv[1]
    processor = imageProcessor()

    app = QApplication(sys.argv)
    ex = project4Widget(processor)
    ex.setGeometry(300, 300, 600, 600)
    ex.show()
    processor.loadImage(imgPath)
    processor.setThreshold(128)
    sys.exit(app.exec_())
