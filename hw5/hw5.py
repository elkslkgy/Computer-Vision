import cv2
import numpy as np

def dilation(img, kernel):
	dil = np.zeros(img.shape, int)
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			maxValue = img[i][j]
			for dot in kernel:
				x = dot[0]
				y = dot[1]
				if i + x >= 0 and i + x < img.shape[0] \
				and j + y >= 0 and j + y < img.shape[1]:
					if img[i + x][j + y] > maxValue:
						maxValue = img[i + x][j + y]
			dil[i][j] = maxValue
	return dil

def erosion(img, kernel):
	ero = np.zeros(img.shape, int)
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			minValue = img[i][j]
			for dot in kernel:
				x = dot[0]
				y = dot[1]
				if i + x >= 0 and i + x < img.shape[0] \
				and j + y >= 0 and j + y < img.shape[1]:
					if img[i + x][j + y] < minValue:
						minValue = img[i + x][j + y]
			ero[i][j] = minValue
	return ero

octagonal = [[-2, -1], [-2, 0], [-2, 1], 
			[-1, -2], [-1, -1], [-1, 0], [-1, 1], [-1, 2], 
			[0, -2], [0, -1], [0, 0], [0, 1], [0, 2], 
			[1, -2], [1, -1], [1, 0], [1, 1], [1, 2], 
			[2, -1], [2, 0], [2, 1]]

image = cv2.imread('lena.bmp', 0)

# Dilation
dil = dilation(image, octagonal)
cv2.imwrite('dilation.png', dil)

# Erosion
ero = erosion(image, octagonal)
cv2.imwrite('erosion.png', ero)

# Opening
opening = dilation(erosion(image, octagonal), octagonal)
cv2.imwrite('opening.png', opening)

# Closing
closing = erosion(dilation(image, octagonal), octagonal)
cv2.imwrite('closing.png', closing)


