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

time_start = datetime.datetime.now()

img = cv2.imread(image_path, 0)
y_original,x_original = img.shape

padding = int(window_size/2)
img = np.lib.pad(img, (padding, padding), 'symmetric')

y,x = img.shape

if not ( ( 3 <= window_size <= x) or ( 3 <= window_size <= y ) ):
    print "The window size is incoherent"
    sys.exit()


x_current = 0
y_current = 0
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
        # print x_next_window, y_next_window

        window = img[y_current:y_next_window, x_current:x_next_window]
        l_y, l_x = window.shape
        window_pixels = l_y * l_x
        # map = {}
        # for i in range(l_y):
        #     for j in range(l_x):
        #         l_color = window[i,j]
        #         if l_color in map:
        #             map[l_color] = map[l_color] + 1
        #         else:
        #             map[l_color] = 1
        # print window
        window = cv2.equalizeHist(window)
        # hist = cv2.calcHist([window],[0] ,None,[256],[0,256])
        # plt.plot(hist,color = 'b')

        # # print hist
        # map = {}
        # # print hist
        # l_comulative = 0.0
        # for index, key in enumerate(hist):
        #     # print index
        #     intensity = hist[index]
        #     # print intensity
        #     if intensity > 0 :
        #         intensity = float(intensity)
        #         prob = (intensity / window_pixels) * 256
        #         l_comulative = l_comulative + prob
        #         map[index] = l_comulative

        # print map
        # plt.plot(map,color = 'r')
        # plt.xlim([0,256])
        # plt.savefig("hist.png")
        # sys.exit()
        middle_window_x = (l_x) / 2
        middle_window_y = (l_y) / 2

        # print "middle_window",middle_window_y, middle_window_x
        # print img[middle_window_y,middle_window_x]
        middle_img_y = y_current + ( (y_next_window - y_current) / 2 )
        middle_img_x = x_current + ( (x_next_window - x_current) / 2 )

        # print "middle_img", middle_img_y, middle_img_x
        # print new_img[middle_img_y, middle_img_x]
        # print window[middle_window_y, middle_window_x]
        # print map[window[middle_window_y, middle_window_x]]
        # sys.exit()

        # new_img[middle_img_y, middle_img_x] = int (map[window[middle_window_y, middle_window_x]])
        new_img[middle_img_y, middle_img_x] = window[middle_window_y, middle_window_x]
        # print new_img[middle_img_y, middle_img_x]
cv2.imwrite("./out_{}.png".format(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")),new_img[padding:y_original+padding, padding:x_original+padding])

time_end = datetime.datetime.now()
print "Executed in {}".format(time_end - time_start)
