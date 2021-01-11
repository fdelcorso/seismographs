# This function resizes the image dimensions about 60% using OpenCV

import cv2
from numpy import save
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('C:\\temp\\cavia.png', cv2.IMREAD_UNCHANGED)
img1 = cv2.imread('C:\\temp\\cavia-subtract.png', cv2.IMREAD_UNCHANGED)
img_dir = "C\\temp\\"

#print('Original Dimensions : ',img.shape)
 
scale_percent = 60 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
# resize image
resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

#print('Resized Dimensions : ',resized.shape)
 
cv2.imshow("Resized image", resized)

cv2.waitKey(0)
cv2.destroyAllWindows()

status = cv2.imwrite('C:\\temp\\resized.png',resized)
#print("Image written to file-system : ",status) 

#################################################################

lines_removed = cv2.subtract(img1, img)

cv2.imshow("Immagine ripulita", lines_removed) 

cv2.waitKey(0)
cv2.destroyAllWindows()
