import sys
import cv2
import numpy as np

def nothing(x):
	pass

color_space = 'COLOR SPACE - HSV'
cv2.namedWindow(color_space)

maxh = 'Max(H)'
minh = 'Min(H)'

maxs = 'Max(S)'
mins = 'Min(S)'

maxv = 'Max(V)'
minv = 'Min(V)'

cv2.createTrackbar(minh, color_space,0,179,nothing)
cv2.createTrackbar(maxh, color_space,0,179,nothing)
cv2.createTrackbar(mins, color_space,0,255,nothing)
cv2.createTrackbar(maxs, color_space,0,255,nothing)
cv2.createTrackbar(minv, color_space,0,255,nothing)
cv2.createTrackbar(maxv, color_space,0,255,nothing)


path = ""
if len(sys.argv) > 1:
	path = sys.argv[1]

# Read image from path
image = cv2.imread(path)

# Change color space
image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Shape of image
h,w,_ = image.shape
fixed_size = 300

# Resize image to adjust the screen
if h > fixed_size:
	rfactor = fixed_size / h;
	image = cv2.resize(image, (round(w*rfactor), round(h*rfactor)))
elif w > fixed_size:
	rfactor = fixed_size / w;
	image = cv2.resize(image, (round(w*rfactor), round(h*rfactor)))

cv2.imshow('Original', cv2.cvtColor(image, cv2.COLOR_HSV2BGR))
while(True):

	pos_minh = cv2.getTrackbarPos(minh, color_space)
	pos_maxh = cv2.getTrackbarPos(maxh, color_space)
	pos_mins = cv2.getTrackbarPos(mins, color_space)
	pos_maxs = cv2.getTrackbarPos(maxs, color_space)
	pos_minv = cv2.getTrackbarPos(minv, color_space)
	pos_maxv = cv2.getTrackbarPos(maxv, color_space)

	result = cv2.inRange(image, (pos_minh, pos_mins, pos_minv), (pos_maxh, pos_maxs, pos_maxv))
	result = cv2.bitwise_and(image, image, mask=result)
	cv2.imshow(color_space, result)
	k = cv2.waitKey(1) & 0xFF
	if k == ord('m'):
		mode = not mode
	elif k == 27:
		break

cv2.destroyAllWindows()
