import cv2
import math
import numpy as np

image = cv2.imread('lena.bmp')

# upside-down lena.bmp
upside_down = np.zeros(image.shape, int)
for i in range(image.shape[0]):
	upside_down[i] = image[image.shape[0]-1-i]

# right-side-left lena.bmp
right_side_left = np.zeros(image.shape, int)
for i in range(image.shape[0]):
	for j in range(image.shape[1]):
		right_side_left[i, j] = image[i, image.shape[1]-1-j]

# diagonally flip lena.bmp
diagonally_flip = np.zeros(image.shape, int)
for i in range(image.shape[0]):
	for j in range(image.shape[1]):
		diagonally_flip[i, j] = image[j, i]

# shrink lena.bmp in half
half_size = tuple([int(image.shape[0]/2), int(image.shape[1]/2), image.shape[2]])
half = np.zeros(half_size, int)
for i in range(int(image.shape[0]/2)):
	for j in range(int(image.shape[1]/2)):
		half[i, j] = image[i*2, j*2]

# binarize lena.bmp at 128 to get a binary image
binarize = np.zeros(image.shape, int)
for i in range(image.shape[0]):
	for j in range(image.shape[1]):
		if (image[i][j][0] * 0.299 + image[i][j][1] * 0.587 + image[i][j][2] * 0.114) > 128:
			binarize[i][j] = 255
		else:
			binarize[i][j] = 0

cv2.imwrite('upside_down.jpg', upside_down)
cv2.imwrite('right_side_left.jpg', right_side_left)
cv2.imwrite('diagonally_flip.jpg', diagonally_flip)
cv2.imwrite('half.jpg', half)
cv2.imwrite('binarize.jpg', binarize)


# ===================================================================================
# rotate_size_0 = int(image.shape[0] * (math.cos(math.pi/4) + math.sin(math.pi/4)))
# rotate_size_1 = int(image.shape[1] * (math.cos(math.pi/4) + math.sin(math.pi/4)))
# rotate_size_2 = image.shape[2]
# rotate_size = tuple([rotate_size_0, rotate_size_1, rotate_size_2])
# rotate = np.zeros(rotate_size, int)
# sin = math.sin(math.pi/4)
# cos = math.cos(math.pi/4)
# for i in range(image.shape[0]):
# 	for j in range(image.shape[1]):
# 		i_ = i - int(image.shape[0]/2)
# 		j_ = j - int(image.shape[1]/2)
# 		rotate[int(cos * i_ + sin * j_ + image.shape[0] * sin), int(-sin * i_ + cos * j_ + image.shape[0] * cos)] = image[i, j]

# cv2.imwrite('rotate.jpg', rotate)

# cv2.waitKey(0)
# cv2.destroyAllWindows()