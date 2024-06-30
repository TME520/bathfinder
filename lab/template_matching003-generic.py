try:
  import argparse
except ImportError:
  print('Cannot import argparse module\nTry: pip3 install argparse')

try:
  import cv2 as cv
except ImportError:
  print('Cannot import cv2 computer vision PIP module\nTry: pip3 install opencv-python')

try:
  import numpy as np
except ImportError:
  print('Cannot import numpy module\nTry: pip3 install numpy') 

try:
  from matplotlib import pyplot as plt
except ImportError:
  print('Cannot import pyplot module\nTry: pip3 install matplotlib') 
 
parser = argparse.ArgumentParser(description='Look for items and furniture on a floorplan')
parser.add_argument('--floorplan', help='Path to input floorplan image.', default='floorplan.png')
parser.add_argument('--template', help='Path to input template image.', default='template.png')
args = parser.parse_args()

# Load floorplan from file
floorplan_rgb = cv.imread(cv.samples.findFile(args.floorplan))
if floorplan_rgb is None:
    print('Could not open or find the floorplan image:', args.floorplan)
    exit(0)

floorplan_gray = cv.cvtColor(floorplan_rgb, cv.COLOR_BGR2GRAY)

# Load template (sink, shower, bathtub, toilet...) from file
template = cv.imread(cv.samples.findFile(args.template), cv.IMREAD_GRAYSCALE)
if template is None:
    print('Could not open or find the template image:', args.template)
    exit(0)
w, h = template.shape[::-1]
 
res = cv.matchTemplate(floorplan_gray,template,cv.TM_CCOEFF_NORMED)
threshold = 0.8
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
 cv.rectangle(floorplan_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
 
cv.imwrite('template_matching003-generic_output.png',floorplan_rgb)
exit(0)

