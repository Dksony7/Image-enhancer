from PIL import Image
import os

def validate_image(file_path):
    """Check if the file is a valid image."""
    try:
        with Image.open(file_path) as img:
            img.verify()
        return True
    except Exception:
        return False

def save_image(img, output_path):
    """Save an image to the specified path."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "JPEG")
