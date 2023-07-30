from PIL import Image

image = Image.open('test-page1.jpg')

# what do i have to do?
# 'read' the margin and get coords
# split the images according to the y-coords/height
# save the image section and tag it with the appropriate metadata

print(image.format, image.size, image.mode)