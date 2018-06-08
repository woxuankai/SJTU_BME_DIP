#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np

# reference: https://github.com/scikit-image/scikit-image/blob/master/skimage/filters/thresholding.py

def thresholdOTSU(image, nbins=256):
    assert image.ndim == 2, 'supports 2D gray image only'
    hist, bin_centers = np.histogram(image.ravel(), nbins)
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
    return threshold

def thresholdMaxEntropy(image, nbins=256):
    assert image.ndim == 2, 'supports 2D gray image only'
    hist, bin_centers = np.histogram(image.ravel(), nbins, density=True)
    Hb = - np.cumsum(hist[:-1] * np.log2(hist[:-1]))# leng: bins - 1
    Hw = - np.cumsum(hist[1::-1] * np.log2(hist[1::-1])) # len: bins - 1
    H = Hb + Hw
    idx = np.argmax(H)
    threshold = bin_centers[:-1][idx]
    return threshold


