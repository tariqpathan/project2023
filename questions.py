from PIL import Image
import cv2
import pytesseract
import numpy as np

THRESHOLD_VALUE = 180  # Adjust this value based on the image characteristics and number clarity
X_MARGIN = 180
image = Image.open('test-page15.jpg')

# what do i have to do?
# 'read' the margin and get coords
# split the images according to the y-coords/height
# save the image section and tag it with the appropriate metadata

grayscale_image = image.convert('L')
# print(grayscale_image.mode)

binary_image = grayscale_image.point(lambda x: 0 if x < THRESHOLD_VALUE else 255, "1")

# binary_image.show()
print(binary_image.height, binary_image.width) # get the image height for a converted image/page
img_height = binary_image.height - 120 # is 120 a magic number?

cropped = binary_image.crop((0, 0, X_MARGIN , img_height))
cropped_array = np.array(cropped)
# binary_image.show()
cropped_img = Image.fromarray(cropped_array)
cropped_img.show()


""" 
Here we get the heights for the question markers
The top of the question is given in the pixel_values array
"""
non_white_pixels = []
pixel_values = []


THRESHOLD_DISTANCE = 100  # Minimum distance between the start of two questions
CHECK_DISTANCE = 50  # Distance to check outside the margin before adding a boundary


pixel_values = []
for index, row in enumerate(cropped_array):
    if len(set(row)) != 1:
        non_white_pixels.append(index)

        if index - 1 not in non_white_pixels:
            # Check the content outside the margin
            outside_margin = binary_image.crop((X_MARGIN, index - CHECK_DISTANCE, binary_image.width, index + CHECK_DISTANCE))
            outside_margin_array = np.array(outside_margin)
            if np.any(outside_margin_array == 0):
                # There is non-white content outside the margin, so this is likely a true question boundary
                pixel_values.append(index)


# for index, row in enumerate(cropped_array):
#     if len(set(row)) != 1:
#         non_white_pixels.append(index)

#         if index - 1 not in non_white_pixels:
#             pixel_values.append(index)
        

print(f'non-white pixels: {non_white_pixels}, pixel-values: {pixel_values}')

# THRESHOLD_DISTANCE = 200  # Minimum distance between the start of two questions

# filtered_pixel_values = [pixel_values[0]]
# for i in range(1, len(pixel_values)):
#     if pixel_values[i] - filtered_pixel_values[-1] >= THRESHOLD_DISTANCE:
#         filtered_pixel_values.append(pixel_values[i])

# print(f'filtered_pixel_values: {filtered_pixel_values}')

"""get the start and end coords"""
height_coords = []
for i in range(len(pixel_values) - 1):
    height_coords.append(
        (pixel_values[i] - 50, pixel_values[i + 1] - 50) # what does the 50 represent here: adds a white border to make it look better
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
    """This calls the remove vertical whitespace function"""
    print(f'length of images  {len(images)}')
    out = []
    for image in images:
        get_question_number(image)
        image_new = hide_question_number(image)
        out.append(remove_vertical_whitespace(image_new))
    return out

def remove_vertical_whitespace(i):
    image = get_grayscale_image(i)
    data = np.array(image)
    # Project the 2D image data onto the vertical axis
    min_values = data.min(axis=1)
    
    # Find the first and last occurrence of a value less than the threshold
    non_white_rows = np.where(min_values < 128)[0]
    # If there's no content in the image, exit the function
    if non_white_rows.size == 0:
        print("No content detected in the image.")
        return

    # Compute top and bottom taking the border into account.
    # Don't let the border go outside the image boundaries.
    BORDER = 50
    top = max(non_white_rows[0] - BORDER, 0)
    bottom = min(non_white_rows[-1] + BORDER, i.height)
    print(f'image height: {i.height}; top: {top}, bottom: {bottom}')

    # Crop the image
    cropped = image.crop((0, top, image.width, bottom))

    # Save the cropped image
    return cropped

def get_question_number(image):
    """perform ocr on the top left corner to get the question number"""
    MAX_WIDTH = 190
    MAX_HEIGHT = 100
    MIN_HEIGHT = 40
    MIN_WIDTH = 100
    image2 = image.crop((MIN_WIDTH, MIN_HEIGHT, MAX_WIDTH, MAX_HEIGHT))
    # binary = image2.point(lambda p: p < 150 and 255)
    # qnum_image.show()
    # _, thresh = cv2.threshold(qnum_image, 150, 255, cv2.THRESH_BINARY_INV)
    # qnum_resize = cv2.resize(thresh, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    # binary.show()
    text = pytesseract.image_to_string(image2, config='--psm 6')
    print(f'Question Number: {repr(text)}')
    return image

def hide_question_number(image):
    # Open the image
    np_img = np.array(image)
    x1, y1, x2, y2 = 100, 50, 190, 100

    np_img[y1:y2, x1:x2][np_img[y1:y2, x1:x2] < 220] = 255 # < threshold value - higher values ensure that number is removed, but may remove other detail too.
    new_image = Image.fromarray(np_img)
    
    return new_image


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


