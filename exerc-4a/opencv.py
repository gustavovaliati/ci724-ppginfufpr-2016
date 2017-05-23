#!/usr/bin/python

import cv2, sys, argparse, datetime, math
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-s", "--sigma", required = True, help = "Is sigma value for the standard deviation.")
ap.add_argument("-f", "--filter", required = True, help = "Is the filter size.")
ap.add_argument("-i", "--image", required = True, help = "Is the input image.")
ap.add_argument("-o", "--output", required = False, help = "Is the output image.")
args = vars(ap.parse_args())

filterSize = int(args["filter"])
sigma = float(args["sigma"])
img = cv2.imread(args["image"],0)

if ( filterSize < 0 or (filterSize % 2) == 0 ):
    print "The filter size must be odd and positive"
    sys.exit()

time_start = datetime.datetime.now()

new_img = cv2.GaussianBlur(src=img, sigmaX=sigma, sigmaY=sigma, ksize=(filterSize,filterSize))

time_end = datetime.datetime.now()
cv2.imwrite("./out_opencv_sigma{}_filter{}_{}.png".format(sigma,filterSize,datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")),new_img)
print "Executed in {}".format(time_end - time_start)
