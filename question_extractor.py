from PIL import Image
import numpy as np
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.debug('Test debug message')
logger.info('This is an info message')

# new function
THRESHOLD_VALUE = 180  # Adjust this value based on the image characteristics and number clarity
X_MARGIN = 180
image = Image.open('test-page15.jpg')
grayscale_image = image.convert('L')
binary_image = grayscale_image.point(lambda x: 0 if x < THRESHOLD_VALUE else 255, "1")
img_height = binary_image.height - 120 # is 120 a magic number?

def get_threshold_value():
    """This sets the value at which a pixel is considered black or white"""
    return 180

def get_footer_height():
    """Removes the footer from image processing operations"""
    return 120

def convert_to_grayscale_image(image):
    return image.convert('L')

def convert_to_binary_image(image, thresh):
    image.point(lambda x: 0 if x < thresh else 255, "1")

def calculate_image_height():
    return 0

cropped = binary_image.crop((0, 0, X_MARGIN , img_height))
binary_array = np.asarray(binary_image)
cropped_array = np.array(cropped)

def get_margin_coords():
    xstart = 0
    ystart = 0
    xend = X_MARGIN
    yend = img_height
    return (xstart, ystart, xend, yend)

def find_question_starts(binary_array, cropped_array):
    non_white_rows = np.where(np.any(cropped_array == 0, axis=1))[0]
    
    diffs = np.diff(non_white_rows, prepend=non_white_rows[0])
    starts = np.where(diffs != 1)[0]
    candidate_starts = non_white_rows[starts]
    res = candidate_starts[np.all(binary_array[candidate_starts - 25] == 1, axis=1)]
    return res

pixel_values = find_question_starts(binary_array, cropped_array)

"""get the start and end coords"""

height_coords = []
for i in range(len(pixel_values) - 1):
    height_coords.append(
        (pixel_values[i] - 50, pixel_values[i + 1] - 50) # what does the 50 represent here: adds a white border to make it look better
    )

print(height_coords) # DEBUG


def crop_questions(image, coordinates: list[tuple]):
    questions = []
    # image = Image.open(image)
    for (start, end) in coordinates:
        question = image.crop((0, start, image.width, end))
        questions.append(question)
    return questions


def remove_vertical_whitespace(i, thresh):
    data = np.array(image)
    # Project the 2D image data onto the vertical axis
    min_values = data.min(axis=1)
    
    # Find the first and last occurrence of a value less than the threshold
    non_white_rows = np.where(min_values < thresh)[0]
    # If there's no content in the image, exit the function
    if non_white_rows.size == 0:
        print("No content detected in the image.")
        return

    # Compute top and bottom taking the border into account.
    # Don't let the border go outside the image boundaries.
    BORDER = 50
    top = max(non_white_rows[0] - BORDER, 0)
    bottom = min(non_white_rows[-1] + BORDER, i.height)
    # Crop the image
    cropped = image.crop((0, top, image.width, bottom))
    # Save the cropped image
    return cropped

questions = crop_questions(image, height_coords)
# for q in questions:
#     q.show()

def main():
    image = Image.open('test-page15.jpg')
    grayscale_image = convert_to_grayscale_image(image)
    threshold_value = get_threshold_value()
    # min_question_distance = get_question_distance()
    binary_image = convert_to_binary_image(grayscale_image, threshold_value)

