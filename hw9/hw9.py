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

image = cv2.imread('lena.bmp', 0)

row = image.shape[0]
col = image.shape[1]

img = padding(image, row, col)

# Robert's Operator: 12
img_Robert = np.zeros((row, col), int)
for i in range(1, row+1):
	for j in range(1, col+1):
		r1 = img[i+1][j+1] - img[i][j]
		r2 = img[i+1][j] - img[i][j+1]
		thres = (r1**2 + r2**2)**0.5
		if thres >= 12:
			img_Robert[i-1][j-1] = 0
		else:
			img_Robert[i-1][j-1] = 255
cv2.imwrite('img_Robert.png', img_Robert)

# Prewitt's Edge Detector: 24
img_Prewitt = np.zeros((row, col), int)
for i in range(1, row+1):
	for j in range(1, col+1):
		p1 = img[i+1][j-1] + img[i+1][j] + img[i+1][j+1] - img[i-1][j-1] - img[i-1][j] - img[i-1][j+1]
		p2 = img[i-1][j+1] + img[i][j+1] + img[i+1][j+1] - img[i-1][j-1] - img[i][j-1] - img[i+1][j-1]
		thres = (p1**2 + p2**2)**0.5
		if thres >= 24:
			img_Prewitt[i-1][j-1] = 0
		else:
			img_Prewitt[i-1][j-1] = 255
cv2.imwrite('img_Prewitt.png', img_Prewitt)

# Sobel's Edge Detector: 38
img_Sobel = np.zeros((row, col), int)
for i in range(1, row+1):
	for j in range(1, col+1):
		s1 = img[i+1][j-1] + img[i+1][j]*2 + img[i+1][j+1] - img[i-1][j-1] - img[i-1][j]*2 - img[i-1][j+1]
		s2 = img[i-1][j+1] + img[i][j+1]*2 + img[i+1][j+1] - img[i-1][j-1] - img[i][j-1]*2 - img[i+1][j-1]
		thres = (s1**2 + s2**2)**0.5
		if thres >= 38:
			img_Sobel[i-1][j-1] = 0
		else:
			img_Sobel[i-1][j-1] = 255
cv2.imwrite('img_Sobel.png', img_Sobel)

# Frei and Chen's Gradient Operator: 30
img_FC = np.zeros((row, col), int)
for i in range(1, row+1):
	for j in range(1, col+1):
		f1 = img[i+1][j-1] + img[i+1][j]*(2**0.5) + img[i+1][j+1] - img[i-1][j-1] - img[i-1][j]*(2**0.5) - img[i-1][j+1]
		f2 = img[i-1][j+1] + img[i][j+1]*(2**0.5) + img[i+1][j+1] - img[i-1][j-1] - img[i][j-1]*(2**0.5) - img[i+1][j-1]
		thres = (f1**2 + f2**2)**0.5
		if thres >= 30:
			img_FC[i-1][j-1] = 0
		else:
			img_FC[i-1][j-1] = 255
cv2.imwrite('img_FC.png', img_FC)

# Kirsch's Compass Operator: 135
img_Kirsch = np.zeros((row, col), int)
for i in range(1, row+1):
	for j in range(1, col+1):
		k = []
		k.append((img[i-1][j+1] + img[i][j+1] + img[i+1][j+1])*5 - (img[i-1][j-1] + img[i-1][j] + img[i][j-1] + img[i+1][j-1] + img[i+1][j])*3)
		k.append((img[i-1][j] + img[i-1][j+1] + img[i][j+1])*5 - (img[i-1][j-1] + img[i][j-1] + img[i+1][j-1] + img[i+1][j] + img[i+1][j+1])*3)
		k.append((img[i-1][j-1] + img[i-1][j] + img[i-1][j+1])*5 - (img[i][j-1] + img[i][j+1] + img[i+1][j-1] + img[i+1][j] + img[i+1][j+1])*3)
		k.append((img[i-1][j-1] + img[i-1][j] + img[i][j-1])*5 - (img[i-1][j+1] + img[i][j+1] + img[i+1][j-1] + img[i+1][j] + img[i+1][j+1])*3)
		k.append((img[i-1][j-1] + img[i][j-1] + img[i+1][j-1])*5 - (img[i-1][j] + img[i-1][j+1] + img[i][j+1] + img[i+1][j] + img[i+1][j+1])*3)
		k.append((img[i][j-1] + img[i+1][j-1] + img[i+1][j])*5 - (img[i-1][j-1] + img[i-1][j] + img[i-1][j+1] + img[i][j+1] + img[i+1][j+1])*3)
		k.append((img[i+1][j-1] + img[i+1][j] + img[i+1][j+1])*5 - (img[i-1][j-1] + img[i-1][j] + img[i-1][j+1] + img[i][j-1] + img[i][j+1])*3)
		k.append((img[i][j+1] + img[i+1][j] + img[i+1][j+1])*5 - (img[i-1][j-1] + img[i-1][j] + img[i-1][j+1] + img[i][j-1] + img[i+1][j-1])*3)
		if max(k) >= 135:
			img_Kirsch[i-1][j-1] = 0
		else:
			img_Kirsch[i-1][j-1] = 255
