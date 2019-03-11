import cv2
import numpy as np

def blur(img, size):
    copy = img.astype(int)
    h,w = copy.shape
    
    surrounded = copy.mean() * np.ones((h + 2*(size//2), w + 2*(size//2)), dtype=int)
    surrounded[size//2:h + size//2, size//2:w + size//2] = copy
    
    for row in range(h):
        for col in range(w):
            copy[row,col] = np.sum(surrounded[row : row + size, col: col+size]) // (size*size)
    
    return copy.astype('uint8')

t_rex_stripe = cv2.imread('../images/t_rex_stripes.jpg', 0)
blured = blur(t_rex_stripe, 19)

cv2.imwrite('../images/t_rex_blur.jpg', blured)
cv2.imshow('Blured', blured)
cv2.waitKey(0);
cv2.destroyAllWindows()
