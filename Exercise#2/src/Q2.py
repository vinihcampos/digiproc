import cv2
import numpy as np

def local_conv(img, kernel, cx, cy, norm=False, maxv=None, minv=None):
    kh,kw = kernel.shape
    size = kh // 2
    
    h,w = img.shape
    
    result = 0
    
    kernel_x = 0
    kernel_y = 0
    
    for i in range(cx - size, cx + size + 1):
        for j in range(cy - size, cy + size + 1):
            if i >= 0 and j >= 0 and i < h and j < w:
                result += abs(img[i,j] * kernel[kernel_x, kernel_y])
            kernel_y += 1
        kernel_y = 0
        kernel_x += 1
    
    if norm:
        result = int(255 * (result + maxv) / (maxv - minv))
        
    return result

def sobelx(img):
    kernel = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
    copy = img.copy()
    h,w = img.shape
    
    for i in range(h):
        for j in range(w):
            copy[i,j] = local_conv(img, kernel, i, j, True, 1020, -1020)
    return copy

def sobely(img):
    kernel = np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
    copy = img.copy()
    h,w = img.shape
    
    for i in range(h):
        for j in range(w):
            copy[i,j] = local_conv(img, kernel, i, j, True, 1020, -1020)
    return copy

def bitwise_or(img1, img2, norm=False):
    result = img1.astype(int) + img2.astype(int)    
    minv = img1.astype(int).min() + img2.astype(int).min()
    maxv = img1.astype(int).max() + img2.astype(int).max()
    
    if norm:
        result = (int)(255 * ((result + maxv) / (maxv - minv)))
    
    return result

def mask_generation(img, limit, margin):
    h,w = img.shape
    mask = np.zeros((h,w), dtype='uint')
    
    for row in range(h):
        for col in range(w):
            if img[row,col] <= limit:
                min_row = max(0,   row-margin)
                max_row = min(h-1, row+margin)
                min_col = max(0,   col-margin)
                max_col = min(w-1, col+margin)
                mask[min_row:max_row,min_col:max_col] = 255
    
    return mask.astype('uint8')

def selective_smooth(img, binary, blur_min, blur_max):
    kernel_min = (1 / (blur_min * blur_min)) * np.ones((blur_min,blur_min), dtype=float)
    kernel_max = (1 / (blur_max * blur_max)) * np.ones((blur_max,blur_max), dtype=float)
    
    copy = img.copy()
    h,w = copy.shape[0:2]
    
    for i in range(h):
        for j in range(w):
            if binary[i,j] == 255:
                copy[i,j] = local_conv(img, kernel_min, i, j)
            else:
                copy[i,j] = local_conv(img, kernel_max, i, j)
    return copy.astype('uint8')

velociraptor = cv2.imread('../images/velociraptor.jpg', 0)

velociraptor_sobelx = sobelx(velociraptor)
velociraptor_sobely = sobely(velociraptor)
velociraptor_sobelxy = bitwise_or(velociraptor_sobelx, velociraptor_sobely)
mask = mask_generation(velociraptor_sobelxy, 150, 10)
velociraptor_blured = selective_smooth(velociraptor, mask, 1, 3)
cv2.imwrite('../images/velociraptor_blured.jpg', velociraptor_blured)

cv2.imshow('Original', velociraptor)
cv2.imshow('Mask', mask)
cv2.imshow('Result', velociraptor_blured)
cv2.waitKey(0);
cv2.destroyAllWindows()
