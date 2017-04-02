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
    ' \n Example: python main.py -i myOriginalImage.jpg\n '

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

if (image_path == None):
    print "Missing parameters"
    printHelp()
    sys.exit()

img = cv2.imread(image_path, 0)

hist = cv2.calcHist([img],[0],None,[256],[0,256])
plt.plot(hist, label="Original")
plt.xlim([0,256])
plt.savefig("orig-hist.png")

y,x = img.shape
total_pixels = y*x
comulative_prob = 0.0

map = {}
prob_cumulative_hist = []
for c,i in enumerate(hist):
    pixels = i[0]

    prob = None
    if pixels > 0:
        prob = pixels/total_pixels
    else:
        prob = 0

    comulative_prob = comulative_prob + prob

    # debug map
    #map[c] = {"color" : c, "pixels" : pixels, "probability": prob, "comulative_prob": comulative_prob, "new_color": int(comulative_prob * 256)}

    prob_cumulative_hist.append(comulative_prob)
    map[c] = int(comulative_prob * 256)

new_img = np.zeros([y,x],dtype=np.uint8)

for x_coord in range(x):
    for y_coord in range(y):
        orig_color = img[y_coord,x_coord]
        new_img[y_coord,x_coord] = map[orig_color]

cv2.imwrite("out.png", new_img)

new_hist = cv2.calcHist([new_img],[0],None,[256],[0,256])
plt.xlim([0,256])
plt.plot(new_hist, label="Normalized")
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
plt.savefig("new-hist.png")


plt.clf() #clear

new_prob_cumulative_hist = []
new_comulative_prob = 0.0
for c,i in enumerate(new_hist):
    pixels = i[0]

    prob = None
    if pixels > 0:
        prob = pixels/total_pixels
    else:
        prob = 0

    new_comulative_prob = new_comulative_prob + prob
    new_prob_cumulative_hist.append(new_comulative_prob)


plt.xlim([0,256])
plt.plot(prob_cumulative_hist, label="Original Prob. Comul.")
plt.plot(new_prob_cumulative_hist, label="New Prob. Comul.")
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
plt.savefig("comulative_freq.png")
