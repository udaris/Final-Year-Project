# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 23:01:51 2023

@author: Udari
"""

import cv2
import numpy as np
import joblib
from skimage.feature import graycomatrix, graycoprops
from skimage.filters import gabor
from scipy.stats import skew, kurtosis
from PIL import Image
import csv
from werkzeug.utils import secure_filename

# Define a function to extract features from an image
def extract_features(img):
    # Define feature vectors to store the extracted features
    glcm_features = np.zeros((1, 5))
    gabor_features = np.zeros((1, 12))
    histogram_features = np.zeros((1, 256))
    moments_features = np.zeros((1, 8))

    # Compute GLCM features
    glcm = graycomatrix(img, distances=[1], angles=[0], levels=256, symmetric=True, normed=True)
    glcm_features[0, 0] = graycoprops(glcm, 'dissimilarity')[0, 0]
    glcm_features[0, 1] = graycoprops(glcm, 'correlation')[0, 0]
    glcm_features[0, 2] = graycoprops(glcm, 'energy')[0, 0]
    glcm_features[0, 3] = graycoprops(glcm, 'homogeneity')[0, 0]
    glcm_features[0, 4] = graycoprops(glcm, 'ASM')[0, 0]

    # Compute Gabor filter features
    for i, theta in enumerate([0, np.pi/4, np.pi/2, 3*np.pi/4]):
        for j, frequency in enumerate([0.1, 0.2, 0.3]):
            real, imag = gabor(img, frequency=frequency, theta=theta)
            magnitude = np.sqrt(real**2 + imag**2)
            gabor_features[0, i*3+j] = magnitude.mean()

    # Compute histogram features
    histogram_features[0] = cv2.calcHist([img], [0], None, [256], [0, 256]).flatten()

    # Compute moments features
    moments = cv2.moments(img)
    hu_moments = cv2.HuMoments(moments).flatten()
    hu_moments = hu_moments[:6] # truncate to 6 elements
    moments_features[0, 0] = skew(img.flatten())
    moments_features[0, 1] = kurtosis(img.flatten())
    moments_features[0, 2:] = hu_moments


    # Concatenate all the feature vectors into a single feature vector
    features = np.concatenate((glcm_features, gabor_features, histogram_features, moments_features), axis=1)

    return features

def getPrediction(filename):
    # Load the trained model
    model = joblib.load('model/rfmodel.joblib')
    
    # Load and preprocess the input image
    #image=cv2.imread('input/Ranawara_26.jpg')
    #img_path='static/images/'+filename
    img_path = 'static/images/' + secure_filename(filename)
    image=np.asarray(Image.open(img_path))
    resized_image = cv2.resize(image, (256, 256))

    # Apply color transformation to remove noise
    image_rgb=cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
    #converts images rgb_images to gray
    gray_image= cv2.cvtColor(image_rgb,cv2.COLOR_RGB2GRAY)
    #to normalized
    normalized_img= cv2.normalize(gray_image, None, 0, 255, cv2.NORM_MINMAX)
    #to apply meddian filter
    blurred_img=cv2.medianBlur(normalized_img, 3)
    #to increase contrast
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    preprocessed_img = clahe.apply(blurred_img)

    # Extract features from the input image
    # Use the same feature extraction technique that you used during training
    features= extract_features(preprocessed_img)

    # Predict the class label of the new input plant leaf image
    predicted_class = model.predict(features)
    predicted_class = str(predicted_class[0])
    # Print the predicted class
    print(f"Predicted class: {predicted_class}")
    
    return predicted_class



def getPlantDetails(predicted_class):
    with open('FinalLableSetwithusage.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Local Name'] == predicted_class:
                return row

    return None


