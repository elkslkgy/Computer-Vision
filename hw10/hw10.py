import cv2
import numpy as np

def padding(image, row, col):
	img = np.zeros((row+2, col+2), int)
	for i in range(row+2):
		for j in range(col+2):
			if i == 0:
				if j == 0:
					img[i][j] = image[i][j]
				elif j == col + 1:
					img[i][j] = image[i][j-2]
				else:
					img[i][j] = image[i][j-1]
			elif i == row + 1:
				if j == 0:
					img[i][j] = image[i-2][j]
				elif j == col + 1:
					img[i][j] = image[i-2][j-2]
				else:
					img[i][j] = image[i-2][j-1]
			else:
				if j == 0:
					img[i][j] = image[i-1][j]
				elif j == col + 1:
					img[i][j] = image[i-1][j-2]
				else:
					img[i][j] = image[i-1][j-1]
	return img

def laplacian(image, row, col, l, thres):
	output = np.zeros((row, col), int)
	for i in range(1, row+1):
		for j in range(1, col+1):
			if np.sum(l * image[i-1: i+2, j-1: j+2]) >= thres:
				output[i-1][j-1] = 1
			elif np.sum(l * image[i-1: i+2, j-1: j+2]) <= -thres:
				output[i-1][j-1] = -1
			else:
				output[i-1][j-1] = 0
	# zero_crossing
	img = padding(output, row, col)
	for i in range(1, row+1):
		for j in range(1, col+1):
			if img[i][j] == 1 and (img[i-1][j-1] == -1 or img[i-1][j] == -1 or img[i-1][j+1] == -1 or img[i][j-1] == -1 or img[i][j+1] == -1 or img[i+1][j-1] == -1 or img[i+1][j] == -1 or img[i+1][j+1] == -1):
				output[i-1][j-1] = 0
			else:
				output[i-1][j-1] = 255
	return output

def G(image, row, col, l, thres):
	output = np.zeros((row, col), int)
	for i in range(5, row+5):
		for j in range(5, col+5):
			if np.sum(l * image[i-5: i+6, j-5: j+6]) >= thres:
				output[i-5][j-5] = 1
			elif np.sum(l * image[i-5: i+6, j-5: j+6]) <= -thres:
				output[i-5][j-5] = -1
			else:
				output[i-5][j-5] = 0
	# zero_crossing
	img = padding(output, row, col)
	for i in range(1, row+1):
		for j in range(1, col+1):
			if img[i][j] == 1 and (img[i-1][j-1] == -1 or img[i-1][j] == -1 or img[i-1][j+1] == -1 or img[i][j-1] == -1 or img[i][j+1] == -1 or img[i+1][j-1] == -1 or img[i+1][j] == -1 or img[i+1][j+1] == -1):
				output[i-1][j-1] = 0
			else:
				output[i-1][j-1] = 255
	return output

image = cv2.imread('lena.bmp', 0)

row = image.shape[0]
col = image.shape[1]

img = padding(image, row, col)

l1 = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
l2 = np.array([[1/3, 1/3, 1/3], [1/3, -8/3, 1/3], [1/3, 1/3, 1/3]])
mvl = np.array([[2/3, -1/3, 2/3], [-1/3, -4/3, -1/3], [2/3, -1/3, 2/3]])

img_l1 = laplacian(img, row, col, l1, 15)
img_l2 = laplacian(img, row, col, l2, 15)
img_mvl = laplacian(img, row, col, mvl, 20)

for i in range(5):
	img = padding(img, row+2*i, col+2*i)

loG = np.array([[0, 0, 0, -1, -1, -2, -1, -1, 0, 0, 0], 
				[0, 0, -2, -4, -8, -9, -8, -4, -2, 0, 0], 
				[0, -2, -7, -15, -22, -23, -22, -15, -7, -2, 0], 
				[-1, -4, -15, -24, -14, -1, -14, -24, -15, -4, -1], 
				[-1, -8, -22, -14, 52, 103, 52, -14, -22, -8, -1], 
				[-2, -9, -23, -1, 103, 178, 103, -1, -23, -9, -2], 
				[-1, -8, -22, -14, 52, 103, 52, -14, -22, -8, -1], 
				[-1, -4, -15, -24, -14, -1, -14, -24, -15, -4, -1], 
				[0, -2, -7, -15, -22, -23, -22, -15, -7, -2, 0], 
				[0, 0, -2, -4, -8, -9, -8, -4, -2, 0, 0], 
				[0, 0, 0, -1, -1, -2, -1, -1, 0, 0, 0]])
img_LoG = G(img, row, col, loG, 3000)

doG = np.array([[-1, -3, -4, -6, -7, -8, -7, -6, -4, -3, -1], 
				[-3, -5, -8, -11, -13, -13, -13, -11, -8, -5, -3], 
				[-4, -8, -12, -16, -17, -17, -17, -16, -12, -8, -4], 
				[-6, -11, -16, -16, 0, 15, 0, -16, -16, -11, -6], 
				[-7, -13, -17, 0, 85, 160, 85, 0, -17, -13, -7], 
				[-8, -13, -17, 15, 160, 283, 160, 15, -17, -13, -8], 
				[-7, -13, -17, 0, 85, 160, 85, 0, -17, -13, -7], 
				[-6, -11, -16, -16, 0, 15, 0, -16, -16, -11, -6], 
				[-4, -8, -12, -16, -17, -17, -17, -16, -12, -8, -4], 
				[-3, -5, -8, -11, -13, -13, -13, -11, -8, -5, -3], 
				[-1, -3, -4, -6, -7, -8, -7, -6, -4, -3, -1]])
img_DoG = G(img, row, col, doG, 1)

cv2.imwrite('img_l1.png', img_l1)
cv2.imwrite('img_l2.png', img_l2)
cv2.imwrite('img_mvl.png', img_mvl)
cv2.imwrite('img_LoG.png', img_LoG)
cv2.imwrite('img_DoG.png', img_DoG)
