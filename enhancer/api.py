from PIL import Image, ImageEnhance, ImageFilter
import os

def enhance_image(input_path, output_path, brightness_factor=1.2, contrast_factor=1.2, sharpness_factor=1.1, smoothness_level=2):
    """
    Enhance brightness, contrast, and sharpness while adding smoothness to the image.
    
    Args:
        input_path (str): Path to the input image.
        output_path (str): Path to save the enhanced image.
        brightness_factor (float): Brightness enhancement factor.
        contrast_factor (float): Contrast enhancement factor.
        sharpness_factor (float): Sharpness enhancement factor.
        smoothness_level (int): Level of smoothness (1 = light, 2 = moderate, 3 = strong).
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file {input_path} not found.")
    
    # Open the image
    with Image.open(input_path) as img:
        # Enhance brightness
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(brightness_factor)

        # Enhance contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(contrast_factor)

        # Enhance sharpness
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(sharpness_factor)

        # Add smoothness (apply multiple passes for stronger smoothness)
        for _ in range(smoothness_level):
            img = img.filter(ImageFilter.SMOOTH_MORE)

        # Save the enhanced image
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img.save(output_path, "JPEG")
        
