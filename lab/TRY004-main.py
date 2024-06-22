try:
  import numpy as np
except ImportError:
  print('Cannot import numpy module\nTry: pip3 install numpy')

try:
  import cv2
except ImportError:
  print('Cannot import cv2 computer vision PIP module\nTry: pip3 install opencv-python')

print("Loading images")
image1 = cv2.imread("./TRY004-input/journal1.jpg")
image2 = cv2.imread("./TRY004-input/news1.jpg")
image3 = cv2.imread("./TRY004-input/CookingAtItsBest.png")
image4 = cv2.imread("./TRY004-input/TRY004-floorplan001.jpg")
image5 = cv2.imread("./TRY004-input/TRY004-floorplan002.jpg")

print("Hardcoded assigning of output images for the 3 input images")
output1_letter = image1.copy()
output1_word = image1.copy()
output1_line = image1.copy()
output1_par = image1.copy()
output1_margin = image1.copy()

output2_letter = image2.copy()
output2_word = image2.copy()
output2_line = image2.copy()
output2_par = image2.copy()
output2_margin = image2.copy()

output3_letter = image3.copy()
output3_word = image3.copy()
output3_line = image3.copy()
output3_par = image3.copy()
output3_margin = image3.copy()

output4_letter = image4.copy()
output4_word = image4.copy()
output4_line = image4.copy()
output4_par = image4.copy()
output4_margin = image4.copy()

output5_letter = image5.copy()
output5_word = image5.copy()
output5_line = image5.copy()
output5_par = image5.copy()
output5_margin = image5.copy()

gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
gray3 = cv2.cvtColor(image3, cv2.COLOR_BGR2GRAY)
gray4 = cv2.cvtColor(image4, cv2.COLOR_BGR2GRAY)
gray5 = cv2.cvtColor(image5, cv2.COLOR_BGR2GRAY)

