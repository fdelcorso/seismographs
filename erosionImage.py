
# Python program to demonstrate erosion and  dilation of images. 

import cv2 
import numpy as np 
  
# Reading the input images 

img = cv2.imread('C:\\temp\\cavia.png', 0) 
img1 =  cv2.imread('C:\\temp\\cavia-subtract.png', 0) 

# Subtract image

lines_removed = cv2.subtract(img, img1)
cv2.imshow("Cleaned Waveform", lines_removed) 
  
cv2.waitKey(0) 
cv2.destroyAllWindows()

# Saving the cleaned image

status = cv2.imwrite('C:\\temp\\cavia-cleaned.png',lines_removed)
print("Image written to file-system : ",status) 