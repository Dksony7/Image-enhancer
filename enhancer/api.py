import cv2
import numpy as np
import os

def enhance_image(input_path, output_path):
    """
    Enhance the brightness and sharpness of an image using OpenCV.
    Args:
        input_path (str): Path to the input image.
        output_path (str): Path to save the enhanced image.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file {input_path} not found.")
    
    # Read the image
    img = cv2.imread(input_path)
    if img is None:
        raise ValueError("Invalid image file")

    # Enhance brightness
    brightness_factor = 1.2
    img = cv2.convertScaleAbs(img, alpha=brightness_factor, beta=30)

    # Apply sharpening filter
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    sharpened = cv2.filter2D(img, -1, kernel)

    # Save the enhanced image
    cv2.imwrite(output_path, sharpened)
    
