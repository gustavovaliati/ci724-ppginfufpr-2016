#!/usr/bin/python
# test http://stackoverflow.com/questions/14873203/plotting-of-1-dimensional-gaussian-distribution-function

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

img = cv2.imread(args["image"], 0)
y_original,x_original = img.shape
padding = int(filterSize/2)
img = np.lib.pad(img, (padding, padding), 'symmetric')
y_padded,x_padded = img.shape
new_img = np.zeros([y_padded,x_padded],dtype=np.uint8)


if ( filterSize < 0 or (filterSize % 2) == 0 ):
    print "The filter size must be odd and positive"
    sys.exit()

time_start = datetime.datetime.now()


finalKernel = np.zeros((filterSize,filterSize))

def gaussianFunc(x,y,sigma):
    print x,y,sigma
    # versao slide professor
    # a = 1
    # r = -1 * ( ((x ** 2) +  (y ** 2)) / ( 2 * (sigma ** 2) ) )
    # print a ** r

max = int(filterSize / 2) # Ex. 5. -> 5/2=2.5 -> int(2.5)=2 -> -2,-1,0,1,2
start = -1 * max

cur_x = cur_y = start
print start, max

while cur_x <= max:
    while cur_y <= max:
        '''
        Ex. Filter size = 5 -> max = 2
        To find matrix position:
        cur_x + max = matrix_pos
        -2 + 2 = 0
        -1 + 2 = 1
        0 + 2 = 2
        1 + 2 = 3
        2 + 2 = 4
        '''
        finalKernel[cur_y + max, cur_x + max] = gaussianFunc(cur_x,cur_y,sigma)
        cur_y = cur_y+1
    cur_y = start
    cur_x = cur_x+1

print finalKernel

time_end = datetime.datetime.now()
cv2.imwrite("./out_{}.png".format(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")),new_img[padding:y_original+padding, padding:x_original+padding])
print "Executed in {}".format(time_end - time_start)
