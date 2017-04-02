#!/usr/bin/python

import cv2
import numpy as np
import sys, getopt
import matplotlib
matplotlib.use('Agg') # Force matplotlib to not use any Xwindows backend.
from matplotlib import pyplot as plt
import datetime

image_path = None
window_size = None

def printHelp():
    print 'main.py\n' \
    ' -i <Image Path. Ex: /home/myImage.jpg > (Mandatory)\n' \
    ' -w <Window size. Ex: 8 . This is going to generate a window of 8x8 pixels > (Mandatory)\n' \
    ' \n Example: python main.py -i myOriginalImage.jpg -w 8 \n '

try:
    opts, args = getopt.getopt(sys.argv[1:],"hi:w:")
except getopt.GetoptError:
    printHelp()
    sys.exit(2)

for opt, arg in opts:
    if opt == '-h':
        printHelp()
        sys.exit()
    elif opt in ("-i"):
        image_path = arg
    elif opt in ("-w"):
        window_size = int(arg)

if (image_path == None) or (window_size == None):
    print "Missing parameters"
    printHelp()
    sys.exit()
if ( (window_size % 2) == 0 ):
    print "The window size must be odd."
    sys.exit()

img = cv2.imread(image_path, 0)
y,x = img.shape

if not ( ( 3 <= window_size <= x) or ( 3 <= window_size <= y ) ):
    print "The window size is incoherent"
    sys.exit()


x_current = 0
y_current = 0
window_pixels = window_size * window_size
new_img = np.zeros([y,x],dtype=np.uint8)

for y_current in range(y):
    y_next_window = y_current + window_size
    if y_next_window > y :
        y_next_window = y

    for x_current in range(x):
        x_next_window = x_current + window_size
        if x_next_window > x :
            x_next_window = x

        # print x_current, y_current

        window = img[y_current:y_next_window, x_current:x_next_window]
        # print window
        l_y, l_x = window.shape
        map = {}
        for i in range(l_y):
            for j in range(l_x):
                l_color = window[i,j]
                if l_color in map:
                    map[l_color] = map[l_color] + 1
                else:
                    map[l_color] = 1

        l_comulative = 0.0
        for key in map:
            intensity = float(map[key])
            prob = (intensity / window_pixels) * 256
            l_comulative = l_comulative + prob
            map[key] = l_comulative

        # print map

        middle_window_x = (l_x) / 2
        middle_window_y = (l_y) / 2

        # print "middle_window",middle_window_y, middle_window_x
        middle_img_y = y_current + ( (y_next_window - y_current) / 2 )
        middle_img_x = x_current + ( (x_next_window - x_current) / 2 )

        # print "middle_img", middle_img_y, middle_img_x
        # print new_img[middle_img_y, middle_img_x]
        # print map[window[middle_window_y, middle_window_x]]


        new_img[middle_img_y, middle_img_x] = int (map[window[middle_window_y, middle_window_x]])
        # print new_img[middle_img_y, middle_img_x]

cv2.imwrite("./out_{}.png".format(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")),new_img)
