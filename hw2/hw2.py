import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread('lena.bmp', 0)
image_cols = image.shape[0]
image_rows = image.shape[1]

# binarize lena.bmp at 128 to get a binary image
binarize = np.zeros(image.shape, int)
for i in range(image_rows):
	for j in range(image_cols):
		if image[i][j] < 128:
			binarize[i][j] = 0
		else:
			binarize[i][j] = 255
cv2.imwrite('binarize.jpg', binarize)

# draw a histogram
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

# connected components
image3 = cv2.imread('binarize.jpg', 0)

image3_rows = image3.shape[0]
image3_cols = image3.shape[1]

in_run = 0			# 是否在 run 裡面
counts_inRow = []	# 一列有多少個 run [row 開始時在第幾個 run, row 結束時在第幾個 run]
run_data = []		# index -> 第幾個 run, [第幾個 row, startCOL, endCOL, permLabel, 該 run 有幾個 pixel]
for i in range(image3_rows):
	row_counts = 0
	startCOL = 0
	endCOL = 0
	for j in range(image3_cols):

		if image3[i][j] > 128:	# pixel 0 黑色, pixel != 0 白色 
			if in_run == 0:
				in_run = 1
				startCOL = j
				row_counts += 1
			if j == image3_cols - 1:
				in_run = 0
				endCOL = j
				run_data.append([i, startCOL, endCOL, 0, endCOL - startCOL + 1])
		else:
			if in_run != 0:
				in_run = 0
				endCOL = j - 1
				run_data.append([i, startCOL, endCOL, 0, endCOL - startCOL + 1])
		
	if row_counts == 0:
		counts_inRow.append([0, 0])
	else:
		length = len(run_data)
		counts_inRow.append([length - row_counts + 1, length])

# Run_Lenght_Implementation
label = [['nothing']]	# 有哪些 run 是用哪些 label
# Top-down pass
for L in range(image3_rows):
	Start_inL = counts_inRow[L][0]
	End_inL = counts_inRow[L][1]
	if L == 0:
		preStart_inL = 0
		preEnd_inL = 0
	else:
		preStart_inL = counts_inRow[L - 1][0]
		preEnd_inL = counts_inRow[L - 1][1]
	while (Start_inL <= End_inL and preStart_inL <= preEnd_inL and preStart_inL != 0):

		if run_data[Start_inL - 1][2] < run_data[preStart_inL - 1][1]:
			Start_inL += 1
		elif run_data[preStart_inL - 1][2] < run_data[Start_inL - 1][1]:
			preStart_inL += 1
		else:
			PLabel = run_data[Start_inL - 1][3]
			preLabel = run_data[preStart_inL - 1][3]
			if PLabel == 0:
				run_data[Start_inL - 1][3] = preLabel
				label[preLabel].append(Start_inL - 1)
			elif PLabel != 0 and preLabel != PLabel:

				if PLabel < preLabel:
					run_data[preStart_inL - 1][3] = PLabel
					label[preLabel].remove(preStart_inL - 1)
					label[PLabel].append(preStart_inL - 1)
				else:
					run_data[Start_inL - 1][3] = preLabel
					label[PLabel].remove(Start_inL - 1)
					label[preLabel].append(Start_inL - 1)
			if run_data[Start_inL - 1][2] > run_data[preStart_inL - 1][2]:
				preStart_inL += 1
			elif run_data[preStart_inL - 1][2] > run_data[Start_inL - 1][2]:
				Start_inL += 1
			elif run_data[preStart_inL - 1][2] == run_data[Start_inL - 1][2]:
				preStart_inL += 1
				Start_inL += 1
	Start_inL = counts_inRow[L][0]
	while (Start_inL <= End_inL):
		PLabel = run_data[Start_inL - 1][3]
		LenOfLabel = len(label)
		if PLabel == 0:
			run_data[Start_inL - 1][3] = LenOfLabel
			label.append([Start_inL - 1])
		Start_inL += 1

