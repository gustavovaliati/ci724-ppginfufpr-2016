#!/usr/bin/python

import cv2, sys, argparse, datetime
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--filter", required = True, help = "Is the filter size.")
ap.add_argument("-i", "--image", required = True, help = "Is the input image.")
ap.add_argument("-o", "--output", required = False, help = "Is the output image.")
args = vars(ap.parse_args())

filterSize = int(args["filter"])

img = cv2.imread(args["image"])
y_original,x_original,z = img.shape

blue = img[:,:,0]
green = img[:,:,1]
red = img[:,:,2]

padding = int(filterSize/2)
blue = np.lib.pad(blue, (padding, padding), 'symmetric')
green = np.lib.pad(green, (padding, padding), 'symmetric')
red = np.lib.pad(red, (padding, padding), 'symmetric')

if ( filterSize < 0 or (filterSize % 2) == 0 ):
    print "The filter size must be odd and positive"
    sys.exit()

time_start = datetime.datetime.now()

def processWindow(window):
    # print window
    return np.median(window)

x_current = 0
y_current = 0

for y_current in range(y_original):
    y_center = y_current + padding
    for x_current in range(x_original):
        x_center = x_current + padding
        b = processWindow(blue[ y_current: y_center+padding+1, x_current:x_center+padding+1])
        g = processWindow(green[ y_current: y_center+padding+1, x_current:x_center+padding+1])
        r = processWindow(red[ y_current: y_center+padding+1, x_current:x_center+padding+1])
        img[y_current,x_current] = (b,g,r)

time_end = datetime.datetime.now()
cv2.imwrite("./out_{}.png".format(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")),img)
print "Executed in {}".format(time_end - time_start)
