# This version processes the base template for sinks, showers, bathtubs, doors and toilets.
# It also automatically looks for the rotated versions (rot90, rot180 and rot270)
# Count & catalog discovered items (now stores it in a dict)
# Cleaned up output files and folders
# Item detection and floorplan anotation are now two separate steps

import os
import string
import random

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

detected_items = {}
anti_duplicates = {}

def writeToFile(filename, mode, content):
  target_file = open(filename, mode)
  target_file.write(content)
  target_file.close()

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

def spotitems(floorplan_pic_rgb, floorplan_pic_gray, template_pic, template_w, template_h, item_type, item_subtype):
  res = cv.matchTemplate(floorplan_pic_gray,template_pic,cv.TM_CCOEFF_NORMED)
  # threshold = 0.8
  threshold = 0.7
  loc = np.where(res >= threshold)
  if (len(anti_duplicates)>0):
    notDuplicate = False
  else:
    notDuplicate = True
  if (len(loc[0]) > 0) and (len(loc[1]) > 0):
    maxdrifty = template_w
    maxdrifx = template_h
    for pt in zip(*loc[::-1]):
      if (len(anti_duplicates)>0):
        for current_duplicate in anti_duplicates:
          if (((pt[0]<anti_duplicates[current_duplicate]['minus_y']) or (pt[0]>anti_duplicates[current_duplicate]['plus_y'])) or ((pt[1]<anti_duplicates[current_duplicate]['minus_x']) or (pt[1]>anti_duplicates[current_duplicate]['plus_x']))):
             notDuplicate = True
          else:
            writeToFile(f'{output_log}bathfinder.log', 'a', '.')
            notDuplicate = False
            break
      if (notDuplicate == True):
        rndid=id_generator()
        print(f'[INFO] New {item_type} ({rndid}) located {pt}, will draw')
        writeToFile(f'{output_log}bathfinder.log', 'a', f'  [INFO] New {item_type} ({rndid}) located {pt}, will draw \n')
        detected_items[rndid] = { 'type':item_type, 'x':pt[1], 'y':pt[0], 'height':template_h, 'width':template_w }
        anti_duplicates[rndid] = { 'duptype':item_type, 'subtype':item_subtype, 'minus_x':pt[1] - 10, 'minus_y':pt[0] - 10, 'plus_x':pt[1] + 10, 'plus_y':pt[0] + 10 }
        writeToFile(f'{output_log}bathfinder.log', 'a', f'  [DEBUG] New duplicate added to the list: duptype={item_type}, subtype={item_subtype}, minus_x={pt[1] - 10}, minus_y={pt[0] - 10}, plus_x={pt[1] + 10}, plus_y={pt[0] + 10} \n')

def drawdetecteditems():
  for current_item in detected_items:
    print(f'  [DEBUG] Drawing {current_item}')
    match detected_items[current_item]['type']:
      case "bathtub":
        border_color_r = 255
        border_color_g = 0
        border_color_b = 0
      case "door":
        border_color_r = 0
        border_color_g = 100 
        border_color_b = 0
      case "shower":
        border_color_r = 0
        border_color_g = 0 
        border_color_b = 255
      case "sink":
        border_color_r = 0
        border_color_g = 255
        border_color_b = 0
      case "toilet":
        border_color_r = 0
        border_color_g = 0 
        border_color_b = 100
    cv.rectangle(floorplan_rgb, (detected_items[current_item]['y'], detected_items[current_item]['x']), (detected_items[current_item]['y'] + detected_items[current_item]['width'], detected_items[current_item]['x'] + detected_items[current_item]['height']), (border_color_r,border_color_g,border_color_b), 2)
    cv.putText(floorplan_rgb, f'{current_item}', (detected_items[current_item]['y'] + 5, detected_items[current_item]['x'] - 3), cv.FONT_HERSHEY_PLAIN, 1, (border_color_r,border_color_g,border_color_b), 1, cv.LINE_AA)