# Bottom-up pass
for L in range(image3_rows - 1, -1, -1):
	Start_inL = counts_inRow[L][0]
	End_inL = counts_inRow[L][1]
	if L == image3_rows - 1:
		preStart_inL = 0
		preEnd_inL = 0
	else:
		preStart_inL = counts_inRow[L + 1][0]
		preEnd_inL = counts_inRow[L + 1][1]
	while (Start_inL <= End_inL and preStart_inL <= preEnd_inL and preStart_inL != 0):
		if run_data[Start_inL - 1][2] < run_data[preStart_inL - 1][1]:
			Start_inL += 1
		elif run_data[preStart_inL - 1][2] < run_data[Start_inL - 1][1]:
			preStart_inL += 1
		else:
			PLabel = run_data[Start_inL - 1][3]
			preLabel = run_data[preStart_inL - 1][3]
			if PLabel != preLabel:
				if PLabel < preLabel:
					Len_of_Label = len(label[preLabel])
					for i in range(Len_of_Label):
						run_num = label[preLabel][i]
						run_data[run_num][3] = PLabel
					label[PLabel] += label[preLabel]
					for i in range(Len_of_Label):
						label[preLabel].pop()
				else:
					Len_of_Label = len(label[PLabel])
					for i in range(Len_of_Label):
						run_num = label[PLabel][i]
						run_data[run_num][3] = preLabel
					label[preLabel] += label[PLabel]
					for i in range(Len_of_Label):
						label[PLabel].pop()
			if run_data[Start_inL - 1][2] > run_data[preStart_inL - 1][2]:
				preStart_inL += 1
			elif run_data[preStart_inL - 1][2] > run_data[Start_inL - 1][2]:
				Start_inL += 1
			elif run_data[preStart_inL - 1][2] == run_data[Start_inL - 1][2]:
				preStart_inL += 1
				Start_inL += 1
	Start_inL = counts_inRow[L][0]

Len = len(label)
len_pixel = [0]
right_pos = [0]
left_pos = [0]
for i in range(1, Len):
	pixel = 0
	if len(label[i]) == 0:
		right_pos.append([])
		left_pos.append([])
	for j in range(len(label[i])):
		pixel += run_data[label[i][j]][4]
		if j == 0:
			right_pos.append(run_data[label[i][j]][2])
			left_pos.append(run_data[label[i][j]][1])
		else:
			if right_pos[i] < run_data[label[i][j]][2]:
				right_pos[i] = run_data[label[i][j]][2]
			if left_pos[i] > run_data[label[i][j]][1]:
				left_pos[i] = run_data[label[i][j]][1]

	len_pixel.append(pixel)
count = 0
final_image = cv2.imread('binarize.jpg')
for i in range(Len):
	label[i].sort()
	Length = len(label[i])
	x_cen = 0
	y_cen = 0
	if (len_pixel[i] >= 500):
		count += 1
		x = left_pos[i]
		x_end = right_pos[i]
		y = run_data[label[i][0]][0]
		y_end = run_data[label[i][Length - 1]][0]
		cv2.rectangle(final_image, (x, y), (x_end, y_end), (255, 255, 0), 1)
		for j in range(Length):
			run_order = label[i][j]
			x_cen_plus = ((run_data[run_order][1] + run_data[run_order][2])/ 2) * run_data[run_order][4] 
			y_cen_plus = run_data[run_order][0] * run_data[run_order][4]
			x_cen += x_cen_plus
			y_cen += y_cen_plus
		x_cen /= len_pixel[i]
		y_cen /= len_pixel[i]
		x_cen = int(x_cen)
		y_cen = int(y_cen)
		cv2.line(final_image, (x_cen - 6, y_cen), (x_cen + 6, y_cen), (0, 0, 255), thickness=2)
		cv2.line(final_image, (x_cen, y_cen - 6), (x_cen, y_cen + 6), (0, 0, 255), thickness=2)

cv2.imwrite('connected.jpg', final_image)

