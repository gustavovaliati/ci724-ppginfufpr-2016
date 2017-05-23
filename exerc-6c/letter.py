#!/usr/bin/python

import numpy as np
import cv2,sys,random

import matplotlib
matplotlib.use('Agg') # Force matplotlib to not use any Xwindows backend.
from matplotlib import pyplot as plt

'''
A carta tem 23 linhas
'''

img_original = cv2.imread('carta.png')
img_gray = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)

ret, th = cv2.threshold(img_gray, 0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)

cv2.imwrite("1-otsu.png", th)

inverted = abs(255 - th)

cv2.imwrite("2-inverted.png", inverted)

h,w = inverted.shape

hist = []

for i in range(h):
    line = inverted[i,:]
    hist.append(cv2.countNonZero(line))

plt.plot(hist)
plt.xlim([0,h-1])
plt.savefig("3-hist.png")

minimum = 26 # minimum of pixels to consider as line
inside_line = False
line_counter = 0
for val in hist:
    if val > minimum and not inside_line:
        line_counter = line_counter + 1
        inside_line = True
    elif val < minimum:
        #this is not a line anymore
        inside_line = False

print "The image has around {} lines of text".format(line_counter)
