#jpeg to RLE run file
#Made by William and friend...
#This script will prompt for a file path of an image and return a file - 'output.rle' that contains the rle values of the JPEG
#The output will be of format <width> <height> <max-grey-level> <grey-level><len> etcetc
import cv2
from PIL import Image
import numpy as np


def rle_encode(data):
    encoded = []
    prev_pixel = data[0]
    count = 1

    for pixel in data[1:]:
        if pixel == prev_pixel:
            count += 1
        else:
            encoded.append((prev_pixel, count))
            prev_pixel = pixel
            count = 1
    
    encoded.append((prev_pixel, count))
    return encoded

while True:
    #load image
    path = input("enter image path:").strip('"')
    image = Image.open(path)
    #check image loaded
    if image is None:
        raise ValueError("Error: Image not found or could not be read. Check path!")

    #resize - dimensions in pixels - the aspect ratio won't change - set to appropriate for terminal printing - 100x100 is good
    image.thumbnail((100, 100))
    
    #convert to greyscale
    image = image.convert("L")

    #convert to numpy array
    imageArr = np.array(image)
 
    #get image dimensions
    height, width = imageArr.shape
    print("height:",  height)
    print("width:", width)

    #reduce greyscale levels to 4
    quantised_image = np.floor(imageArr/64).astype(np.uint8) # values: 0,1,2,3

    #flatten image into 1D array
    pixels = quantised_image.flatten()

    #apply RLE
    compressed_data = rle_encode(pixels)

    #save to file
    with open("output.rle", "w") as file:
        file.write(f"{width} {height} 4\n")
        for value, count in compressed_data:
            file.write(f"{value} {count}\n")

    print("Conversion complete!")