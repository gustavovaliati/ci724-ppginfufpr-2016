import numpy as np
import cv2

img = cv2.imread('../orig-img.png',0)

clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
cl1 = clahe.apply(img)

cv2.imwrite('out.jpg',cl1)
