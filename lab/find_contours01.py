import cv2 as cv
import argparse

parser = argparse.ArgumentParser(description='Code for basic contour detection')
parser.add_argument('--input', help='Path to input image.', default='pic3.png')
args = parser.parse_args()

img = cv.imread(cv.samples.findFile(args.input))
if img is None:
    print('Could not open or find the image:', args.input)
    exit(0)

# img = cv.imread("UYret.png")
img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(img_gray, 127, 255, 0)
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

print(contours)
cv.drawContours(img, contours, -1, (0, 255, 0), 3)
cv.imwrite("out.png", img)

