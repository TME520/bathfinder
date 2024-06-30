# This version processes the base template for sink, shower and bathtub.
# It also automatically looks for the rotated versions (rot90, rot180 and rot270)
# Added support for doors and toilets

import os

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

def spotanddraw(floorplan_pic_rgb, floorplan_pic_gray, template_pic, template_w, template_h, border_color_r, border_color_g, border_color_b):
  res = cv.matchTemplate(floorplan_pic_gray,template_pic,cv.TM_CCOEFF_NORMED)
  threshold = 0.8
  loc = np.where( res >= threshold)
  for pt in zip(*loc[::-1]):
    cv.rectangle(floorplan_pic_rgb, pt, (pt[0] + template_w, pt[1] + template_h), (border_color_r,border_color_g,border_color_b), 2)
 
parser = argparse.ArgumentParser(description='Look for items and furniture on a floorplan')
parser.add_argument('--floorplan', help='Path to input floorplan image.', default='floorplan.png')
parser.add_argument('--sink', help='Path to input sink image.', default='sink.png')
parser.add_argument('--shower', help='Path to input shower image.', default='shower.png')
parser.add_argument('--bathtub', help='Path to input bathtub image.', default='bathtub.png')
parser.add_argument('--toilet', help='Path to input toilet image.', default='toilet.png')
parser.add_argument('--door', help='Path to input door image.', default='dor.png')
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

spotanddraw(floorplan_rgb, floorplan_gray, sink, sink_w, sink_h, 0, 0, 255)

sinkrot90=os.path.dirname(args.sink) + '/' + os.path.splitext(os.path.basename(args.sink))[0] + '-rot90' + os.path.splitext(os.path.basename(args.sink))[1]
sinkrot180=os.path.dirname(args.sink) + '/' + os.path.splitext(os.path.basename(args.sink))[0] + '-rot180' + os.path.splitext(os.path.basename(args.sink))[1]
sinkrot270=os.path.dirname(args.sink) + '/' + os.path.splitext(os.path.basename(args.sink))[0] + '-rot270' + os.path.splitext(os.path.basename(args.sink))[1]
if os.path.isfile(sinkrot90) is True:
  print(f"[INFO] Additional ROT90 file found: {sinkrot90}")
  sinkrot90img = cv.imread(cv.samples.findFile(sinkrot90), cv.IMREAD_GRAYSCALE)
  sinkrot90_w, sinkrot90_h = sinkrot90img.shape[::-1]
  spotanddraw(floorplan_rgb, floorplan_gray, sinkrot90img, sinkrot90_w, sinkrot90_h, 0, 0, 255)
if os.path.isfile(sinkrot180) is True:
  print(f"[INFO] Additional ROT180 file found: {sinkrot180}")
  sinkrot180img = cv.imread(cv.samples.findFile(sinkrot180), cv.IMREAD_GRAYSCALE)
  sinkrot180_w, sinkrot180_h = sinkrot180img.shape[::-1]
  spotanddraw(floorplan_rgb, floorplan_gray, sinkrot180img, sinkrot180_w, sinkrot180_h, 0, 0, 255)
if os.path.isfile(sinkrot270) is True:
  print(f"[INFO] Additional ROT270 file found: {sinkrot270}")
  sinkrot270img = cv.imread(cv.samples.findFile(sinkrot270), cv.IMREAD_GRAYSCALE)
  sinkrot270_w, sinkrot270_h = sinkrot270img.shape[::-1]
  spotanddraw(floorplan_rgb, floorplan_gray, sinkrot270img, sinkrot270_w, sinkrot270_h, 0, 0, 255)

print(f"[INFO] Load shower from file {args.shower}")
shower = cv.imread(cv.samples.findFile(args.shower), cv.IMREAD_GRAYSCALE)
if shower is None:
  print(f"[ERROR] Could not open or find the template shower image {args.shower}")
  exit(0)
