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
    print(f'length of images  {len(images)}')
    out = []
    for image in images:
        out.append(remove_vertical_whitespace(image))
    return out

def remove_vertical_whitespace(i):
    image = get_grayscale_image(i)
    data = np.array(image)
    min_values = data.min(axis=1)
    
    # Find the first and last occurrence of a value less than the threshold
    non_white_rows = np.where(min_values < 128)[0]
    if non_white_rows.size == 0:
        print("No content detected in the image.")
        return

    top = non_white_rows[0]
    bottom = non_white_rows[-1]

    # Crop the image
    cropped = image.crop((0, top, image.width, bottom + 1))

    # Save the cropped image
    return cropped


def get_grayscale_image(image):
    if image.mode != 'L':
        image = image.convert('L')
    return image


out = crop_questions(image, height_coords)
for i in out: 
    print(i.height)
    # i.show()

out2 = remove_excess_whitespace(out)
print(f'length of out2: {len(out2)}')
for i in out2: 
    print(i.height)
    i.show()


