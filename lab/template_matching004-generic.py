# This version looks for sinks, showers and bathtubs.

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
parser.add_argument('--sink', help='Path to input sink image.', default='sink.png')
parser.add_argument('--shower', help='Path to input shower image.', default='shower.png')
parser.add_argument('--bathtub', help='Path to input bathtub image.', default='bathtub.png')
args = parser.parse_args()

print(f"[INFO] Load floorplan from file {args.floorplan}")
floorplan_rgb = cv.imread(cv.samples.findFile(args.floorplan))
if floorplan_rgb is None:
    print(f"[ERROR] Could not open or find the floorplan image {args.floorplan}")
    exit(0)

floorplan_gray = cv.cvtColor(floorplan_rgb, cv.COLOR_BGR2GRAY)

print(f"[INFO] Load sink from file {args.sink}")
sink = cv.imread(cv.samples.findFile(args.sink), cv.IMREAD_GRAYSCALE)
if sink is None:
    print(f"[ERROR] Could not open or find the template sink image {args.sink}")
    exit(0)
sink_w, sink_h = sink.shape[::-1]
 
res = cv.matchTemplate(floorplan_gray,sink,cv.TM_CCOEFF_NORMED)
threshold = 0.8
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
 cv.rectangle(floorplan_rgb, pt, (pt[0] + sink_w, pt[1] + sink_h), (0,0,255), 2)

print(f"[INFO] Load shower from file {args.shower}")
shower = cv.imread(cv.samples.findFile(args.shower), cv.IMREAD_GRAYSCALE)
if shower is None:
    print(f"[ERROR] Could not open or find the template shower image {args.shower}")
    exit(0)
shower_w, shower_h = shower.shape[::-1]
 
res = cv.matchTemplate(floorplan_gray,shower,cv.TM_CCOEFF_NORMED)
threshold = 0.8
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
 cv.rectangle(floorplan_rgb, pt, (pt[0] + shower_w, pt[1] + shower_h), (255,0,0), 2)

print(f"Load bathtub from file {args.bathtub}")
bathtub = cv.imread(cv.samples.findFile(args.bathtub), cv.IMREAD_GRAYSCALE)
if bathtub is None:
    print(f"Could not open or find the template bathtub image {args.bathtub}")
    exit(0)
bathtub_w, bathtub_h = bathtub.shape[::-1]
 
res = cv.matchTemplate(floorplan_gray,bathtub,cv.TM_CCOEFF_NORMED)
threshold = 0.8
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
 cv.rectangle(floorplan_rgb, pt, (pt[0] + bathtub_w, pt[1] + bathtub_h), (0,255,0), 2)
 
print("[INFO] Writing result file template_matching004-generic_output.png")
cv.imwrite('template_matching004-generic_output.png',floorplan_rgb)

print("[INFO] Done, exiting.")
exit(0)

