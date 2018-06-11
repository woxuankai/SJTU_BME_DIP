#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np

# reference: https://github.com/scikit-image/scikit-image/blob/master/skimage/filters/thresholding.py

def thresholdOTSU(image, nbins=256):
    assert image.ndim == 2, 'supports 2D gray image only'
    hist, bin_edges = np.histogram(image.ravel(), nbins)
    bin_centers = (bin_edges[:-1] + bin_edges[1:])/2
    hist = hist.astype(float)
    # class probabilities for all possible thresholds
    weight1 = np.cumsum(hist)
    weight2 = np.cumsum(hist[::-1])[::-1]
    # class means for all possible thresholds
    mean1 = np.cumsum(hist * bin_centers) / weight1
    mean2 = (np.cumsum((hist * bin_centers)[::-1]) / weight2[::-1])[::-1]
    
    variance12 = weight1[:-1] * weight2[1:] * (mean1[:-1] - mean2[1:]) ** 2

    idx = np.argmax(variance12)
    threshold = bin_centers[:-1][idx]
    #print(variance12)
    return threshold


from scipy.stats import entropy
def thresholdMaxEntropy(image, nbins=256):
    assert image.ndim == 2, 'supports 2D gray image only'
    hist, bin_edges = np.histogram(image.ravel(), nbins)
    #hist, bin_edges = np.histogram(image.ravel(), nbins, density=True)
    bin_centers = (bin_edges[:-1] + bin_edges[1:])/2
    #Hb = - np.exp(hist[:0:-1]*np.log(hist[:0:-1]))# leng: bins - 1
    #Hw = - np.exp(hist[1:]*np.log(hist[1:])) # len: bins - 1
    #Hb[np.isnan(Hb)] = 0
    #Hw[np.isnan(Hw)] = 0
    #Hb = np.cumsum(Hb)
    #Hw = np.cumsum(Hw)
    #H = Hb + Hw
    H=[]
    for i in range(nbins-1):
        e = entropy(hist[0:i+1]) + entropy(hist[i+1:])
        H.append(e)
    #print(H)
    idx = np.argmax(H)
    threshold = bin_centers[:-1][idx]
    return threshold

if __name__ == '__main__':
    import os, sys
    import cv2 as cv
    imgPath = 'pics/Lenna.png'
    if len(sys.argv) > 1:
        imgPath = sys.argv[1]
    image = cv.imread(imgPath, cv.IMREAD_GRAYSCALE) # grayscale, uint8 img
    print('OTSU: '+str(thresholdOTSU(image)))
    print('MaxEntropy: '+str(thresholdMaxEntropy(image)))
