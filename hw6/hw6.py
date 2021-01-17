import cv2
import numpy as np

def h(b, c, d, e):
	if b != c:
		return 's'
	if d == b and e == b:
		return 'r'
	return 'q'

image = cv2.imread('lena.bmp', 0)
data = open('data.txt','w+') 
image_rows = image.shape[0]
image_cols = image.shape[1]

binary = np.zeros(image.shape, int)
for i in range(image_rows):
	for j in range(image_cols):
		if image[i][j] < 128:
			binary[i][j] = 0
		else:
			binary[i][j] = 255

down_rows = image_rows // 8
down_cols = image_cols // 8
down = np.zeros((down_rows, down_cols), int)
yokoi = np.zeros(down.shape, int)

for i in range(down_rows):
	for j in range(down_cols):
		down[i][j] = binary[i * 8][j * 8]

for i in range(down_rows):
	for j in range(down_cols):
		x0, x1, x2, x3, x4, x5, x6, x7, x8 = [0] * 9
		if down[i][j] != 0:
			x0 = down[i][j]
			if i - 1 >= 0:
				x2 = down[i - 1][j]
				if j - 1 >= 0:
					x7 = down[i - 1][j - 1]
				if j + 1 < down_cols:
					x6 = down[i - 1][j + 1]
			if i + 1 < down_rows:
				x4 = down[i + 1][j]
				if j - 1 >= 0:
					x8 = down[i + 1][j - 1]
				if j + 1 < down_cols:
					x5 = down[i + 1][j + 1]
			if j - 1 >= 0:
				x3 = down[i][j - 1]
			if j + 1 < down_cols:
				x1 = down[i][j + 1]
			count = [h(x0, x1, x6, x2), h(x0, x2, x7, x3), h(x0, x3, x8, x4), h(x0, x4, x5, x1)]
			temp = count.count('q')
			yokoi[i][j] = temp
			if count.count('r') == 4:
				yokoi[i][j] = 5
		if j == down_cols - 1:
			end = '\n'
		else: end = ' '
		if yokoi[i][j] == 0:
			print (' ', end = end, file = data)
		else: print (yokoi[i][j], end = end, file = data)
data.close()