input_folder = './input/'
output_folder = './output/'
floorplans_folder = f'{input_folder}floorplans/'
bathtubs_folder = f'{input_folder}bathtubs/'
doors_folder = f'{input_folder}doors/'
showers_folder = f'{input_folder}showers/'
sinks_folder = f'{input_folder}sinks/'
toilets_folder = f'{input_folder}toilets/'

if (os.path.isdir(f'{input_folder}')):
  print(f'[DEBUG] {input_folder} folder found')
else:
  print(f'[DEBUG] Creating {input_folder} folder...') 
  os.mkdir(f'{input_folder}')
  print(f'[INFO] ...done. Now place your input files in {input_folder} and restart this program.')
  print(f'{input_folder} must contain the following folders: floorplans, bathtubs, doors, showers, sinks, toilets')
  exit(0)

if (os.path.isdir(f'{output_folder}')):
  print(f'[DEBUG] {output_folder} folder found')
else:
  print(f'[DEBUG] Creating {output_folder} folder')
  os.mkdir(f'{output_folder}')
  output_csv = f'{output_folder}/csv/'
  os.mkdir(f'{output_csv}')
  output_image = f'{output_folder}/image/'
  os.mkdir(f'{output_image}')
  output_log = f'{output_folder}/log/'
  os.mkdir(f'{output_log}')

writeToFile(f'{output_log}bathfinder.log', 'w', '[INFO] New run\n')

print('[DEBUG] Listing input floorplan files')
input_floorplans_list = []
for (dir_path, dir_names, file_names) in os.walk(floorplans_folder):
    input_floorplans_list.extend(file_names)
print(input_floorplans_list)

print('[DEBUG] Listing bathtubs templates')
bathtubs_templates_list = []
for (dir_path, dir_names, file_names) in os.walk(bathtubs_folder):
    bathtubs_templates_list.extend(file_names)
print(bathtubs_templates_list)

print('[DEBUG] Listing doors templates')
doors_templates_list = []
for (dir_path, dir_names, file_names) in os.walk(doors_folder):
    doors_templates_list.extend(file_names)
print(doors_templates_list)

print('[DEBUG] Listing showers templates')
showers_templates_list = []
for (dir_path, dir_names, file_names) in os.walk(showers_folder):
    showers_templates_list.extend(file_names)
print(showers_templates_list)

print('[DEBUG] Listing sinks templates')
sinks_templates_list = []
for (dir_path, dir_names, file_names) in os.walk(sinks_folder):
    sinks_templates_list.extend(file_names)
print(sinks_templates_list)

print('[DEBUG] Listing toilets templates')
toilets_templates_list = []
for (dir_path, dir_names, file_names) in os.walk(toilets_folder):
    toilets_templates_list.extend(file_names)
print(toilets_templates_list)