shower_w, shower_h = shower.shape[::-1]

spotanddraw(floorplan_rgb, floorplan_gray, shower, shower_w, shower_h, 255, 0, 0)

showerrot90=os.path.dirname(args.shower) + '/' + os.path.splitext(os.path.basename(args.shower))[0] + '-rot90' + os.path.splitext(os.path.basename(args.shower))[1]
showerrot180=os.path.dirname(args.shower) + '/' + os.path.splitext(os.path.basename(args.shower))[0] + '-rot180' + os.path.splitext(os.path.basename(args.shower))[1]
showerrot270=os.path.dirname(args.shower) + '/' + os.path.splitext(os.path.basename(args.shower))[0] + '-rot270' + os.path.splitext(os.path.basename(args.shower))[1]
if os.path.isfile(showerrot90) is True:
  print(f"[INFO] Additional ROT90 file found: {showerrot90}")
  showerrot90img = cv.imread(cv.samples.findFile(showerrot90), cv.IMREAD_GRAYSCALE)
  showerrot90_w, showerrot90_h = showerrot90img.shape[::-1]
  spotanddraw(floorplan_rgb, floorplan_gray, showerrot90img, showerrot90_w, showerrot90_h, 255, 0, 0)
if os.path.isfile(showerrot180) is True:
  print(f"[INFO] Additional ROT180 file found: {showerrot180}")
  showerrot180img = cv.imread(cv.samples.findFile(showerrot180), cv.IMREAD_GRAYSCALE)
  showerrot180_w, showerrot180_h = showerrot180img.shape[::-1]
  spotanddraw(floorplan_rgb, floorplan_gray, showerrot180img, showerrot180_w, showerrot180_h, 255, 0, 0)
if os.path.isfile(showerrot270) is True:
  print(f"[INFO] Additional ROT270 file found: {showerrot270}")
  showerrot270img = cv.imread(cv.samples.findFile(showerrot270), cv.IMREAD_GRAYSCALE)
  showerrot270_w, showerrot270_h = showerrot270img.shape[::-1]
  spotanddraw(floorplan_rgb, floorplan_gray, showerrot270img, showerrot270_w, showerrot270_h, 255, 0, 0)

print(f"[INFO] Load bathtub from file {args.bathtub}")
bathtub = cv.imread(cv.samples.findFile(args.bathtub), cv.IMREAD_GRAYSCALE)
if bathtub is None:
  print(f"[ERROR] Could not open or find the template bathtub image {args.bathtub}")
  exit(0)
bathtub_w, bathtub_h = bathtub.shape[::-1]
 
spotanddraw(floorplan_rgb, floorplan_gray, bathtub, bathtub_w, bathtub_h, 0, 255, 0)

bathtubrot90=os.path.dirname(args.bathtub) + '/' + os.path.splitext(os.path.basename(args.bathtub))[0] + '-rot90' + os.path.splitext(os.path.basename(args.bathtub))[1]
bathtubrot180=os.path.dirname(args.bathtub) + '/' + os.path.splitext(os.path.basename(args.bathtub))[0] + '-rot180' + os.path.splitext(os.path.basename(args.bathtub))[1]
bathtubrot270=os.path.dirname(args.bathtub) + '/' + os.path.splitext(os.path.basename(args.bathtub))[0] + '-rot270' + os.path.splitext(os.path.basename(args.bathtub))[1]
if os.path.isfile(bathtubrot90) is True:
  print(f"[INFO] Additional ROT90 file found: {bathtubrot90}")
  bathtubrot90img = cv.imread(cv.samples.findFile(bathtubrot90), cv.IMREAD_GRAYSCALE)
  bathtubrot90_w, bathtubrot90_h = bathtubrot90img.shape[::-1]
  spotanddraw(floorplan_rgb, floorplan_gray, bathtubrot90img, bathtubrot90_w, bathtubrot90_h, 0, 255, 0)
