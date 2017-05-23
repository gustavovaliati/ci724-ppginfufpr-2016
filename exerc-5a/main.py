#!/usr/bin/python

import cv2, sys, datetime
import numpy as np


time_start = datetime.datetime.now()

img = cv2.imread('clown.jpg',0)
f = np.fft.fft2(img)
fshift = np.fft.fftshift(f)

magnitude_spectrum = 20*np.log(np.abs(fshift))
cv2.imwrite("./freq_original.png", magnitude_spectrum)

def removeAreas(img,areas):
    for area in areas:
        a,b,c,d = area
        img[a:b+1,c:d+1] = 0
    return img

areas = [
    (111,133,188,191),
    (120,123,179,215),
    (131,140,126,127),
    (135,136,120,133),
    (155,163,167,168),
    (159,160,161,173),
    (159,182,103,106),
    (170,172,80,118)
    ]

freq_fixed = removeAreas(fshift, areas)
magnitude_spectrum = 20*np.log(np.abs(freq_fixed))
cv2.imwrite("./freq_fixed.png", magnitude_spectrum)

f_ishift = np.fft.ifftshift(freq_fixed)
img_back = np.fft.ifft2(f_ishift)
img_back = np.abs(img_back)

cv2.imwrite("./out.png", img_back)


time_end = datetime.datetime.now()
print "Executed in {}".format(time_end - time_start)
