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
y_original,x_original = img.shape
padding = int(filterSize/2)
img = np.lib.pad(img, (padding, padding), 'symmetric')
y_padded,x_padded = img.shape
new_img = np.zeros([y_original,x_original],dtype=np.uint8)


if ( filterSize < 0 or (filterSize % 2) == 0 ):
    print "The filter size must be odd and positive"
    sys.exit()

time_start = datetime.datetime.now()


def makeGaussian(size, fwhm = 3, center=None):
    """ Make a square gaussian kernel.
    size is the length of a side of the square
    fwhm is full-width-half-maximum, which
    can be thought of as an effective radius.
    """
    print fwhm
    x = np.arange(0, size, 1, float)
    # print x
    y = x[:,np.newaxis]
    # print y
    if center is None:
        x0 = y0 = size // 2
    else:
        x0 = center[0]
        y0 = center[1]
    # print x0,y0

    return np.exp(-4*np.log(2) * ((x-x0)**2 + (y-y0)**2) / fwhm**2)

def makeGaussian2(sigma, size):
    sigma_x = sigma
    sigma_y = sigma

    ax = np.arange(-size // 2 + 1., size // 2 + 1.)
    # print ax
    x, y = np.meshgrid(ax, ax)
    # print x
    # print y
    return (1/(2*np.pi*sigma_x*sigma_y) * np.exp(-(x**2/(2*sigma_x**2) + y**2/(2*sigma_y**2))))


kernel = makeGaussian2(sigma,filterSize)
print kernel
new_img = cv2.filter2D(img, -1, kernel)

time_end = datetime.datetime.now()
cv2.imwrite("./out_sigma{}_filter{}_{}.png".format(sigma,filterSize,datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")),new_img)
print "Executed in {}".format(time_end - time_start)
