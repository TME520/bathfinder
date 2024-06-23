try:
  import argparse
except ImportError:
  print('Cannot import argparse module\nTry: pip3 install argparse') 

try:
  import numpy as np
except ImportError:
  print('Cannot import numpy module\nTry: pip3 install numpy') 

try:
  import cv2 as cv
except ImportError:
  print('Cannot import cv2 computer vision PIP module\nTry: pip3 install opencv-python')

parser = argparse.ArgumentParser(description='Code for basic contour detection')
parser.add_argument('--input', help='Path to input image.', default='pic3.png')
args = parser.parse_args()

img = cv.imread(cv.samples.findFile(args.input))
if img is None:
    print('Could not open or find the image:', args.input)
    exit(0)

print("Get pixel value")
px = img[100,100]
print(f"Value: {px}")

# Image is BGR, Blue(0) - Green(1) - Red(2)
blue = img[100,100,0]
print(f"Blue: {blue}")
green = img[100,100,1]
print(f"Green: {green}")
red = img[100,100,2]
print(f"Red: {red}")

print("Modify pixel color")
img[100,100] = [255,255,255]
print(f"{img[100,100]}")

print(f"Image properties (rows, columns, channels): {img.shape}")

print("Experimenting with ROI, Region Of Interest")
ball = img[280:340, 330:390]
img[273:333, 100:160] = ball

img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imwrite("img_gray_out.png", img_gray)

exit(0)

