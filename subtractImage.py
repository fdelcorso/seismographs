
# Python program to subtract images. 

import cv2 
import numpy as np 
  
# Reading the input images 

img = cv2.imread('C:\\temp\\red.png', 0) 
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
flags = [i for i in dir(cv2) if i.startswith('COLOR_')]
print (flags)

#img_extracted = cv2.bitwise_and(img, img, mask=mask_inv)
cv2.imshow("Cleaned Waveform", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

#img1 =  cv2.imread('C:\\temp\\cavia-subtract.png', 0) 

# Subtract image

#lines_removed = cv2.subtract(img1, img)
#cv2.imshow("Cleaned Waveform", lines_removed) 
#cv2.waitKey(0) 
#cv2.destroyAllWindows()

# Saving the cleaned image

#status = cv2.imwrite('C:\\temp\\cavia-result3.png',lines_removed)

#print("Image written to file-system : ",status) 