print("Clean the image using otsu method with the inversed binarized image")
ret1,th1 = cv2.threshold(gray1,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
ret2,th2 = cv2.threshold(gray2,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
ret3,th3 = cv2.threshold(gray3,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
ret4,th4 = cv2.threshold(gray4,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
ret5,th5 = cv2.threshold(gray5,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

def process_letter(thresh,output):	
  print("Processing letter by letter boxing")
  # assign the kernel size	
  kernel = np.ones((2,1), np.uint8) # vertical
  # use closing morph operation then erode to narrow the image	
  temp_img = cv2.morphologyEx(thresh,cv2.MORPH_CLOSE,kernel,iterations=3)
  # temp_img = cv2.erode(thresh,kernel,iterations=2)		
  letter_img = cv2.erode(temp_img,kernel,iterations=1)

  # find contours 
  (contours, _) = cv2.findContours(letter_img.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

  # loop in all the contour areas
  for cnt in contours:
    x,y,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(output,(x-1,y-5),(x+w,y+h),(0,255,0),1)

  return output	

def process_word(thresh,output):	
  print("Processing letter by letter boxing")
  # assign 2 rectangle kernel size 1 vertical and the other will be horizontal	
  kernel = np.ones((2,1), np.uint8)
  kernel2 = np.ones((1,4), np.uint8)
  # use closing morph operation but fewer iterations than the letter then erode to narrow the image	
  temp_img = cv2.morphologyEx(thresh,cv2.MORPH_CLOSE,kernel,iterations=2)
  #temp_img = cv2.erode(thresh,kernel,iterations=2)	
  word_img = cv2.dilate(temp_img,kernel2,iterations=1)

  (contours, _) = cv2.findContours(word_img.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

  for cnt in contours:
    x,y,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(output,(x-1,y-5),(x+w,y+h),(0,255,0),1)

  return output	

def process_line(thresh,output):	
  print("Processing line by line boxing")
  # assign a rectangle kernel size 1 vertical and the other will be horizontal
  kernel = np.ones((1,5), np.uint8)
  kernel2 = np.ones((2,4), np.uint8)	
  # use closing morph operation but fewer iterations than the letter then erode to narrow the image	
  temp_img = cv2.morphologyEx(thresh,cv2.MORPH_CLOSE,kernel2,iterations=2)
  #temp_img = cv2.erode(thresh,kernel,iterations=2)	
  line_img = cv2.dilate(temp_img,kernel,iterations=5)

  (contours, _) = cv2.findContours(line_img.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

  for cnt in contours:
    x,y,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(output,(x-1,y-5),(x+w,y+h),(0,255,0),1)

  return output	

def process_par(thresh,output):	
  print("Processing par by par boxing")
  # assign a rectangle kernel size
  kernel = np.ones((5,5), 'uint8')	
  par_img = cv2.dilate(thresh,kernel,iterations=3)

  (contours, _) = cv2.findContours(par_img.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

  for cnt in contours:
    x,y,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(output,(x,y),(x+w,y+h),(0,255,0),1)

  return output	

def process_margin(thresh,output):	
  print("Processing margin with paragraph boxing")
  # assign a rectangle kernel size
  kernel = np.ones((20,5), 'uint8')	
  margin_img = cv2.dilate(thresh,kernel,iterations=5)

  (contours, _) = cv2.findContours(margin_img.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

  for cnt in contours:
    x,y,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(output,(x,y),(x+w,y+h),(0,255,0),1)

  return output

print("Processing and writing the output")
output1_letter = process_letter(th1,output1_letter)
output1_word = process_word(th1,output1_word)
output1_line = process_line(th1,output1_line)

print("Special case for the 5th output because margin with paragraph is just the 4th output with margin")
cv2.imwrite("./TRY004-output/letter/output1_letter.jpg", output1_letter)	
cv2.imwrite("./TRY004-output/word/output1_word.jpg", output1_word)
cv2.imwrite("./TRY004-output/line/output1_line.jpg", output1_line)
output1_par = process_par(th1,output1_par)
cv2.imwrite("./TRY004-output/par/output1_par.jpg", output1_par)
output1_margin = process_margin(th1,output1_par)
cv2.imwrite("./TRY004-output/margin/output1_margin.jpg", output1_par)

output2_letter = process_letter(th2,output2_letter)
output2_word = process_word(th2,output2_word)
output2_line = process_line(th2,output2_line)

cv2.imwrite("./TRY004-output/letter/output2_letter.jpg", output2_letter)	
cv2.imwrite("./TRY004-output/word/output2_word.jpg", output2_word)
cv2.imwrite("./TRY004-output/line/output2_line.jpg", output2_line)
output2_par = process_par(th2,output2_par)
cv2.imwrite("./TRY004-output/par/output2_par.jpg", output2_par)
output2_margin = process_margin(th2,output2_par)
cv2.imwrite("./TRY004-output/margin/output2_margin.jpg", output2_par)

output3_letter = process_letter(th3,output3_letter)
output3_word = process_word(th3,output3_word)
output3_line = process_line(th3,output3_line)

cv2.imwrite("./TRY004-output/letter/output3_letter.jpg", output3_letter)	
cv2.imwrite("./TRY004-output/word/output3_word.jpg", output3_word)
cv2.imwrite("./TRY004-output/line/output3_line.jpg", output3_line)
output3_par = process_par(th3,output3_par)
cv2.imwrite("./TRY004-output/par/output3_par.jpg", output3_par)
output3_margin = process_margin(th3,output3_par)
cv2.imwrite("./TRY004-output/margin/output3_margin.jpg", output3_par)

output4_letter = process_letter(th4,output4_letter)
output4_word = process_word(th4,output4_word)
output4_line = process_line(th4,output4_line)

cv2.imwrite("./TRY004-output/letter/output4_letter.jpg", output4_letter)	
cv2.imwrite("./TRY004-output/word/output4_word.jpg", output4_word)
cv2.imwrite("./TRY004-output/line/output4_line.jpg", output4_line)
output4_par = process_par(th4,output4_par)
cv2.imwrite("./TRY004-output/par/output4_par.jpg", output4_par)
output4_margin = process_margin(th4,output4_par)
cv2.imwrite("./TRY004-output/margin/output4_margin.jpg", output4_par)

output5_letter = process_letter(th5,output5_letter)
output5_word = process_word(th5,output5_word)
output5_line = process_line(th5,output5_line)

cv2.imwrite("./TRY004-output/letter/output5_letter.jpg", output5_letter)	
cv2.imwrite("./TRY004-output/word/output5_word.jpg", output5_word)
cv2.imwrite("./TRY004-output/line/output5_line.jpg", output5_line)
output5_par = process_par(th5,output5_par)
cv2.imwrite("./TRY004-output/par/output5_par.jpg", output5_par)
output3_margin = process_margin(th5,output5_par)
cv2.imwrite("./TRY004-output/margin/output5_margin.jpg", output5_par)

print("Display results")
# cv2.imshow("output letter", output1_letter)
# cv2.imshow("output word", output1_word)
# cv2.imshow("output line", output1_line)
# cv2.imshow("output par", output1_par)
# cv2.imshow("output margin", output1_par)

# cv2.waitKey(0)

