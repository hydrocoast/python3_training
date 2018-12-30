import cv2
import numpy as np

def img_reduction(img):
    """ 
    Resize an image
    """
    h, w = img.shape[:2]
    #print h, w
    while h >= 1024 or w>= 1024:
        img = cv2.resize(img, (int(w/2), int(h/2)), interpolation = cv2.INTER_LINEAR)
        h, w = img.shape[:2]
    return img

def cv2show(image, windowname="Figure"):
    cv2.imshow(windowname, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def mask_white(image, threshold1, threshold2):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    threshold1 = np.array(threshold1, np.uint8)
    threshold2 = np.array(threshold2, np.uint8)
    c_region = cv2.inRange(hsv, threshold1, threshold2)
    
    white = np.full(image.shape, 255, dtype=image.dtype)
    background = cv2.bitwise_and(white, white, mask=c_region)
    
    inv_masked = cv2.bitwise_not(c_region)
    extracted = cv2.bitwise_and(image, image, mask=inv_masked)

    masked = cv2.add(extracted, background)
    return masked

def binary_threshold(imggray, thresh_bg, thresh_main, maxval=255):
    th, back = cv2.threshold(imggray, thresh_bg, maxval, cv2.THRESH_BINARY)
    th, clr = cv2.threshold(imggray, thresh_main, maxval, cv2.THRESH_BINARY_INV)
    merged = np.minimum(back, clr)
    return merged

def padding_position(x, y, w, h, p):
    return x - p, y - p, w + p * 2, h + p * 2

def main():
    ## read an image
    imgorg = cv2.imread('data/hydrangea.jpg')
    imgorg = img_reduction(imgorg)
    
    ## masking
    masked = mask_white(cv2.GaussianBlur(imgorg, (9, 9), 0), [25, 0, 0], [95, 255, 255])
    cv2show(masked)

    ## egde detection
    grayblurred = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
    extracted_gray = binary_threshold(grayblurred, 160, 255)
    cv2show(extracted_gray)
    extracted_gray = cv2.bitwise_not(extracted_gray)
    # version 3
    im, contours, hierarchy = cv2.findContours(extracted_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    ## draw contour
    imgwcnt = np.copy(imgorg)
    for c in contours:
        if cv2.contourArea(c) < 800:
             continue
        
        # rectangle area
        x, y, w, h = cv2.boundingRect(c)
        x, y, w, h = padding_position(x, y, w, h, 5)
        # circle
        (xr,yr), radius = cv2.minEnclosingCircle(c)
        center = (int(xr), int(yr))
        radius = int(radius)
    
        # draw contour
        cv2.drawContours(imgwcnt, c, -1, (0, 0, 255), 3)  # contour
        cv2.rectangle(imgwcnt, (x, y), (x + w, y + h), (255, 0, 0), 3)  #rectangle
        cv2.circle(imgwcnt, center, radius, (0, 255, 0), 3)  #circle

    cv2show(imgwcnt)
    #cv2.imwrite('hydrangea_contour.jpg', imgwcnt)
    
if __name__ == '__main__':
    main()
