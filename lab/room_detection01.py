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

def find_rooms(img, noise_removal_threshold=25, corners_threshold=0.1, room_closing_max_length=100, gap_in_wall_threshold=500):
  """
  :param img: grey scale image of rooms, already eroded and doors removed etc.
  :param noise_removal_threshold: Minimal area of blobs to be kept.
  :param corners_threshold: Threshold to allow corners. Higher removes more of the house.
  :param room_closing_max_length: Maximum line length to add to close off open doors.
  :param gap_in_wall_threshold: Minimum number of pixels to identify component as room instead of hole in the wall.
  :return: rooms: list of numpy arrays containing boolean masks for each detected room
           colored_house: A colored version of the input image, where each room has a random color.
  """
  assert 0 <= corners_threshold <= 1
  img[img < 128] = 0
  img[img > 128] = 255
  contours, _ = cv2.findContours(~img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  # print(f'Contours: {contours}')
  mask = np.zeros_like(img)
  for contour in contours:
    # print(f'Current contour: {contour}')
    area = cv2.contourArea(contour)
    if area > noise_removal_threshold:
      cv2.fillPoly(mask, [contour], 255)
  img = ~mask
  cv2.imshow("Contoured", img)

  rooms = []
  img = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
  return rooms, img

IMAGE_NAME = 'TRY005-floorplan001.jpg'
img_gray = cv2.imread(IMAGE_NAME, cv2.IMREAD_GRAYSCALE)
(thresh, img_bw) = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
thresh = 127
img_bw = cv2.threshold(img_gray, thresh, 255, cv2.THRESH_BINARY)[1]

kernel = np.ones((5, 5), np.uint8)
img_eroded = cv2.erode(img_bw, kernel, iterations=2)
# cv2.imshow("Eroded pic", img_eroded)
img_dilated = cv2.dilate(img_bw, kernel)
cv2.imshow("Dilated pic", img_dilated)

rooms, colored_house = find_rooms(img_dilated.copy())

cv2.imwrite("room_detection_output.png", img_bw)

# Press any key to close the image
cv2.waitKey(0)
cv2.destroyAllWindows()

exit(0)

