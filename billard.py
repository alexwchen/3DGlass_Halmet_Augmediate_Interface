from scipy.misc import imresize
from operation import *
import numpy as np
import cv
import cv2

"""
    This functin is only used by the video recording function
"""
def billard_extract_and_draw_countour(color_np, max_area, mono_np, thr, thr_mode):

    # Numpy Arrays
    color = color_np
    gray = mono_np

    # Calculate Contour Using Binary Grayscale
    """
    0: Binary
    1: Binary Inverted
    2: Threshold Truncated
    3: Threshold to Zero
    4: Threshold to Zero Inverted
    """
    ret,thresh = cv2.threshold(gray,thr,255,thr_mode)

    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(color,contours,-1,(0,255,0),3)
    contour_list = []
    # Loop through all possible contour find max
    for i in contours:
        x,y,w,h = cv2.boundingRect(i)
        if w*h < 4000 and w*h>200:
            cv2.rectangle(color,(x,y),(x+w, y+h),(0,255,255),2)
            contour_list.append((x,y,w,h))

    return color, thresh, contour_list
