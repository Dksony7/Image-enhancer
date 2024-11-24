import os
import cv2
import torch
from basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer

# Model weights URL
MODEL_URL = 'https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth'

# Download weights if not already available
if not os.path.exists('weights/RealESRGAN_x4plus.pth'):
    os.makedirs('weights', exist_ok=True)
    os.system(f'wget {MODEL_URL} -P ./weights')

def enhance_image(input_path, output_path, scale=4):
    """Enhance an image using Real-ESRGAN."""
    model = RRDBNet(num_in_ch=3, num_out_ch=3, nf=64, nb=23, gc=32, sf=scale)
    model_path = 'weights/RealESRGAN_x4plus.pth'

    if not os.path.exists(model_path):
        raise FileNotFoundError("Model weights not found. Ensure RealESRGAN_x4plus.pth is available.")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    upsampler = RealESRGANer(scale=scale, model=model, model_path=model_path, device=device)

    # Read input image
    img = cv2.imread(input_path, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Input image could not be read")

    # Enhance the image
    output, _ = upsampler.enhance(img, outscale=scale)

    # Save the output
    cv2.imwrite(output_path, output)
  
