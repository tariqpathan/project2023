from pathlib import Path
import os
import cv2
import pytesseract
import numpy as np

dir_path = Path(__file__).parent
file_location = "temp-q-2.jpg"
img_path = os.path.join(dir_path, file_location)

print(img_path)

img = cv2.imread(img_path)

# Convert the image to gray scale
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Use thresholding
_, thresh = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY_INV)

# Adaptive Thresholding
# thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

# Otsu's Thresholding
# _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)


# Resize the image
# resized = cv2.resize(thresh, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
# kernel = np.ones((3,3),np.uint8)
# eroded = cv2.erode(thresh, kernel, iterations = 2)
# dilated = cv2.dilate(thresh, kernel, iterations = 2)

text = pytesseract.image_to_string(thresh, config='--psm 7')

# cv2.imshow('CV2 Image', eroded)
# cv2.waitKey(2000)
# cv2.destroyAllWindows()
# text = pytesseract.image_to_string(eroded)
# text2 = pytesseract.image_to_string(dilated)

print(f'eroded: {text}, dilated:')