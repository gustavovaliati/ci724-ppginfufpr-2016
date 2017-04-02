import cv2
import numpy as np

img_a = cv2.imread('./a.png',0)

# delete exceding row. Image b has only 383 lines while image a has 384.
img_a = np.delete(img_a, (383), axis=0)

img_b = cv2.imread('./b.png',0)

img_a_bordered_path = './a_bordered.png'
img_b_bordered_path = './b_bordered.png'
img_a_bordered = None
img_b_bordered = None

border = cv2.Laplacian(img_a, cv2.CV_64F, ksize=1) # TODO try different kernels
img_a_bordered =  img_a - border
cv2.imwrite(img_a_bordered_path, img_a_bordered)

border = cv2.Laplacian(img_b, cv2.CV_64F, ksize=1) # TODO try different kernels
img_b_bordered =  img_b - border
cv2.imwrite(img_b_bordered_path, img_b_bordered)
