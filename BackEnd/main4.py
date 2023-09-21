# -*- coding: utf-8 -*-


from rembg import remove
from PIL import Image
import numpy as np
import cv2
import joblib


from Features.LaplacianFeatures import LaplacianTextureFeatures
from Features.ShapeFeatures import ImageShapeFeatures
from Features.CannyFeatures import CannyFeatures


def prediction_03(filename):

    img_path='static/images/'+filename
    image = Image.open(img_path).convert("RGB")

    image_data = np.array(image)
    output_data = remove(image_data)

    output_data_lap = cv2.cvtColor(output_data, cv2.COLOR_BGRA2BGR)

    laplacean_features = LaplacianTextureFeatures(output_data_lap)
    shape_features = ImageShapeFeatures(output_data)
    canny_features = CannyFeatures(output_data_lap)

# Prepare the features for prediction
    test_features = [
        shape_features[0],
        shape_features[1],
        shape_features[2],
        shape_features[3],
        shape_features[4],
        shape_features[5],
        shape_features[6],
        shape_features[7],
        laplacean_features[0],
        laplacean_features[1],
        laplacean_features[2],
        laplacean_features[3],
        laplacean_features[4],
        laplacean_features[5],
        laplacean_features[6],
        laplacean_features[7],
        laplacean_features[8],
        laplacean_features[9],
        laplacean_features[10],
        canny_features[0][0],
        canny_features[1][0],
        canny_features[2][0],
        canny_features[3][0],
        ]


    loaded_rf_classifier = joblib.load('model/rf_classifier.pkl')

    rf_prediction = loaded_rf_classifier.predict([test_features])

    print("Random Forest Prediction:", rf_prediction)

    return rf_prediction

