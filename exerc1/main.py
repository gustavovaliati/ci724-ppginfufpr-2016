#!/usr/bin/python

import cv2
import numpy as np
import sys, getopt

img = None
new_img = None
gray_slice = 0
gray_max = 0
gray_scale = 0

def printHelp():
    print 'main.py\n -i <image>\n -o <output image>\n -p <percent>\n -g <gray>\n -t <technic: mean>'

def main(argv):
    global gray_scale
    image_path = ''
    percent = 0.0
    technic = ''
    output_path = ''

    try:
        opts, args = getopt.getopt(argv,"hi:p:g:t:o")
    except getopt.GetoptError:
        printHelp()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            printHelp()
            sys.exit()
        elif opt in ("-i"):
            image_path = arg
        elif opt in ("-p"):
            percent = float(arg)
        elif opt in ("-g"):
            gray_scale = int(arg)
        elif opt in ("-t"):
            technic = arg
        elif opt in ("-o"):
            output_path = arg

    process(image_path=image_path, percent=percent, gray_scale=gray_scale, output_path=output_path, technic=technic)


def calculateWindow(y1,y2,x1,x2):
    global img
    global new_img
    window_orig = img[y1:y2,x1:x2]
    tmp = np.zeros([y2-y1+1,x2-x1+1],dtype=np.uint8)
    tmp.fill(calculateGray(window_orig.mean()))
    new_img[y1:y2+1,x1:x2+1] = tmp

def calculateGray(value):
    new_color_sector = int ((value * gray_scale)/gray_max)
    return (new_color_sector * gray_slice)

def process(image_path, percent, gray_scale, output_path, technic):
    global img
    global new_img
    global gray_slice
    global gray_max

    img = cv2.imread(image_path, 0)
    y, x = img.shape
    new_img = np.empty([y,x])

    percent = percent
    y_wsize = int(y * percent) # window size
    x_wsize = int(x * percent) # window size
    print("Window size width {} x height {} pixels").format(x_wsize, y_wsize)

    #-- Gray scale

    gray_min = img.min()
    gray_max = img.max()

    print("Detected gray min of {} and max of {}").format(gray_min, gray_max)

    gray_scale = int(gray_scale)
    gray_slice = gray_max / gray_scale;

    current_y = 0
    current_x = 0

    while (current_y < y):
        new_y = current_y + y_wsize;
        if new_y > y:
            new_y = y

        while (current_x < x):
            new_x = current_x + x_wsize;
            if new_x > x:
                new_x = x

            calculateWindow(current_y, new_y-1, current_x, new_x-1);

            current_x = new_x

        current_x = 0
        current_y = new_y

    cv2.imwrite('output/out.png',new_img)

if __name__ == "__main__":
    main(sys.argv[1:])
