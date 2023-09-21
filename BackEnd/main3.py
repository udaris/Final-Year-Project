from skimage.measure import regionprops_table
import cv2
import numpy as np
import joblib
from skimage.feature import graycomatrix, graycoprops
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
glcm_distance = 1
glcm_angles = [0, np.pi/4, np.pi/2, 3*np.pi/4]

def flatten_arrays(lst):
    flattened_lst = []
    for item in lst:
        if isinstance(item, np.ndarray):
            flattened_lst.extend(item.ravel())
        else:
            flattened_lst.append(item)
    return flattened_lst

def getPrediction_03(filename):
        svm = joblib.load('model/svm_model2.joblib')
        
        csv_file = 'model/features_final.csv'
        df = pd.read_csv(csv_file)
        
        # Separate features and labels
        X = df.drop('label', axis=1)
        y = df['label']

        # Perform feature scaling
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        # Apply PCA for dimensionality reduction
        pca = PCA(n_components=0.95)  # Retain 95% of the variance
        X_pca = pca.fit_transform(X_scaled)
        
        test_image_path='static/images/'+filename
        image = cv2.imread(test_image_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_image = cv2.resize(gray_image, (256, 256))
        label_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        # Extract features from the image
        glcm = graycomatrix(gray_image, distances=[glcm_distance], angles=glcm_angles, levels=256, symmetric=True, normed=True)
        glcm_features = graycoprops(glcm, prop='contrast').ravel().tolist()
        props = regionprops_table(label_image, gray_image, properties=['convex_area', 'area', 'eccentricity', 'extent', 'inertia_tensor', 'major_axis_length', 'minor_axis_length', 'perimeter', 'solidity', 'orientation', 'moments_central', 'moments_hu', 'euler_number', 'equivalent_diameter', 'mean_intensity', 'bbox'])
        props['perimeter_area_ratio'] = props['perimeter'] / props['area']
        color_features = cv2.mean(image)[:3]
        combined_features = glcm_features + list(props.values()) + list(color_features)
        print(combined_features)

        combined_features = flatten_arrays(combined_features)

        # Convert combined_features to a NumPy array
        combined_features = np.array(combined_features)

        # Perform feature scaling and dimensionality reduction
        scaled_features = scaler.transform([combined_features])
        pca_features = pca.transform(scaled_features)

        prediction = svm.predict(pca_features)[0]

        
        return prediction