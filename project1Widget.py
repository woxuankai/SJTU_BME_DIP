#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, \
        QHBoxLayout, QVBoxLayout, QSizePolicy, \
        QFileDialog
from PyQt5.QtCore import Qt, pyqtSlot, QPoint


from imageViewerWidget import imageViewerWidget
from histWidget import histWidget

        

class project1Widget(QWidget):
    def __init__(self, processor, parent=None):
        super(project1Widget, self).__init__(parent=parent)
        # variables
        self.processor = processor
        # layout
        self.histViewer = histWidget()
        self.labelThreshold = QLabel('Threshold')
        self.editThreshold = QLineEdit()
        self.btnThreshold = QPushButton('Accept')
        self.btnOtsu = QPushButton('OTSU')
        self.btnEntropy = QPushButton('Entropy Method')
        self.btnOpen = QPushButton('Open Image')
        hbox = QHBoxLayout()
        hbox.addWidget(self.btnOtsu)
        hbox.addWidget(self.btnEntropy)
        hbox.addWidget(self.labelThreshold)
        hbox.addWidget(self.editThreshold)
        hbox.addWidget(self.btnThreshold)
        hbox.addWidget(self.btnOpen)
        vbox = QVBoxLayout()
        vbox.addWidget(self.histViewer)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        # connect inner signals
        #self.btnOtsu.clicked.connect(lambda \
        #        p=self.processor, e=self.editThreshold: \
        #        e.setText('{:}'.format(processor.getOtsuThreshold())))
        #self.btnEntropy.clicked.connect(lambda  \
        #        p=self.processor, e=self.editThreshold: \
        #        e.setText('{:}'.format(processor.getEntropyThreshold())))
        self.btnOtsu.clicked.connect(lambda \
                p=self.processor, h=self.histViewer: \
                h.setValue(processor.getOtsuThreshold()))
        self.btnEntropy.clicked.connect(lambda  \
                p=self.processor, h=self.histViewer: \
                h.setValue(processor.getEntropyThreshold()))
        #self.histViewer.valueChanged.connect(lambda value, \
        #        p=self.processor: \
        #        p.setThreshold(value))
        self.histViewer.valueChanged.connect(lambda value, \
                e=self.editThreshold: \
                e.setText('{:}'.format(value)))
        # connect outer signals
        self.btnThreshold.clicked.connect(lambda  \
                p=self.processor, e=self.editThreshold: \
                processor.setThreshold(float(e.text())))
        self.processor.thresholdChanged.connect(lambda value, \
                e=self.editThreshold:
                e.setText('{:}'.format(value)))
        self.processor.thresholdChanged.connect(lambda value, \
                h=self.histViewer:
                h.setValue(value))
        self.processor.imageChanged.connect(lambda \
                p=self.processor, h=self.histViewer:
                h.setImage(p.getImage()))

        self.btnOpen.clicked.connect(self.actLoadImage)

    def actLoadImage(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setViewMode(QFileDialog.Detail)
        #dialog.setOption(QFileDialog.ShowDirsOnly, True)
        if dialog.exec_():
            imgPath = str(dialog.selectedFiles()[0])
            self.processor.loadImage(imgPath)


if __name__ == '__main__':
    import sys, os
    from PyQt5.QtWidgets import QApplication
    from imageProcessor import binaryImage
    imgPath = 'pics/Lenna.png'
    if len(sys.argv) > 1:
        imgPath = sys.argv[1]
    processor = binaryImage()

    app = QApplication(sys.argv)
    ex = project1Widget(processor)
    ex.setGeometry(300, 300, 600, 600)
    ex.show()
    processor.loadImage(imgPath)
    sys.exit(app.exec_())
