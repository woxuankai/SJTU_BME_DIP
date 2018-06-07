#!/usr/bin/python3

import numpy as np
import cv2 as cv

from .imageAlgos import thresholdOTSU, thresholdMaxEntropy

class basicImage(object):
    def __init__(self):
        super(basicImage, self).__init__()
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
        self.__checkImage(image)
        self.__reset()
        self.__image = image

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
        threshold = float(threshold)
        self.__reset()
        self.__threshold = threshold

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
        threshold = thresholdOSTU()
        return threshold

    def getEntropyThreshold(self):
        image = self.getImage()
        threshold = thresholdMaxEntropy()
        return threshold


