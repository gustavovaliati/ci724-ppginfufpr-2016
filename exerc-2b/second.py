import cv2
import numpy as np

img_a_bordered_path = './a_bordered.png'
img_b_bordered_path = './b_bordered.png'
img_a_transformed_path = './a_transformed.png'
img_final_result = './final_result.png'

img_a_bordered = cv2.imread(img_a_bordered_path,0)
x,y = img_a_bordered.shape
img_b_bordered = cv2.imread(img_b_bordered_path,0)

# manually collected coordinates

img_a_1 = [328,308]
img_b_1 = [201,69]

img_a_2 = [135,157]
img_b_2 = [411,190]

img_a_3 = [421,173]
img_b_3 = [127,214]

points_img_a = np.float32([img_a_1, img_a_2, img_a_3])
points_img_b = np.float32([img_b_1, img_b_2, img_b_3])

affine_a = cv2.getAffineTransform(points_img_a, points_img_b)
img_a_transformed = cv2.warpAffine(img_a_bordered, affine_a, (y,x), borderMode=cv2.BORDER_TRANSPARENT)
cv2.imwrite(img_a_transformed_path, img_a_transformed)

img_b_difference = cv2.subtract(img_b_bordered, img_a_transformed)
cv2.imwrite(img_final_result, img_b_difference)

# img_b_difference_equa = cv2.equalizeHist(img_b_difference)
# cv2.imwrite('b_difference_equa.png', img_b_difference_equa)

hist = cv2.calcHist([img_b_difference],[0] ,None,[256],[0,256])
total = x*y
difference = total - hist[0]
print "Total pixel quantity is {}. The number of different pixels is {}.".format(total, difference)
print "Check out {} .".format(img_final_result) 
