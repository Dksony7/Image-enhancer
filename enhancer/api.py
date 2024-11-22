from PIL import Image, ImageEnhance
import os

def enhance_image(input_path, output_path, enhancement_factor=1.5):
    """
    Enhance the brightness and sharpness of an image.
    Args:
        input_path (str): Path to the input image.
        output_path (str): Path to save the enhanced image.
        enhancement_factor (float): Factor for enhancement (default=1.5).
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file {input_path} not found.")
    
    # Open the image
    with Image.open(input_path) as img:
        # Enhance brightness
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(enhancement_factor)

        # Enhance sharpness
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(enhancement_factor)

        # Save the enhanced image
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img.save(output_path, "JPEG")
