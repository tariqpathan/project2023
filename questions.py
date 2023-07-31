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


"""get the start and end coords"""

height_coords = []
for i in range(len(pixel_values) - 1):
    height_coords.append(
        (pixel_values[i] - 10, pixel_values[i + 1] - 10)
    )

print(height_coords)


def crop_questions(image, coordinates: list[tuple]):
    questions = []
    # image = Image.open(image)
    for (start, end) in coordinates:
        question = image.crop((0, start, image.width, end))
        questions.append(question)
    return questions

def remove_excess_whitespace(images: list):
    out = []
    for image in images:
        mask = image.point(lambda p: p < 128)
        bbox = mask.getbbox()
        if bbox: image.crop(bbox)
        out.append(image)
    return out


out = crop_questions(image, height_coords)
for i in out: print(i.height)
out2 = remove_excess_whitespace(out)
for i in out2: print(i.height)


