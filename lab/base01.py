import cv2 as cv
import argparse

parser = argparse.ArgumentParser(description='Code for basic contour detection')
parser.add_argument('--input', help='Path to input image.', default='pic3.png')
args = parser.parse_args()

img = cv.imread(cv.samples.findFile(args.input))
if img is None:
    print('Could not open or find the image:', args.input)
    exit(0)

img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imwrite("img_gray_out.png", img_gray)

exit(0)

