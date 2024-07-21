import os
import random

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
  cv2.imwrite("step1-room_detection_output.png", img)

  # Detect corners
  dst = cv2.cornerHarris(img ,2,3,0.04)
  dst = cv2.dilate(dst,None)
  corners = dst > corners_threshold * dst.max()

  # Draw lines to close the rooms off by adding a line between corners on the same x or y coordinate
  # This gets some false positives.
  # You could try to disallow drawing through other existing lines for example.
  for y,row in enumerate(corners):
    x_same_y = np.argwhere(row)
    for x1, x2 in zip(x_same_y[:-1], x_same_y[1:]):
      if x2[0] - x1[0] < room_closing_max_length:
        # color = 0
        color = 230
        # color = random.randint(0,255) 
        # print(f'x1: {x1}, x2: {x2}')
        # print(f'\t\tx1[0]: {x1[0]}, x2[0]: {x2[0]}')
        cv2.line(img, (int(x1[0]), int(y)), (int(x2[0]), int(y)), color, 1)
  cv2.imwrite("step2-room_detection_output.png", img)

  for x,col in enumerate(corners.T):
    y_same_x = np.argwhere(col)
    for y1, y2 in zip(y_same_x[:-1], y_same_x[1:]):
      if y2[0] - y1[0] < room_closing_max_length:
        # color = 0
        color = 230
        # color = random.randint(0,255)
        # print(f'y1: {y1}, y2: {y2}')
        cv2.line(img, (int(x), int(y1[0])), (int(x), int(y2[0])), color, 1)
  cv2.imwrite("step3-room_detection_output.png", img)

  cv2.imwrite("room_detection_output.png", img)
  rooms = []
  return rooms, img

  # Mark the outside of the house as black
  contours, _ = cv2.findContours(~img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
  biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
  mask = np.zeros_like(mask)
  cv2.fillPoly(mask, [biggest_contour], 255)
  # img[mask == 0] = 0
  img[mask == 0] = 10

  # Find the connected components in the house
  ret, labels = cv2.connectedComponents(img)
  img = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
  unique = np.unique(labels)
  rooms = []
  for label in unique:
    component = labels == label
    if img[component].sum() == 0 or np.count_nonzero(component) < gap_in_wall_threshold:
      color = 0
    else:
      rooms.append(component)
      color = np.random.randint(0, 255, size=3)
    img[component] = color
  # print(f'Rooms: {rooms}')

  cv2.imwrite("room_detection_output.png", img)

  return rooms, img

IMAGE_NAME = 'TRY005-floorplan001.jpg'
img_gray = cv2.imread(IMAGE_NAME, cv2.IMREAD_GRAYSCALE)
(thresh, img_bw) = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
thresh = 127
img_bw = cv2.threshold(img_gray, thresh, 255, cv2.THRESH_BINARY)[1]

# kernel = np.ones((5, 5), np.uint8)
kernel = np.ones((3, 3), np.uint8)
img_eroded = cv2.erode(img_bw, kernel, iterations=2)
# cv2.imshow("Eroded pic", img_eroded)
img_dilated = cv2.dilate(img_bw, kernel)
# cv2.imshow("Dilated pic", img_dilated)
cv2.imwrite("step0-room_detection_output.png", img_dilated)

rooms, colored_house = find_rooms(img_dilated.copy())

# cv2.imwrite("room_detection_output.png", img_bw)

# Press any key to close the image
# cv2.waitKey(0)
cv2.destroyAllWindows()

exit(0)

