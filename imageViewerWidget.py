#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QSlider, QLabel, QScrollArea, \
        QHBoxLayout, QVBoxLayout, QSizePolicy
from PyQt5.QtGui import QImage, QPixmap, QPalette
from PyQt5.QtCore import Qt, pyqtSlot, QPoint

import numpy as np

def array2Pixmap(array):
    assert (array.ndim==2) or (array.ndim==3 and array.shape[2]==3), \
            'Only 2D grayscale or bgr image is supported'
    assert array.dtype == np.uint8, 'Only uint8 pixel type is supported'
    if array.ndim == 2:
        array = np.stack([array, array, array], axis=-1)
    img = QImage(array.copy().data, \
            array.shape[1], array.shape[0], QImage.Format_RGB888)
    pixmap = QPixmap.fromImage(img)
    return pixmap

class scalableLabel(QScrollArea):
    scaleMin = 0.2
    scaleMax = 10
    wheelScale = 1/480.0
    def __init__(self, parent=None):
        super(scalableLabel, self).__init__(parent)
        self.imageLabel = QLabel(parent)
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.imageLabel.setScaledContents(True)

        self.setBackgroundRole(QPalette.Dark)
        self.setWidget(self.imageLabel)
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.__pixmap = None
        self.__scaleFactor = 1 # defalut scaleFactor
        self.__mouseLeftPressing = False
        self.__mouseLeftPos = QPoint(0,0)

    def setScale(self, scale):
        scale = np.clip(scale, self.scaleMin, self.scaleMax)
            
        if self.__pixmap is None:
            return
        self.__scaleFactor = scale
        scaledPixmap = self.__pixmap.scaled(self.__pixmap.size() * scale)
        self.imageLabel.setPixmap(scaledPixmap)
        self.imageLabel.adjustSize()

    def getScale(self):
        return self.__scaleFactor

    def setPixmap(self, pixmap):
        assert pixmap is not None
        self.__pixmap = pixmap
        scaledPixmap = self.__pixmap.scaled(\
                self.__pixmap.size() * self.__scaleFactor)
        self.imageLabel.setPixmap(scaledPixmap)
        self.imageLabel.adjustSize()

    def reset(self):
        self.__pixmap = None
        self.imageLabel.setText('Not Available')
        self.__scaleFactor = 1 # defalut scaleFactor

    def wheelEvent(self, event):
        self.setScale(self.getScale() + event.angleDelta().y()*self.wheelScale)

    def mousePressEvent(self, event):
        if (event.button() == Qt.LeftButton):
            self.__mouseLeftPressing = True
            self.__mouseLeftPressPos = event.pos()
        else:
            super(scalableLabel, self).mousePressEvent(event)
            
    def mouseMoveEvent(self, event):
        if self.__mouseLeftPressing and (event.buttons() & Qt.LeftButton):
            currentPos = event.pos()
            hScrollBar = self.horizontalScrollBar()
            vScrollBar = self.verticalScrollBar()
            delta = currentPos - self.__mouseLeftPressPos
            self.__mouseLeftPressPos = currentPos
            hScrollBar.setValue(hScrollBar.value() - delta.x())
            vScrollBar.setValue(vScrollBar.value() - delta.y())
        else:
            super(scalableLabel, self).mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        if (event.button() == Qt.LeftButton):
            self.__mouseLeftPressing = False
        else:
            super(scalableLabel, self).mouseReleaseEvent(event)

class imageViewerWidget(scalableLabel):
    def __init__(self, parent=None):
        super(imageViewerWidget, self).__init__(parent)

    def setImage(self, image):
        assert image.ndim == 2, "accepts 2D grayscale image only"
        pixmap = array2Pixmap(image)
        self.setPixmap(pixmap)

if __name__ == '__main__':
    import sys, os, time
    from PyQt5.QtWidgets import QApplication
    from imageProcessor import basicImage
    imgPath = 'pics/Lenna.png'
    if len(sys.argv) > 1:
        imgPath = sys.argv[1]
    processor = basicImage()
    processor.loadImage(imgPath)
    image = processor.getImage()

    app = QApplication(sys.argv)
    ex = imageViewerWidget()
    ex.setGeometry(300, 300, 600, 600)
    ex.show()
    ex.setImage(image)
    #ex.reset()
    sys.exit(app.exec_())

