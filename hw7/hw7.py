import cv2
import numpy as np

def yokoi_func(listOfx, i, j, rowEdge, colEdge, down_image):
	listOfx[0] = down_image[i][j]
	if i - 1 >= 0:
		listOfx[2] = down_image[i - 1][j]
		if j - 1 >= 0:
			listOfx[7] = down_image[i - 1][j - 1]
		if j + 1 < colEdge:
			listOfx[6] = down_image[i - 1][j + 1]
	if i + 1 < rowEdge:
		listOfx[4] = down_image[i + 1][j]
		if j - 1 >= 0:
			listOfx[8] = down_image[i + 1][j - 1]
		if j + 1 < colEdge:
			listOfx[5] = down_image[i + 1][j + 1]
	if j - 1 >= 0:
		listOfx[3] = down_image[i][j - 1]
	if j + 1 < colEdge:
		listOfx[1] = down_image[i][j + 1]
	count = [h(listOfx[0], listOfx[1], listOfx[6], listOfx[2]), \
			h(listOfx[0], listOfx[2], listOfx[7], listOfx[3]), \
			h(listOfx[0], listOfx[3], listOfx[8], listOfx[4]), \
			h(listOfx[0], listOfx[4], listOfx[5], listOfx[1])]
	ans = count.count('q')
	if count.count('r') == 4:
		ans = 5
	return ans

def h(b, c, d, e):
	if b != c:
		return 's'
	if d == b and e == b:
		return 'r'
	return 'q'
	
image = cv2.imread('lena.bmp', 0)
image_rows = image.shape[0]
image_cols = image.shape[1]

binary = np.zeros(image.shape, int)
for i in range(image_rows):
	for j in range(image_cols):
		if image[i][j] < 128:
			binary[i][j] = 0
		else:
			binary[i][j] = 255
# cv2.imwrite('binary.bmp', binary)

down_rows = image_rows // 8
down_cols = image_cols // 8
down = np.zeros((down_rows, down_cols), int)
yokoi = np.zeros(down.shape, int)
pair = np.zeros((down_rows, down_cols), str)

for i in range(down_rows):
	for j in range(down_cols):
		down[i][j] = binary[i * 8][j * 8]

cv2.imwrite('thresholding and downsampling image.bmp', down)

while 1:
	for i in range(down_rows):
		for j in range(down_cols):
			if down[i][j] != 0:
				yokoi[i][j] = yokoi_func([0]*9, i, j, down_rows, down_cols, down)
				
	for i in range(down_rows):
		for j in range(down_cols):
			if yokoi[i][j] == 1:
				add = 0
				if i != 0:
					add += (yokoi[i-1][j] == 1)
				if i != down_rows - 1:
					add += (yokoi[i+1][j] == 1)
				if j != 0:
					add += (yokoi[i][j-1] == 1)
				if j != down_cols - 1:
					add += (yokoi[i][j+1] == 1)
				if add > 0:
					pair[i][j] = 'p'
				else:
					pair[i][j] = 'q'
			elif yokoi[i][j] > 1:
				pair[i][j] = 'q'

	newDown = down.copy()
	for i in range(down_rows):
		for j in range(down_cols):
			if pair[i][j] == 'p':
				if yokoi_func([0]*9, i, j, down_rows, down_cols, newDown) == 1:
					newDown[i][j] = 0

	if (down == newDown).all():
		break
	down = newDown

cv2.imwrite('newDown.bmp', newDown)
