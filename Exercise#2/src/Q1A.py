import cv2

# Increase the pixel intensity by a value v
def addWeight(img, v):
    copy = img.astype(int)
    copy += v
    copy[ copy > 255 ] = 255
    return copy.astype('uint8')

# Draw vertical rectangle
def vertical_rectangle(img, p, width, color):
    img[:,p:p+width] = color

# Draw several vertical rectangles
def vertical_strips(img, width, spacing, color):
    copy = img.copy()
    h,w = copy.shape
    sw = 0
    while(sw < w):
        vertical_rectangle(copy, sw, width, color)
        sw += width + spacing
    return copy

# Apply weight and draw vertical rectangles
def efect(img, weight, width, spacing, color):
    weighted = addWeight(img, weight)
    return vertical_strips(weighted, width, spacing, color)

t_rex = cv2.imread('../images/t_rex.jpg', 0)
t_rex_stripes = efect(t_rex, 150, 15, 5, 0)
cv2.imwrite('../images/t_rex_stripes.jpg', t_rex_stripes)

cv2.imshow('Original', t_rex)
cv2.imshow('Stripes', t_rex_stripes)
cv2.waitKey(0);
cv2.destroyAllWindows()

