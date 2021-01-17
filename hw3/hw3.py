import cv2
import matplotlib.pyplot as plt
import numpy as np

image = cv2.imread('lena.bmp', 0)
image_cols = image.shape[1]
image_rows = image.shape[0]

# original image and its histogram
cv2.imwrite('lena.png', image)

histogram = np.zeros(256, int)
index = np.arange(256)
for i in range(image_rows):
	for j in range(image_cols):
		histogram[image[i][j]] += 1

plt.bar(index, histogram)
plt.ylabel("Counts")
plt.xlabel('Gray Level')
plt.title('HISTOGRAM OF LENA.BMP')
plt.show()

# image with intensity divided by 3 and its histogram
div3_his = np.zeros(256, int)
div3_img = np.zeros(image.shape, int)
for i in range(image_rows):
	for j in range(image_cols):
		new_value = int(image[i][j] / 3)
		div3_img[i][j] = new_value
		div3_his[new_value] += 1

cv2.imwrite('lena_divided_by_3.png', div3_img)
plt.bar(index, div3_his)
plt.ylabel("Counts")
plt.xlabel('Gray Level')
plt.title('HISTOGRAM OF LENA.BMP DIVIDED BY 3')
plt.show()

# image after applying histogram equalization to (b) and its histogram
eq_img = np.zeros(image.shape, int)
new_grayvalue = np.zeros(256, int)
MN = image_cols * image_rows
for i in range(256):
	acc = 0
	for j in range(i + 1):
		acc += div3_his[j]
	new_grayvalue[i] = 255 * acc / MN
for i in range(image_rows):
	for j in range(image_cols):
		eq_img[i][j] = new_grayvalue[div3_img[i][j]]

eq_his = np.zeros(256, int)
for i in range(image_rows):
	for j in range(image_cols):
		eq_his[eq_img[i][j]] += 1

cv2.imwrite('lena_equalized.png', eq_img)
plt.bar(index, eq_his)
plt.ylabel("Counts")
plt.xlabel('Gray Level')
plt.title('HISTOGRAM OF EQUALIZED LENA.BMP')
plt.show()