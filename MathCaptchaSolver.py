import cv2
import numpy as np
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import re

# Initialize the processor and model for image-to-text
processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-printed")
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-printed")

class CaptchaSolver:
    def __init__(self, image_np):
        self.image = image_np
        self.kernel = np.ones((2, 2), np.uint8)

    def enhance_legibility(self, cropped_image):
        gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        return cv2.erode(cv2.blur(mask, (2, 2)), self.kernel, iterations=1)

    def math_operation(self, left_number, right_number, operation='+'):
        if isinstance(left_number, int) and isinstance(right_number, int):
            return eval(f"{left_number} {operation} {right_number}")
        else:
            return None

    def math_operation_for_both_signs(self, left_number, right_number):
        if isinstance(left_number, int) and isinstance(right_number, int):
            return left_number + right_number
        else:
            return None

    def numpy_to_pil(self, numpy_array):
        return Image.fromarray(cv2.cvtColor(numpy_array, cv2.COLOR_BGR2RGB))

    def resolve(self, left_image, right_image, sign_image):
        def get_text_from_image(image):
            pixel_values = processor(images=image, return_tensors="pt").pixel_values
            generated_ids = model.generate(pixel_values)
            return processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

        sign = get_text_from_image(self.numpy_to_pil(sign_image))
        left_number = get_text_from_image(self.numpy_to_pil(left_image))

        def convert_to_number(string):
            if isinstance(string, str):
                string = re.sub('[^A-Za-z0-9 ]+', '', string.replace('-', "").replace("Z", "7").replace("%", "6").replace("&", "8").replace("'", "").replace('/', "").replace(':', '1').replace('S', '5').replace('s', '5'))
                return int(string) if string.isnumeric() else None
            else:
                return string

        left_number = convert_to_number(left_number)
        print('left_number:', left_number)

        if sign in {'+', '@', '4', '*'}:
            print('sign:', sign)
            right_number = get_text_from_image(self.numpy_to_pil(right_image))
            right_number = convert_to_number(right_number)
            print('right_number:', right_number)
            return self.math_operation(left_number, right_number)
        else:
            unfixed_right_number = ''.join(char for char in get_text_from_image(self.numpy_to_pil(right_image)) if isinstance(char, int))
            print('right_number:', unfixed_right_number)
            return self.math_operation_for_both_signs(left_number, unfixed_right_number)

    def solve_captcha(self):
        positions = {'left': 5, 'right': 52, 'sign': 33}
        dimensions = {'width': 25, 'width_sign': 15, 'width_right': 14}
        left_image = self.image[7:27, positions['left']:positions['left'] + dimensions['width']]
        right_image = self.image[6:24, positions['right']:positions['right'] + dimensions['width_right']]
        sign_image = self.image[10:25, positions['sign']:positions['sign'] + dimensions['width_sign']]

        left_enhanced = self.enhance_legibility(left_image)
        right_enhanced = self.enhance_legibility(right_image)

        return self.resolve(left_enhanced, right_enhanced, sign_image)

