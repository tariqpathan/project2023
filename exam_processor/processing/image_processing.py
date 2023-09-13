from PIL import Image, ImageDraw
import numpy as np
from typing import Tuple


def overwrite_image(image: Image.Image, coords: Tuple[int, int, int, int]) -> Image.Image:
    """Overlays a white box on given image with provided coords"""
    modified_image = image.copy()
    draw = ImageDraw.Draw(modified_image)
    draw.rectangle(coords, fill="white")
    return modified_image

def remove_vertical_whitespace(image: Image.Image, padding:int, threshold: int) -> Image.Image:
    """Removes vertical whitespace from an image upto a padded amount"""
    data = np.array(image)
    min_values = data.min(axis=1)
    non_white_rows = np.where(min_values < threshold)[0]
    top = max(non_white_rows[0] - padding, 0)
    bottom = min(non_white_rows[-1] + padding, image.height)
    return image.crop((0, top, image.width, bottom))

def convert_to_grayscale_image(image:Image.Image) -> Image.Image:
    """Converts image to grayscale"""
    return image.convert('L')

def convert_to_binary_image(image: Image.Image, threshold: int) -> Image.Image:
    """
    Converts a grayscale image to a binary, using threshold value
    1 represents a white pixel, 0 represents black
    """
    return image.point(lambda x: 0 if x < threshold else 255, "1")