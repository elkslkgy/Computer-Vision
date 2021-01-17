import cv2
import numpy as np

def dilation(img, kernel):
	dil = np.zeros(img.shape, int)
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			if img[i][j] != 0:
				for dot in kernel:
					if i + dot[0] >= 0 and i + dot[0] < img.shape[0] \
					and j + dot[1] >= 0 and j + dot[1] < img.shape[1]:
						dil[i + dot[0]][j + dot[1]] = 255
	return dil

def erosion(img, kernel):
	ero = np.zeros(img.shape, int)
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			ok = 1
			for dot in kernel:
				if i + dot[0] < 0 or i + dot[0] >= img.shape[0] \
				or j + dot[1] < 0 or j + dot[1] >= img.shape[1] \
				or img[i + dot[0]][j + dot[1]] == 0:
					ok = 0
					break
			if ok:
				ero[i][j] = 255
	return ero

def Hit_and_Miss(img, J_kernel, K_kernel):
	imgC = np.zeros(img.shape, int)
	imgC = -img + 255
	cv2.imwrite('img_comp.bmp', imgC)
	J = erosion(img, J_kernel)
	K = erosion(imgC, K_kernel)
	ham = np.zeros(img.shape, int)
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			if J[i][j] != 0 and K[i][j] != 0:
				ham[i][j] = 255
	return ham

image = cv2.imread('lena.bmp', 0)

binary = np.zeros(image.shape, int)
for i in range(image.shape[0]):
	for j in range(image.shape[1]):
		if image[i][j] >= 128:
			binary[i][j] = 255

# octagonal
# 0 1 1 1 0
# 1 1 1 1 1
# 1 1 ! 1 1
# 1 1 1 1 1
# 0 1 1 1 0
octagonal = [[-2, -1], [-2, 0], [-2, 1], 
			[-1, -2], [-1, -1], [-1, 0], [-1, 1], [-1, 2], 
			[0, -2], [0, -1], [0, 0], [0, 1], [0, 2], 
			[1, -2], [1, -1], [1, 0], [1, 1], [1, 2], 
			[2, -1], [2, 0], [2, 1]]
# Dilation
dil = dilation(binary, octagonal)
cv2.imwrite('dilation.png', dil)

# Erosion
ero = erosion(binary, octagonal)
cv2.imwrite('erosion.png', ero)

# Opening
opening = dilation(erosion(binary, octagonal), octagonal)
cv2.imwrite('opening.png', opening)

# Closing
closing = erosion(dilation(binary, octagonal), octagonal)
cv2.imwrite('closing.png', closing)

# Hit-and-miss transform
J_kernel = [[0, -1], [0, 0], [1, 0]]
K_kernel = [[-1, 0], [-1, 1], [0, 1]]

ham = Hit_and_Miss(binary, J_kernel, K_kernel)
cv2.imwrite('Hit_and_Miss.png', ham)
