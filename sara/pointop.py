# This function apply limiarization to image, 
# applying min_color to all values lower than limit and max_color to the remaining
def threshold(img, limit, min_color, max_color):
    copy = img.copy()
    range_max = img > limit
    range_min = img <= limit

    copy[range_max] = max_color;
    copy[range_min] = min_color;
    return copy

# Negate the pixels of image [0-255]
def negate(img):
    return 255 - img

# Increase the pixel intensity by a value v
def addWeight(img, v, sx = None, ex = None, sy = None, ey = None):
    h,w = img.shape
    
    if sx == None:
        sx = 0
    if ex == None:
        ex = h
    if sy == None:
        sy = 0
    if ey == None:
        ey = w

    copy = img.copy()
    copy[sx:ex,sy:ey] += int(v)

    copy = (copy - v) / (510 - v)
    print(copy)
    return copy