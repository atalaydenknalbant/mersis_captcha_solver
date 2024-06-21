import unittest
import cv2
import numpy as np
from MathCaptchaSolver import CaptchaSolver

class TestCaptchaSolver(unittest.TestCase):
    def setUp(self):
        # Path to the sample captcha image
        self.image_path = "captcha.png"
        self.image = cv2.imread(self.image_path)
        if self.image is None:
            raise ValueError(f"Image not found or unable to read image at path: {self.image_path}")
        self.captcha_image_np = np.array(self.image)

    @unittest.skipUnless(cv2.imread("captcha.png") is not None, "Sample captcha image not found")
    def test_solve_captcha(self):
        solver = CaptchaSolver(self.captcha_image_np)
        result = solver.solve_captcha()
        print("Captcha result:", result)
        self.assertIsInstance(result, int)
    

if __name__ == '__main__':
    unittest.main()
