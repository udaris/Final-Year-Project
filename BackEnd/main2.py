import cv2
import numpy as np
import joblib
from skimage.feature import graycomatrix, graycoprops
from skimage.filters import gabor
from scipy.stats import skew, kurtosis
from PIL import Image
from skimage.feature import local_binary_pattern
import csv

def extract_color_features(hue, saturation, value):
    # Calculate color histogram features
    hist_hue = cv2.calcHist([hue], [0], None, [256], [0, 256])
    hist_saturation = cv2.calcHist([saturation], [0], None, [256], [0, 256])
    hist_value = cv2.calcHist([value], [0], None, [256], [0, 256])

    # Normalize the histograms
    hist_hue = cv2.normalize(hist_hue, hist_hue).flatten()
    hist_saturation = cv2.normalize(hist_saturation, hist_saturation).flatten()
    hist_value = cv2.normalize(hist_value, hist_value).flatten()

    # Concatenate the color histogram features
    color_features = np.concatenate((hist_hue, hist_saturation, hist_value))

    return color_features

def extract_texture_features(gray):
    # Calculate Local Binary Pattern (LBP) features
    lbp = local_binary_pattern(gray, 8, 1, method='uniform')
    hist_lbp, _ = np.histogram(lbp.ravel(), bins=256, range=(0, 256), density=True)

    # Calculate Gray-Level Co-occurrence Matrix (GLCM) features
    glcm = graycomatrix(gray, [1], [0], symmetric=True, normed=True)
    contrast = graycoprops(glcm, 'contrast')[0]
    energy = graycoprops(glcm, 'energy')[0]
    correlation = graycoprops(glcm, 'correlation')[0]

    # Concatenate the texture features
    texture_features = np.concatenate((hist_lbp, contrast, energy, correlation))

    return texture_features

def extract_shape_features(contours):
    # Calculate shape features based on contour properties
    shape_features = []
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        area = cv2.contourArea(contour)
        circularity = (4 * np.pi * area) / (perimeter ** 2)
        shape_features.append(circularity)

    return shape_features

def getPrediction2(filename):
    # Load the trained model
    model = joblib.load('model/SVMmodel.joblib')
    class_names = ['Araliya', 'Elabatu', 'Heenaraththa','Idda', 'Kaduru','Karavila','Kathurumurunga','Class 7','Samanpichcha','Sepalika','Binkohomba']  
    # Load and preprocess the input image
    img_path='static/images/'+filename
    image=np.asarray(Image.open(img_path))
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hue, saturation, value = cv2.split(hsv)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Perform thresholding or any other segmentation technique
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
    # Find contours in the binary image
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Extract color features
    color_features = extract_color_features(hue, saturation, value)
    # Extract texture features
    texture_features = extract_texture_features(gray)

    shape_features = extract_shape_features(contours)
    # Combine all features
    all_features = np.concatenate((color_features, texture_features, shape_features))
    all_features = np.reshape(all_features, (1, -1))
    predicted_class = model.predict(all_features)
    # Predict the class label of the new input plant leaf image
    # predicted_class = str(predicted_class[0])
    predicted_class = (predicted_class[0])
    predicted_class_index =  predicted_class 
    predicted_class = class_names[predicted_class_index]
    # Print the predicted class
    print(f"Predicted class: {predicted_class}")
    
    return predicted_class
