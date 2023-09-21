# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 18:09:42 2023

@author: SHAMIKA
"""

import cv2
import numpy as np


def CannyFeatures(img):
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply Canny edge detection with thresholds of 100 and 320
    edges = cv2.Canny(gray, 150, 320)
    
    # Calculate the mean, standard deviation, skewness and kurtosis of the edge image
    mean, std_dev = cv2.meanStdDev(edges)
    skewness = np.mean((edges - mean)**3) / std_dev**3
    kurtosis = np.mean((edges - mean)**4) / std_dev**4
    

# =============================================================================
#     print("mean: ", mean[0])
#     print("std_dev: ", std_dev[0])
#     print("skewness: ", skewness[0])
#     print("kurtosis: ", kurtosis[0])
# =============================================================================


    return([mean[0], std_dev[0], skewness[0], kurtosis[0]])