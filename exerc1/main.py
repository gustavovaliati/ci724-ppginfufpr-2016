#!/usr/bin/python

import cv2
import numpy as np
import sys, getopt
import datetime

img = None
new_img = None
gray_slice = 0
gray_max = 0
gray_scale = 0

image_path = None
percent = 0.0
technic = 'mean'
output_path = "./out_{}.png".format(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
tech_func = None

def printHelp():
    print 'main.py\n' \
    ' -i <Image Path. Ex: /home/myImage.jpg > (Mandatory)\n' \
    ' -p <Sample Percentage: sets the new pixel window according to the original image resolution . Range: ~0.0001 to 1.0 > (Mandatory)\n' \
    ' -o <Output Image Path. Default: "./out_[datetime].png" > (Optional)\n' \
    ' -g <Number of shades of gray. Ex: 8. Default: original image value. > (Optional)\n' \
    ' -t <Technic to calculate the new pixel window color. Options: [mean , median , mode] . Default: mean. > (Optional)\n' \
    ' \n Example: python main.py -i myOriginalImage.jpg -p 0.03 -g 16 \n '

def calculateWindow(y1,y2,x1,x2):
    global img
    global new_img
    window_orig = img[y1:y2+1,x1:x2+1]
    tmp = np.zeros([y2-y1+1,x2-x1+1],dtype=np.uint8)
    tmp.fill(calculateGray( tech_func(window_orig) ))
    new_img[y1:y2+1,x1:x2+1] = tmp

def calculateGray(value):
    new_color_sector = int ((value * gray_scale)/gray_max)
    return (new_color_sector * gray_slice)

def calcMode(array):
    tmp = np.reshape(array, (1, array.size))[0]

    # begin of debug - uncomment bellow

    # print array
    # print tmp
    # print np.bincount(tmp)
    # print np.argmax(np.bincount(tmp))
    # sys.exit()

    #end of debug

    return np.argmax(np.bincount(tmp))

def getTechnic(key):
    if key == 'mean':
        return np.mean
    elif key == 'mode':
        return calcMode
    elif key == 'median':
        return np.median
    else:
        print "Technic not found."
        sys.exit()

def process(image_path, percent, l_gray_scale, output_path, technic):
    global img
    global new_img
    global gray_slice
    global gray_max
    global gray_scale
    global tech_func

    print("Technic: {}").format(technic)
    tech_func = getTechnic(technic)

    print("Input image: {}").format(image_path)
    img = cv2.imread(image_path, 0)
    y, x = img.shape
    new_img = np.empty([y,x])

    percent = percent
    print("Sample Percentage: {}").format(percent)
    y_wsize = int(y * percent) # window size
    x_wsize = int(x * percent) # window size
    print("New pixel window: width {} x height {} pixels.").format(x_wsize, y_wsize)
    if not ( (0 < x_wsize <= x ) or (0 < y_wsize <= y) ):
        print "Pixel window should be at least 1 pixel and not greater than maximum dimensions: {}x{}".format(x,y)
        sys.exit()

    #-- Gray scale

    gray_min = img.min()
    gray_max = img.max()

    if l_gray_scale > 0:
        gray_scale = int(l_gray_scale)
    else:
        gray_scale = gray_max

    print("Number of colors: {}").format(gray_scale)

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

    print("Output file: {}").format(output_path)
    cv2.imwrite(output_path, new_img)


# START

try:
    opts, args = getopt.getopt(sys.argv[1:],"hi:p:g:t:o:")
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

process(image_path, percent, gray_scale, output_path, technic)