if os.path.isfile(bathtubrot180) is True:
  print(f"[INFO] Additional ROT180 file found: {bathtubrot180}")
  bathtubrot180img = cv.imread(cv.samples.findFile(bathtubrot180), cv.IMREAD_GRAYSCALE)
  bathtubrot180_w, bathtubrot180_h = bathtubrot180img.shape[::-1]
  spotanddraw(floorplan_rgb, floorplan_gray, bathtubrot180img, bathtubrot180_w, bathtubrot180_h, 0, 255, 0)
if os.path.isfile(bathtubrot270) is True:
  print(f"[INFO] Additional ROT270 file found: {bathtubrot270}")
  bathtubrot270img = cv.imread(cv.samples.findFile(bathtubrot270), cv.IMREAD_GRAYSCALE)
  bathtubrot270_w, bathtubrot270_h = bathtubrot270img.shape[::-1]
  spotanddraw(floorplan_rgb, floorplan_gray, bathtubrot270img, bathtubrot270_w, bathtubrot270_h, 0, 255, 0)

print(f"[INFO] Load toilet from file {args.toilet}")
toilet = cv.imread(cv.samples.findFile(args.toilet), cv.IMREAD_GRAYSCALE)
if toilet is None:
  print(f"[ERROR] Could not open or find the template toilet image {args.toilet}")
  exit(0)
toilet_w, toilet_h = toilet.shape[::-1]

spotanddraw(floorplan_rgb, floorplan_gray, toilet, toilet_w, toilet_h, 100, 0, 0)

toiletrot90=os.path.dirname(args.toilet) + '/' + os.path.splitext(os.path.basename(args.toilet))[0] + '-rot90' + os.path.splitext(os.path.basename(args.toilet))[1]
toiletrot180=os.path.dirname(args.toilet) + '/' + os.path.splitext(os.path.basename(args.toilet))[0] + '-rot180' + os.path.splitext(os.path.basename(args.toilet))[1]
toiletrot270=os.path.dirname(args.toilet) + '/' + os.path.splitext(os.path.basename(args.toilet))[0] + '-rot270' + os.path.splitext(os.path.basename(args.toilet))[1]
if os.path.isfile(toiletrot90) is True:
  print(f"[INFO] Additional ROT90 file found: {toiletrot90}")
  toiletrot90img = cv.imread(cv.samples.findFile(toiletrot90), cv.IMREAD_GRAYSCALE)
  toiletrot90_w, toiletrot90_h = toiletrot90img.shape[::-1]
  spotanddraw(floorplan_rgb, floorplan_gray, toiletrot90img, toiletrot90_w, toiletrot90_h, 100, 0, 0)
if os.path.isfile(toiletrot180) is True:
  print(f"[INFO] Additional ROT180 file found: {toiletrot180}")
  toiletrot180img = cv.imread(cv.samples.findFile(toiletrot180), cv.IMREAD_GRAYSCALE)
  toiletrot180_w, toiletrot180_h = toiletrot180img.shape[::-1]
  spotanddraw(floorplan_rgb, floorplan_gray, toiletrot180img, toiletrot180_w, toiletrot180_h, 100, 0, 0)
if os.path.isfile(toiletrot270) is True:
  print(f"[INFO] Additional ROT270 file found: {toiletrot270}")
  toiletrot270img = cv.imread(cv.samples.findFile(toiletrot270), cv.IMREAD_GRAYSCALE)
  toiletrot270_w, toiletrot270_h = toiletrot270img.shape[::-1]
  spotanddraw(floorplan_rgb, floorplan_gray, toiletrot270img, toiletrot270_w, toiletrot270_h, 100, 0, 0)
 
print("[INFO] Writing result file template_matching004-generic_output.png")
cv.imwrite('template_matching006-generic_output.png',floorplan_rgb)

print("[INFO] Done, exiting.")
exit(0)

