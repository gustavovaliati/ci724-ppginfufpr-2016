#!/usr/bin/python

from PIL import Image
from numpy.fft import rfft2, irfft2
import numpy as np
import cv2

def save_dims(ft, low, high, name):
	ft2 = np.zeros_like(ft)
	# copy the frequencies from low to high but all others stay zero.
	ft2[low:high, low:high] = ft[low:high, low:high]
	save(ft2, name)

def save(ft, name):
	rft = irfft2(ft)
	img = Image.fromarray(rft)
	img = img.convert('L')
	img.save(name)

def main():
	# Convert input into grayscale and save.
	img = Image.open("../images/lena-color.png")
	img = img.convert('L')
	img.save('input_gray.png')
	# Do Fourier Transform on image.
	ft = rfft2(img)
	# Take only zeroth frequency and do Inverse FT and save.
	save_dims(ft, 0, 1, 'output_0.png')
	# Take first two frequencies in both directions.
	save_dims(ft, 0, 2, 'output_1.png')
	save_dims(ft, 0, 3, 'output_2.png')
	# Take first 50% of frequencies.
	x = min(ft.shape)
	save_dims(ft, 0, x/2, 'output_50p.png')

def generateGif():
	''' Generates images to be later converted to a gif.
	This requires ImageMagick:
	convert -delay 100 -loop 0 output_*.png animation.gif
	'''
	# Requires images2gif from code.google.com/p/visvis/source/browse/vvmovie/images2gif.py
	# from images2gif import writeGif

	img = Image.open('../images/lena-color.png')
	img = img.convert('L')
	# Resize image before any calculation.
	size = (640,480)
	img.thumbnail(size, Image.ANTIALIAS)
	ft = rfft2(img)
	# f = np.fft.fft2(img)
	fshift = np.fft.fftshift(ft)
	magnitude_spectrum = 20*np.log(np.abs(fshift))
	cv2.imwrite("./freq_original.png", magnitude_spectrum)

	images = []
	for x in range(0, max(ft.shape)+1):
		ft2 = np.zeros_like(ft)
		ft2[0:x, 0:x] = ft[0:x,0:x]
		fshift = np.fft.fftshift(ft2)
		magnitude_spectrum = 20*np.log(np.abs(fshift))
		cv2.imwrite("./test/freq_{}.png".format(x), magnitude_spectrum)
		rft = irfft2(ft2)
		img_out = Image.fromarray(rft).convert('L')
		fname = 'animation/output_%05d.jpg' %(x, )
		img_out.save(fname, quality=60, optimize=True)

	#writeGif('animation.gif', images, duration=0.2)


if __name__=='__main__':
	main()
	generateGif()