# Process floorplans one by one
for current_floorplan in input_floorplans_list:
  print(f'[INFO] Load floorplan from file {floorplans_folder}{current_floorplan}')
  detected_items = {}
  floorplan_rgb = cv.imread(cv.samples.findFile(f'{floorplans_folder}{current_floorplan}'))
  if floorplan_rgb is None:
    print(f'[ERROR] Floorplan image {floorplans_folder}{current_floorplan} not found or unsupported')
  else:
    writeToFile(f'{output_log}bathfinder.log', 'a', f'[INFO] Processing floorplan {current_floorplan} \n')
    floorplan_gray = cv.cvtColor(floorplan_rgb, cv.COLOR_BGR2GRAY)
    # Compare sinks against current floorplan one by one
    anti_duplicates = {}
    for current_sink in sinks_templates_list:
      print(f'  [INFO] Checking sink template {sinks_folder}{current_sink}')
      sink = cv.imread(cv.samples.findFile(f'{sinks_folder}{current_sink}'), cv.IMREAD_GRAYSCALE)
      if sink is None:
        print(f'  [ERROR] Sink template image {sinks_folder}{current_sink} not found or unsupported')
      else:
        sink_w, sink_h = sink.shape[::-1]
        spotitems(floorplan_rgb, floorplan_gray, sink, sink_w, sink_h, 'sink', current_sink)
    # Compare showers against current floorplan one by one
    anti_duplicates = {}
    for current_shower in showers_templates_list:
      print(f'  [INFO] Checking shower template {showers_folder}{current_shower}')
      shower = cv.imread(cv.samples.findFile(f'{showers_folder}{current_shower}'), cv.IMREAD_GRAYSCALE)
      if shower is None:
        print(f'  [ERROR] Shower template image {showers_folder}{current_shower} not found or unsupported')
      else:
        shower_w, shower_h = shower.shape[::-1]
        spotitems(floorplan_rgb, floorplan_gray, shower, shower_w, shower_h, 'shower', current_shower)
    # Compare bathtubs against current floorplan one by one
    anti_duplicates = {}
    for current_bathtub in bathtubs_templates_list:
      print(f'  [INFO] Checking bathtub template {bathtubs_folder}{current_bathtub}')
      bathtub = cv.imread(cv.samples.findFile(f'{bathtubs_folder}{current_bathtub}'), cv.IMREAD_GRAYSCALE)
      if bathtub is None:
        print(f'  [ERROR] Bathtub template image {bathtubs_folder}{current_bathtub} not found or unsupported')
      else:
        bathtub_w, bathtub_h = bathtub.shape[::-1]
        spotitems(floorplan_rgb, floorplan_gray, bathtub, bathtub_w, bathtub_h, 'bathtub', current_bathtub)
    # Compare toilets against current floorplan one by one
    anti_duplicates = {}
    for current_toilet in toilets_templates_list:
      print(f'  [INFO] Checking toilet template {toilets_folder}{current_toilet}')
      toilet = cv.imread(cv.samples.findFile(f'{toilets_folder}{current_toilet}'), cv.IMREAD_GRAYSCALE)
      if toilet is None:
        print(f'  [ERROR] Toilet template image {toilets_folder}{current_toilet} not found or unsupported')
      else:
        toilet_w, toilet_h = toilet.shape[::-1]
        spotitems(floorplan_rgb, floorplan_gray, toilet, toilet_w, toilet_h, 'toilet', current_toilet)
    # Compare doors against current floorplan one by one
    anti_duplicates = {}
    for current_door in doors_templates_list:
      print(f'  [INFO] Checking door template {doors_folder}{current_door}')
      door = cv.imread(cv.samples.findFile(f'{doors_folder}{current_door}'), cv.IMREAD_GRAYSCALE)
      if door is None:
        print(f'  [ERROR] Door template image {doors_folder}{current_door} not found or unsupported')
      else:
        door_w, door_h = door.shape[::-1]
        spotitems(floorplan_rgb, floorplan_gray, door, door_w, door_h, 'door', current_door)
    drawdetecteditems()
    print(f'  [INFO] Writing result file {output_image}{current_floorplan}-detected_items.png')
    cv.imwrite(f'{output_image}{current_floorplan}-detected_items.png',floorplan_rgb)
    print(f'  [INFO] Listing found items in CSV file {output_csv}{current_floorplan}-detected_items.csv')
    writeToFile(f'{output_csv}{current_floorplan}-detected_items.csv', 'w', 'id,type,x,y\n')
    for current_item in detected_items:
      print(f"  [DEBUG] Reference: {current_item} - Type: {detected_items[current_item]['type']} - X: {detected_items[current_item]['x']} - Y: {detected_items[current_item]['y']}")
      writeToFile(f'{output_log}bathfinder.log', 'a', f'  [INFO] {current_floorplan} Found {detected_items[current_item]["type"]} with reference {current_item} at {detected_items[current_item]["x"]},{detected_items[current_item]["y"]}\n')

print('[INFO] Done, exiting.')
exit(0)

