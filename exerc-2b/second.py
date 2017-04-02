import cv2
import numpy as np

img_a_bordered_path = './a_bordered.png'
img_b_bordered_path = './b_bordered.png'

img_a_transformed_path = './a_transformed.png'

img_a_bordered = cv2.imread(img_a_bordered_path,0)
x,y = img_a_bordered.shape
img_b_bordered = cv2.imread(img_b_bordered_path,0)

# manually collected coordinates
img_a_1 = [328,308]
img_b_1 = [201,69]

img_a_2 = [134,158]
img_b_2 = [411,190]

img_a_3 = [420,172]
img_b_3 = [125,217]

points_img_a = np.float32([img_a_1, img_a_2, img_a_3])
points_img_b = np.float32([img_b_1, img_b_2, img_b_3])

affine_a = cv2.getAffineTransform(points_img_a, points_img_b)
img_a_transformed = cv2.warpAffine(img_a_bordered, affine_a, (y,x))
cv2.imwrite(img_a_transformed_path, img_a_transformed)

img_b_difference = cv2.subtract(img_b_bordered, img_a_transformed)
cv2.imwrite('b_difference.png', img_b_difference)

img_b_difference_equa = cv2.equalizeHist(img_b_difference)
cv2.imwrite('b_difference_equa.png', img_b_difference_equa)