cv2.imwrite('img_Kirsch.png', img_Kirsch)

# Robinson's Compass Operator: 43
img_Robinson = np.zeros((row, col), int)
for i in range(1, row+1):
	for j in range(1, col+1):
		r = []
		r.append(abs(img[i-1][j+1] + 2*img[i][j+1] + img[i+1][j+1] - img[i-1][j-1] - 2*img[i][j-1]  - img[i+1][j-1]))
		r.append(abs(img[i-1][j] + 2*img[i-1][j+1] + img[i][j+1] - img[i][j-1] - 2*img[i+1][j-1]  - img[i+1][j]))
		r.append(abs(img[i-1][j-1] + 2*img[i-1][j] + img[i-1][j+1] - img[i+1][j-1] - 2*img[i+1][j]  - img[i+1][j+1]))
		r.append(abs(img[i][j-1] + 2*img[i-1][j-1] + img[i-1][j] - img[i][j+1] - 2*img[i+1][j+1]  - img[i+1][j]))
		if max(r) >= 43:
			img_Robinson[i-1][j-1] = 0
		else:
			img_Robinson[i-1][j-1] = 255
cv2.imwrite('img_Robinson.png', img_Robinson)

# Nevatia-Babu 5x5 Operator: 12500
img_NB = np.zeros((row, col), int)
img55 = padding(img, img.shape[0], img.shape[1])
n1 = np.array([[100, 100, 100, 100, 100], [100, 100, 100, 100, 100], [0, 0, 0, 0, 0], [-100, -100, -100, -100, -100], [-100, -100, -100, -100, -100]])
n2 = np.array([[100, 100, 100, 100, 100], [100, 100, 100, 78, -32], [100, 92, 0, -92, -100], [32, -78, -100, -100, -100], [-100, -100, -100, -100, -100]])
n3 = np.array([[100, 100, 100, 32, -100], [100, 100, 92, -78, -100], [100, 100, 0, -100, -100], [100, 78, -92, -100, -100], [100, -32, -100, -100, -100]])
n4 = np.array([[-100, -100, 0, 100, 100], [-100, -100, 0, 100, 100], [-100, -100, 0, 100, 100], [-100, -100, 0, 100, 100], [-100, -100, 0, 100, 100]])
n5 = np.array([[-100, 32, 100, 100, 100], [-100, -78, 92, 100, 100], [-100, -100, 0, 100, 100], [-100, -100, -92, 78, 100], [-100, -100, -100, -32, 100]])
n6 = np.array([[100, 100, 100, 100, 100], [-32, 78, 100, 100, 100], [-100, -92, 0, 92, 100], [-100, -100, -100, -78, 32], [-100, -100, -100, -100, -100]])
for i in range(2, row+2):
	for j in range(2, col+2):
		n = []
		n.append(np.sum(n1 * img55[i-2: i+3, j-2: j+3]))
		n.append(np.sum(n2 * img55[i-2: i+3, j-2: j+3]))
		n.append(np.sum(n3 * img55[i-2: i+3, j-2: j+3]))
		n.append(np.sum(n4 * img55[i-2: i+3, j-2: j+3]))
		n.append(np.sum(n5 * img55[i-2: i+3, j-2: j+3]))
		n.append(np.sum(n6 * img55[i-2: i+3, j-2: j+3]))
		if max(n) >= 12500:
			img_NB[i-2][j-2] = 0
		else:
			img_NB[i-2][j-2] = 255
cv2.imwrite('img_NB.png', img_NB)
