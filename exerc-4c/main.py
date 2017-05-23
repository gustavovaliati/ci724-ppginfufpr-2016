#!/usr/bin/python

import cv2, sys, argparse, datetime
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Is the input image.")
ap.add_argument("-I", "--intensity", required = True, help = "Is noise intensity. [ 0 < intensity < 1 ]")
ap.add_argument("-o", "--output", required = False, help = "Is the output image.")
args = vars(ap.parse_args())

intensity = float(args["intensity"])
if not 0 < intensity < 1:
    print "Wrong intensity value"
    sys.exit()

img = cv2.imread(args["image"])

time_start = datetime.datetime.now()

def noisy(img):
    a = np.array(img)
    b = np.array(img)
    cv2.randn(a, (0,0,0), (50,50,50))
    return a + b

def manualNoise(img, img_size, img_shape):
    new_img = np.copy(img)
    pixels_qnty = int(intensity * img_size)
    coords = [np.random.randint(0, i - 1, pixels_qnty) for i in img_shape]
    new_img[coords] = np.random.randint(0, 254)
    return new_img


shape = img.shape
size = img.size

for i in range(10):
    sum_matrix = np.zeros(img.shape)
    for j in range(10):
        noise = manualNoise(img, size, shape)
        sum_matrix = sum_matrix + noise
        # cv2.imwrite("./out_{}_{}_{}_{}_noise.png".format(intensity, datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"),i,j),sum_matrix)
    sum_matrix = sum_matrix / 10
    cv2.imwrite("./out_{}_{}_{}_no-noise.png".format(intensity, datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"),i),sum_matrix)


time_end = datetime.datetime.now()
print "Executed in {}".format(time_end - time_start)
