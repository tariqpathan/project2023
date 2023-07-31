from PIL import Image
import numpy as np

THRESHOLD_VALUE = 180  # Adjust this value based on the image characteristics and number clarity
X_MARGIN = 180
image = Image.open('test-page2.jpg')

# what do i have to do?
# 'read' the margin and get coords
# split the images according to the y-coords/height
# save the image section and tag it with the appropriate metadata

grayscale_image = image.convert('L')
print(grayscale_image.mode)

binary_image = grayscale_image.point(lambda x: 0 if x < THRESHOLD_VALUE else 255, "1")

# binary_image.show()
print(binary_image.height, binary_image.width)
img_height = binary_image.height - 120

cropped = binary_image.crop((0, 0, X_MARGIN , img_height))
cropped_array = np.array(cropped)


""" 
Here we get the heights for the question markers
The top of the question is given in the pixel_values array
"""
non_white_pixels = []
pixel_values = []
for index, row in enumerate(cropped_array):
    if len(set(row)) != 1:
        non_white_pixels.append(index)
        if index - 1 not in non_white_pixels:
            pixel_values.append(index)
        

print(non_white_pixels)
print(pixel_values)
