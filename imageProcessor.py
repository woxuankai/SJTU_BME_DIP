#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import cv2 as cv

from PyQt5.QtCore import pyqtSignal, QObject

from imageAlgos import thresholdOTSU, thresholdMaxEntropy

class basicImage(QObject):
    imageChanged = pyqtSignal()
    def __init__(self, parent=None):
        super(basicImage, self).__init__(parent)
        self.__image = None

    # reset only variables define in current class
    def __reset(self):
        self.__image = None

    # reset all
    def reset(self):
        self.__reset()
    

    @staticmethod
    def __checkImage(image):
        assert image is not None, 'empty image'
        assert isinstance(image, np.ndarray), 'image should be numpy array'
        assert image.ndim == 2, 'grayscale image only'
        assert image.dtype == np.uint8, 'uint8 pixel type only'

    # set current image
    def setImage(self, image):
        if (self.__image is not None) and (self.__image == image):
            return
        self.__checkImage(image)
        self.__reset()
        self.__image = image
        self.imageChanged.emit()

    # get current image
    def getImage(self):
        assert self.__image is not None, 'image unset'
        return self.__image.copy()

    # read image from file
    def loadImage(self, imgPath):
        image = cv.imread(imgPath, cv.IMREAD_GRAYSCALE) # grayscale, uint8 img
        self.setImage(image)

    # save image to file
    def saveImage(self,  imgPath):
        image = self.getImage()
        cv.imwrite(imgPath, image)


class binaryImage(basicImage):
    thresholdChanged = pyqtSignal(float)
    def __init__(self):
        super(binaryImage, self).__init__()
        self.__threshold = None
        self.__binaryImage = None

    def __reset(self):
        self.__threshold = None
        self.__binaryImage = None

    def reset(self):
        super(binaryImage, self).reset()
        self.__reset()

    # get current thresholding
    def setThreshold(self, threshold):
        print('set threshold to '+str(threshold))
        eps = 1e-5
        threshold = float(threshold)
        if (self.__threshold is not None) and \
                (abs(threshold - self.__threshold) < eps):
            return
        self.__reset()
        self.__threshold = threshold
        self.thresholdChanged.emit(threshold)

    # get current thresholding
    def getThreshold(self):
        assert self.__threshold is not None, 'threshold unset'
        return self.__threshold

    # get binary image
    def getBinImage(self):
        if self.__binaryImage is not None:
            return self.__binaryImage
        else:
            image = self.getImage()
            threshold = self.getThreshold()
            maxval = 255 #uint8 max
            self.__binaryImage = \
                    cv.threshold(image, threshold, maxval, cv.THRESH_BINARY)
            return self.__binaryImage.copy()

    def getOtsuThreshold(self):
        image = self.getImage()
        threshold = thresholdOTSU(image)
        return threshold

    def getEntropyThreshold(self):
        image = self.getImage()
        threshold = thresholdMaxEntropy(image)
        return threshold

if __name__ == '__main__':
    import sys, os
    from PyQt5.QtWidgets import QApplication, QWidget
    from imageProcessor import binaryImage
    imgPath = 'pics/Lenna.png'
    if len(sys.argv) > 1:
        imgPath = sys.argv[1]
    processor = binaryImage()
    processor.loadImage(imgPath)

    app = QApplication(sys.argv)
    ex = QWidget()
    ex.setGeometry(300, 300, 600, 600)
    ex.show()
    sys.exit(app.exec_())
