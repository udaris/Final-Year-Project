# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 17:59:03 2023

@author: SHAMIKA
"""


from skimage import measure
from scipy.spatial import ConvexHull
import numpy as np
from PIL import Image

def ImageShapeFeatures(img):
    
    # Create a new PIL image from the output data
    output_image = Image.fromarray(img)
    
    # Resize the image to 256x256
    output_image = output_image.resize((256, 256))

    # Convert the output image to grayscale
    gray_image = output_image.convert('L')

    # Convert the grayscale image to a NumPy array
    gray_array = np.array(gray_image)

    # Find the contours
    contours = measure.find_contours(gray_array, 0.8)

    # Choose the longest contour
    contour = max(contours, key=len)

    # Calculate the maximum width and maximum length of the leaf
    max_width = np.max(contour[:, 1]) - np.min(contour[:, 1])
    max_length = np.max(contour[:, 0]) - np.min(contour[:, 0])

    # Calculate the convex area of the contour
    def calculate_convex_area(contour):
        n = len(contour)
        area = 0

        for i in range(n):
            x1, y1 = contour[i]
            x2, y2 = contour[(i + 1) % n]  # Connects the last point with the first point

            area += (x1 * y2 - x2 * y1)

        return abs(area) / 2

    convex_area = calculate_convex_area(contour)

    # Calculate shape slimness (F1)
    bonding_point = contour[0]  # Bonding point of leafstalk with leaf surface
    points_on_margin = contour[1:]  # Points on the leaf margin
    l1 = np.linalg.norm(points_on_margin - bonding_point, axis=1).max()
    vertical_line = np.array([bonding_point[0], bonding_point[1] + l1])  # Vertical line to l1
    l2 = np.linalg.norm(points_on_margin - vertical_line, axis=1).max()
    shape_slimness = l1 / l2

    # Calculate roundness (F2)
    perimeter = np.sum(np.sqrt(np.diff(contour[:, 0]) ** 2 + np.diff(contour[:, 1]) ** 2))
    roundness = (4 * np.pi * convex_area) / (perimeter ** 2)

    # Calculate the area of the contour
    moments = measure.moments(contour[:, ::-1])  # Reverse the order of coordinates
    area = moments[0, 0]

    # Calculate the convex hull area (F4)
    hull = ConvexHull(contour)
    convex_hull_area = hull.volume

    # Calculate solidity (F5)
    solidity = convex_area / convex_hull_area
    
# =============================================================================
#     print("Max width: ", max_width)
#     print("Max length: ", max_length)
#     print("Shape slimness: ", shape_slimness)
#     print("Roundness: ", roundness)
#     print("convex_area: ", convex_area)
#     print("convex_hull_area: ", convex_hull_area)
#     print("solidity: ", solidity)
# =============================================================================

    
    return([
        max_width, 
        max_length, 
        shape_slimness,
        roundness,
        area, 
        convex_area, 
        convex_hull_area, 
        solidity
        ])