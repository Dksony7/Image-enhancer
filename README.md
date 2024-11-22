# Image Enhancer
A simple Python package and API for enhancing images using Pillow.

## Features
- Brightness and sharpness enhancement.
- Easy-to-use Flask API.

## Installation
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.

## Usage
### As a Python Library
```python
from enhancer.api import enhance_image

enhance_image("input.jpg", "output.jpg")
