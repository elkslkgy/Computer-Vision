import cv2
import random
import math
import numpy as np

def gaussian_noise(img, amplitude):
	return img + amplitude * np.random.normal(loc=0, scale=1, size=img.shape)

def salt_and_pepper_noise(img, probability):
	s_a_p_img = img.copy()
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			if random.random() < probability:
				s_a_p_img[i][j] = 0
			elif random.random() > 1 - probability:
				s_a_p_img[i][j] = 255
	return s_a_p_img

def box_filter(img, size):
	box_img = np.zeros(img.shape, int)
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			half = size // 2
			count = 0
			for x in range(0 - half, half + 1):
				for y in range(0 - half, half + 1):
					if (j + y < 0) or (j + y >= img.shape[1]):
						continue
					if (i + x < 0) or (i + x >= img.shape[0]):
						continue
					count += 1
					box_img[i][j] += img[i + x][j + y]
			box_img[i][j] = box_img[i][j] // count
	return box_img

def median_filter(img, size):
	median_img = np.zeros(img.shape, int)
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			half = size // 2
			temp = []
			for x in range(0 - half, half + 1):
				for y in range(0 - half, half + 1):
					if (j + y < 0) or (j + y >= img.shape[1]):
						continue
					if (i + x < 0) or (i + x >= img.shape[0]):
						continue
					temp.append(img[i + x][j + y])
			median_img[i][j] = np.median(temp)
	return median_img

def opening(img, kernel):
	return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

def closing(img, kernel):
	return cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

def mean_var(img, n):
	total = 0
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			total += img[i][j]
	mean = total / n
	v_total = 0
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			v_total += (img[i][j] - mean)**2
	variance = v_total / n
	return mean, variance

def SNR(Img_s, Img_n):
	row = Img_s.shape[0]
	col = Img_s.shape[1]
	n = row * col
	total_s = 0
	total_n = 0
	new = np.zeros(Img_s.shape)
	for i in range(row):
		for j in range(col):
			total_s += Img_s[i][j]
			total_n += Img_n[i][j] + 255 - Img_s[i][j]
	ms = total_s / n
	mn = total_n / n
	v_total_s = 0
	v_total_n = 0
	for i in range(row):
		for j in range(col):
			v_total_s += (Img_s[i][j] - ms)**2 / n
			v_total_n += (Img_n[i][j] + 255 - Img_s[i][j] - mn)**2 / n
	vs = v_total_s
	vn = v_total_n
	snr = 20 * math.log10((vs**0.5) / (vn**0.5))
	return snr

octagonal = np.ones((5,5),np.uint8)
octagonal[0][0] = 0
octagonal[0][4] = 0
octagonal[4][0] = 0
octagonal[4][4] = 0

image = cv2.imread('lena.bmp', 0)

# (a) Generate noisy images with gaussian noise(amplitude of 10 and 30)
gaussian_noise_10 = gaussian_noise(image, 10)
print ('gau_10 SNR:', SNR(image, gaussian_noise_10))
cv2.imwrite('gaussian_noise_10.png', gaussian_noise_10)

gaussian_noise_30 = gaussian_noise(image, 30)
print ('gau_30 SNR:', SNR(image, gaussian_noise_30))
cv2.imwrite('gaussian_noise_30.png', gaussian_noise_30)

# (b) Generate noisy images with salt-and-pepper noise(probability 0.1 and 0.05)
s_a_p_01 = salt_and_pepper_noise(image, 0.1)
print ('sap_01 SNR:', SNR(image, s_a_p_01))
cv2.imwrite('s_a_p_01.png', s_a_p_01)

s_a_p_005 = salt_and_pepper_noise(image, 0.05)
print ('sap_005 SNR:', SNR(image, s_a_p_005))
cv2.imwrite('s_a_p_005.png', s_a_p_005)

# (c) Use the 3x3, 5x5 box filter on images generated by (a)(b)
gau_10_box_3 = box_filter(gaussian_noise_10, 3)
print ('gau10_box3 SNR:', SNR(image, gau_10_box_3))
cv2.imwrite('gau_10_box_3.png', gau_10_box_3)

gau_30_box_3 = box_filter(gaussian_noise_30, 3)
print ('gau30_box3 SNR:', SNR(image, gau_30_box_3))
cv2.imwrite('gau_30_box_3.png', gau_30_box_3)

sap_01_box_3 = box_filter(s_a_p_01, 3)
print ('sap01_box3 SNR:', SNR(image, sap_01_box_3))
cv2.imwrite('sap_01_box_3.png', sap_01_box_3)

sap_005_box_3 = box_filter(s_a_p_005, 3)
print ('sap005_box3 SNR:', SNR(image, sap_005_box_3))
cv2.imwrite('sap_005_box_3.png', sap_005_box_3)

