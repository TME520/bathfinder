import os

try:
  import numpy as np
except ImportError:
  print('Cannot import numpy module\nTry: pip3 install numpy') 

try:
  import cv2
except ImportError:
  print('Cannot import cv2 computer vision PIP module\nTry: pip3 install opencv-python')

import sys

IMAGE_NAME = 'TRY005-floorplan001.jpg'
img_gray = cv2.imread(IMAGE_NAME, cv2.IMREAD_GRAYSCALE)
(thresh, img_bw) = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
thresh = 127
img_bw = cv2.threshold(img_gray, thresh, 255, cv2.THRESH_BINARY)[1]

kernel = np.ones((5, 5), np.uint8)
img_eroded = cv2.erode(img_bw, kernel, iterations=2)
cv2.imshow("Eroded pic", img_eroded)
img_dilated = cv2.dilate(img_bw, kernel)
cv2.imshow("Dilated pic", img_dilated)

cv2.imwrite("room_detection_output.png", img_bw)

# Press any key to close the image
cv2.waitKey(0)

# Clean up
cv2.destroyAllWindows()

exit(0)

