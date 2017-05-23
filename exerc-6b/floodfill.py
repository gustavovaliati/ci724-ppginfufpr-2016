#!/usr/bin/python

import numpy as np
import cv2,sys,random

img_original = cv2.imread('cells.jpg')
img_gray = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)

ret, th = cv2.threshold(img_gray, 0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)

print ret
cv2.imwrite("otsu.png", th)

'''
Achar contornos.
Preencher contornos
passar fazendo floodFill em cada pixel, jogando em outra imagem com label e calculando a area.
'''

thresh = abs(th - 255)
img_c, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
img_contours = np.copy(th)
cv2.drawContours(img_contours, contours, -1, (0,0,0), -1) #find contours and fill then with black
cv2.imwrite("contornado.png", img_contours)

# for c in contours:
#     print c
#     area = cv2.contourArea(c)
#     print area
#     print th[440,103]
#     sys.exit()
#
# sys.exit()

h, w = th.shape[:2]
print "shape",h,w
diff = (6,6,6)
print "diff",diff

img_final = np.zeros((h,w,3),np.uint8)
img_final[:,:,0] = img_contours
img_final[:,:,1] = img_contours
img_final[:,:,2] = img_contours

for i,contour in enumerate(contours):

    #get the first (could be any) coord. for this contour
    # print contour
    y,x = contour[0][0]
    area = cv2.contourArea(contour)

    print "Element {} found on {},{} with area of {}".format(i,y,x,area)
    # sys.exit()
    mask = np.zeros((h+2,w+2),np.uint8)

    b = random.randint(1, 255)
    g = random.randint(1, 255)
    r = random.randint(1, 255)

    cv2.floodFill(img_final, mask, (y,x), (b,g,r),diff,diff)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img_final,str(i),(y,x), font, 0.25,(0,0,0), 1,cv2.LINE_AA)
    # cv2.imwrite("processing/flooding-{}.png".format(i), img_final)
    # cv2.imwrite("processing/mask-{}.png".format(i), mask*255)

    # if i == 2: sys.exit()

cv2.imwrite("out.png", img_final)