gau_10_box_5 = box_filter(gaussian_noise_10, 5)
print ('gau10_box5 SNR:', SNR(image, gau_10_box_5))
cv2.imwrite('gau_10_box_5.png', gau_10_box_5)

gau_30_box_5 = box_filter(gaussian_noise_30, 5)
print ('gau30_box5 SNR:', SNR(image, gau_30_box_5))
cv2.imwrite('gau_30_box_5.png', gau_30_box_5)

sap_01_box_5 = box_filter(s_a_p_01, 5)
print ('sap01_box5 SNR:', SNR(image, sap_01_box_5))
cv2.imwrite('sap_01_box_5.png', sap_01_box_5)

sap_005_box_5 = box_filter(s_a_p_005, 5)
print ('sap005_box5 SNR:', SNR(image, sap_005_box_5))
cv2.imwrite('sap_005_box_5.png', sap_005_box_5)

# (d) Use 3x3, 5x5 median filter on images generated by (a)(b)
gau_10_median_3 = median_filter(gaussian_noise_10, 3)
print ('gau10_med3 SNR:', SNR(image, gau_10_median_3))
cv2.imwrite('gau_10_median_3.png', gau_10_median_3)

gau_30_median_3 = median_filter(gaussian_noise_30, 3)
print ('gau30_med3 SNR:', SNR(image, gau_30_median_3))
cv2.imwrite('gau_30_median_3.png', gau_30_median_3)

sap_01_median_3 = median_filter(s_a_p_01, 3)
print ('sap01_med3 SNR:', SNR(image, sap_01_median_3))
cv2.imwrite('sap_01_median_3.png', sap_01_median_3)

sap_005_median_3 = median_filter(s_a_p_005, 3)
print ('sap005_med3 SNR:', SNR(image, sap_005_median_3))
cv2.imwrite('sap_005_median_3.png', sap_005_median_3)

gau_10_median_5 = median_filter(gaussian_noise_10, 5)
print ('gau10_med5 SNR:', SNR(image, gau_10_median_5))
cv2.imwrite('gau_10_median_5.png', gau_10_median_5)

gau_30_median_5 = median_filter(gaussian_noise_30, 5)
print ('gau30_med5 SNR:', SNR(image, gau_30_median_5))
cv2.imwrite('gau_30_median_5.png', gau_30_median_5)

sap_01_median_5 = median_filter(s_a_p_01, 5)
print ('sap01_med5 SNR:', SNR(image, sap_01_median_5))
cv2.imwrite('sap_01_median_5.png', sap_01_median_5)

sap_005_median_5 = median_filter(s_a_p_005, 5)
print ('sap005_med5 SNR:', SNR(image, sap_005_median_5))
cv2.imwrite('sap_005_median_5.png', sap_005_median_5)

# (e) Use both opening-then-closing and closing-then opening filter (using the octogonal 3-5-5-5-3 kernel, value = 0) on images generated by (a)(b)
gau_10_open_close = closing(opening(gaussian_noise_10, octagonal), octagonal)
print ('gau10_oc SNR:', SNR(image, gau_10_open_close))
cv2.imwrite('gau_10_open_close.png', gau_10_open_close)

gau_10_close_open = opening(closing(gaussian_noise_10, octagonal), octagonal)
print ('gau10_co SNR:', SNR(image, gau_10_close_open))
cv2.imwrite('gau_10_close_open.png', gau_10_close_open)

gau_30_open_close = closing(opening(gaussian_noise_30, octagonal), octagonal)
print ('gau30_oc SNR:', SNR(image, gau_30_open_close))
cv2.imwrite('gau_30_open_close.png', gau_30_open_close)

gau_30_close_open = opening(closing(gaussian_noise_30, octagonal), octagonal)
print ('gau30_co SNR:', SNR(image, gau_30_close_open))
cv2.imwrite('gau_30_close_open.png', gau_30_close_open)

sap_01_open_close = closing(opening(s_a_p_01, octagonal), octagonal)
print ('sap01_oc SNR:', SNR(image, sap_01_open_close))
cv2.imwrite('sap_01_open_close.png', sap_01_open_close)

sap_01_close_open = opening(closing(s_a_p_01, octagonal), octagonal)
print ('sap01_co SNR:', SNR(image, sap_01_close_open))
cv2.imwrite('sap_01_close_open.png', sap_01_close_open)

sap_005_open_close = closing(opening(s_a_p_005, octagonal), octagonal)
print ('sap005_oc SNR:', SNR(image, sap_005_open_close))
cv2.imwrite('sap_005_open_close.png', sap_005_open_close)

sap_005_close_open = opening(closing(s_a_p_005, octagonal), octagonal)
print ('sap005_co SNR:', SNR(image, sap_005_close_open))
cv2.imwrite('sap_005_close_open.png', sap_005_close_open)