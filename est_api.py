import unittest
from enhancer.api import enhance_image
from PIL import Image
import os

class TestEnhancer(unittest.TestCase):
    def setUp(self):
        self.input_image = "test_image.jpg"
        self.output_image = "enhanced_image.jpg"
        img = Image.new("RGB", (100, 100), color="blue")
        img.save(self.input_image)

    def tearDown(self):
        if os.path.exists(self.input_image):
            os.remove(self.input_image)
        if os.path.exists(self.output_image):
            os.remove(self.output_image)

    def test_enhance_image(self):
        enhance_image(self.input_image, self.output_image)
        self.assertTrue(os.path.exists(self.output_image))

if __name__ == "__main__":
    unittest.main()
