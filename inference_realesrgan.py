import os
import cv2
import torch
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer

# Google Drive file ID
FILE_ID = '18pE5kjR4XZJdxfpfAM2umP4IcdNbqtfP'
MODEL_PATH = 'weights/RealESRGAN_x4plus.pth'

# Download weights if not already available
if not os.path.exists(MODEL_PATH):
    os.makedirs('weights', exist_ok=True)
    # Use gdown to download from Google Drive
    os.system(f'gdown --id {FILE_ID} -O {MODEL_PATH}')

def enhance_image(input_path, output_path, scale=4):
    """Enhance an image using Real-ESRGAN."""
    model = RRDBNet(num_in_ch=3, num_out_ch=3, nf=64, nb=23, gc=32, sf=scale)
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Model weights not found. Ensure RealESRGAN_x4plus.pth is available.")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    upsampler = RealESRGANer(scale=scale, model=model, model_path=MODEL_PATH, device=device)

    # Read input image
    img = cv2.imread(input_path, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Input image could not be read")

    # Enhance the image
    output, _ = upsampler.enhance(img, outscale=scale)

    # Save the output
    cv2.imwrite(output_path, output)

