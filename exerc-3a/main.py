#!/usr/bin/python

import cv2
import numpy as np
import sys, getopt
import matplotlib
matplotlib.use('Agg') # Force matplotlib to not use any Xwindows backend.
from matplotlib import pyplot as plt

image_path = None

def printHelp():
    print 'main.py\n' \
    ' -i <Image Path. Ex: /home/myImage.jpg > (Mandatory)\n' \
    ' \n Example: python main.py -i myOriginalImage.jpg \n '

try:
    opts, args = getopt.getopt(sys.argv[1:],"hi:")
except getopt.GetoptError:
    printHelp()
    sys.exit(2)

for opt, arg in opts:
    if opt == '-h':
        printHelp()
        sys.exit()
    elif opt in ("-i"):
        image_path = arg

if image_path == None:
    print "Input file missing"
    printHelp()
    sys.exit()

img = cv2.imread(image_path)
color = ('b','g','r')
for i,col in enumerate(color):
    hist = cv2.calcHist([img],[i],None,[256],[0,256])
    plt.plot(hist,color = col)
    plt.xlim([0,256])

plt.savefig("hist.png")
