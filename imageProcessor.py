#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import cv2 as cv
import scipy
import scipy.ndimage
import scipy.ndimage.morphology
import skimage
import skimage.morphology

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
        assert image.ndim == 2, 'greyscale image only'
        assert image.dtype == np.uint8, 'uint8 pixel type only'

    # set current image
    def setImage(self, image):
        print('image set')
        if (self.__image is not None) and np.array_equal(self.__image, image):
            return
        self.__checkImage(image)
        self.__reset()
        self.__image = image
        print('image emited!')
        self.imageChanged.emit()

    # get current image
    def getImage(self):
        assert self.__image is not None, 'image unset'
        return self.__image.copy()

    # read image from file
    def loadImage(self, imgPath):
        image = cv.imread(imgPath, cv.IMREAD_GRAYSCALE) # greyscale, uint8 img
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
        print('threshold emited!')
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
            _, self.__binaryImage = \
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

class imageProcessor(binaryImage):
    def __init__(self):
        super(imageProcessor, self).__init__()
        self.__skeleton = None
        self.__distance = None

    def __reset(self):
        self.__skeleton = None
        self.__distance = None

    def reset(self):
        super(imageProcessorImage, self).reset()
        self.__reset()

    def binary_dilation(self, *args, **kwargs):
        image = self.getBinImage()
        out = scipy.ndimage.morphology.binary_dilation(\
                image, *args, **kwargs)
        return (out*255).astype(np.uint8)

    def binary_erosion(self, *args, **kwargs):
        image = self.getBinImage()
        out = scipy.ndimage.morphology.binary_erosion(\
                image, *args, **kwargs)
        return (out*255).astype(np.uint8)

    def binary_opening(self, *args, **kwargs):
        image = self.getBinImage()
        out = scipy.ndimage.morphology.binary_opening(\
                image, *args, **kwargs)
        return (out*255).astype(np.uint8)

    def binary_closing(self, *args, **kwargs):
        image = self.getBinImage()
        out = scipy.ndimage.morphology.binary_closing(\
                image, *args, **kwargs)
        return (out*255).astype(np.uint8)

    def grey_dilation(self, *args, **kwargs):
        image = self.getImage()
        out = scipy.ndimage.morphology.grey_dilation(\
                image, *args, **kwargs)
        return out

    def grey_erosion(self, *args, **kwargs):
        image = self.getImage()
        return scipy.ndimage.morphology.grey_erosion(\
                image, *args, **kwargs)

    def grey_opening(self, *args, **kwargs):
        image = self.getImage()
        return scipy.ndimage.morphology.grey_opening(\
                image, *args, **kwargs)

    def grey_closing(self, *args, **kwargs):
        image = self.getImage()
        return scipy.ndimage.morphology.grey_closing(\
                image, *args, **kwargs)
        
    def perform_medial_axis(self):
        image = self.getBinImage()
        skeleton, dist = skimage.morphology.medial_axis(\
                image, return_distance=True)
        self.__distance = dist
        self.__skeleton = skeleton

    def distance(self):
        if self.__distance is None:
            self.perform_medial_axis()
        if self.__distance.max() > 255:
            return (self.__distance/ \
                    float(self.__distance.max())).astype(np.uint8)
        else:
            return self.__distance.astype(np.uint8)

    def skeletonize(self):
        if self.__skeleton is None:
            self.perform_medial_axis()
        return (255*self.__skeleton).astype(np.uint8)

    def restoration(self):
        assert self.__skeleton is not None
        assert self.__distance is not None
        return (255*skimage.morphology.reconstruction( \
                self.__skeleton, self.__distance)).astype(np.uint8)

    def morphological_edge(self):
        return self.binary_dilation() - self.binary_erosion()

    def morphological_gradient(self):
        return self.grey_dilation(size=(3,3)) - self.grey_erosion(size=(3,3))

    def conditional_dilation(self):
        mask = self.getBinImage()
        marker = self.binary_opening()
        while True:
            print('conditonal dialtion loop')
            T = marker.copy()
            marker = scipy.ndimage.morphology.binary_dilation(marker)
            marker = marker*mask
            marker = (255*(marker > 0)).astype(np.uint8)
            if np.array_equal(T, marker):
                print('conditonal dialtion done')
                return marker
            

if __name__ == '__main__':
    import sys, os
    from PyQt5.QtWidgets import QApplication, QWidget
    imgPath = 'pics/Lenna.png'
    if len(sys.argv) > 1:
        imgPath = sys.argv[1]
    processor = imageProcessor()
    processor.loadImage(imgPath)

    app = QApplication(sys.argv)
    ex = QWidget()
    ex.setGeometry(300, 300, 600, 600)
    ex.show()
    sys.exit(app.exec_())
