# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 17:55:30 2023

@author: SHAMIKA
"""

import cv2
import numpy as np

def LaplacianTextureFeatures(img):
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Compute the Laplacian of the grayscale image
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    
    # Compute the standard deviation of the Laplacian
    std_dev = np.std(laplacian)
    
    # Compute the mean of the Laplacian
    mean = np.mean(laplacian)
    
    # Compute the roughness feature
    roughness = std_dev / mean
    
    # Compute the smoothness feature
    smoothness = 1.0 / roughness
    
    # Compute the coarseness feature
    coarseness = np.max(gray) - np.min(gray)
    
    # Compute the regularity feature
    reg = cv2.Laplacian(gray, cv2.CV_64F).var()
    
    # Compute the contrast feature
    contrast = np.mean(cv2.absdiff(gray, cv2.blur(gray, (3,3))))
    
    # Compute the homogeneity feature
    homo = np.mean(1.0 / (1.0 + cv2.absdiff(gray, cv2.blur(gray, (3,3)))))
    
    # Compute the entropy feature
    hist = cv2.calcHist([gray],[0],None,[256],[0,256])
    hist /= np.sum(hist)
    entropy = -np.sum(hist * np.log2(hist + 1e-9))
    
    # Compute the energy feature
    energy = np.sum(np.square(gray))
    
    # Compute the correlation feature
    corr = np.corrcoef(gray.reshape(-1), cv2.blur(gray, (3,3)).reshape(-1))[0,1]
    
    # Compute the directionality feature
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    dir = np.arctan2(np.abs(sobel_y), np.abs(sobel_x)).mean()
    
    # Compute the fractal dimension feature
    fractal = cv2.Laplacian(gray, cv2.CV_64F).var() / (gray.var() ** 2)

# =============================================================================
#     print("Roughness: ", roughness)
#     print("Smoothness: ", smoothness)
#     print("Coarseness: ", coarseness)
#     print("Regularity: ", reg)
#     print("Contrast: ", contrast)
#     print("Homogeneity: ", homo)
#     print("Entropy: ", entropy)
#     print("Energy: ", energy)
#     print("Correlation: ", corr)
#     print("Directionality: ", dir)
#     print("Fractal dimension: ", fractal)
# =============================================================================
    
    return([
        roughness,
        smoothness,
        coarseness,
        reg,
        contrast,
        homo,
        entropy,
        energy,
        corr,
        dir,
        fractal
        ])