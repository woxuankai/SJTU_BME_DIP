#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QSlider, QLabel, \
        QHBoxLayout, QVBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSlot, QPoint



from imageViewerWidget import imageViewerWidget



        

class project1Widget(QWidget):
    def __init__(self, processor, parent=None):
        super(project1Widget, self).__init__(parent=parent)
        self.processor = processor
        self.histViewer = Figure()
        self.imageViewer = imageViewerWidget()
