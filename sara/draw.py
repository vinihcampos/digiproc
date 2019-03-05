def rectangle(img, x1, y1, x2, y2, color):
	img[x1:x2,y1:y2] = color
	return img