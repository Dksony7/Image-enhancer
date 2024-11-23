from PIL import Image, ImageEnhance, ImageFilter
import os

def enhance_image(input_path, output_path, brightness_factor=1.2, contrast_factor=1.2, sharpness_factor=1.2):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file {input_path} not found.")
    
    # Open the image
    with Image.open(input_path) as img:
        # Enhance brightness
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(brightness_factor)

        # Enhance contrast (adjust here)
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(contrast_factor)

        # Enhance sharpness
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(sharpness_factor)

        # Optional: Reduce noise using a filter
        img = img.filter(ImageFilter.SMOOTH)

        # Save the enhanced image
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img.save(output_path, "JPEG")
        
