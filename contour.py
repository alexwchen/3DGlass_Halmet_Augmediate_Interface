from scipy.misc import imresize
from operation import *
import numpy as np
import cv
import cv2

"""
    This functin is only used by the video recording function
"""
def extract_and_draw_countour_above_area_threshold(frame, max_area):

    # Numpy Arrays
    color = iplimage_to_numpy_color(frame)
    gray = iplimage_to_numpy_grayscale(frame)[:,:-10]

    # Calculate Contour Using Binary Grayscale
    ret,thresh = cv2.threshold(gray,127,255,0)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(color,contours,-1,(0,255,0),3)

    contour_list = []
    # Loop through all possible contour find max
    for i in contours:
        x,y,w,h = cv2.boundingRect(i)

        if w*h>max_area:
            # Draw bounding box
            cv2.rectangle(color,(x,y),(x+w, y+h),(0,255,255),2)
            contour_list.append((x,y,w,h))

    return color, contour_list

def resize_ir_callibrate_with_rgb(ir_np):

    ir_cvMat = cv.fromarray(ir_np)
    ir_ipl = cvMat_to_iplimage_color(ir_cvMat)

    # Resize and Crop x,y,w,h
    cv.SetImageROI(ir_ipl, (95,0,500,380))
    ir_np = iplimage_to_numpy_color(ir_ipl)
    ir_np = imresize(ir_np, (480, 640))
    ir_cvMat = cv.fromarray(ir_np)
    ir_ipl = cvMat_to_iplimage_color(ir_cvMat)

    return ir_ipl

def real_time_extract_and_draw_countour(ir_ipl, rgb_ipl, max_area, history_gesture_pos):

    # Numpy Arrays
    rgb_np = iplimage_to_numpy_color(rgb_ipl)
    ir_np = iplimage_to_numpy_color(ir_ipl)
    gray = iplimage_to_numpy_grayscale(ir_ipl)[:,:-10]

    # Calculate Contour Using Binary Grayscale
    ret,thresh = cv2.threshold(gray,127,255,0)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(color,contours,-1,(0,255,0),3)

    contour_list = []
    # Loop through all possible contour find max
    for i in contours:
        x,y,w,h = cv2.boundingRect(i)

        if w*h>max_area:
            # Draw bounding box
            cv2.rectangle(rgb_np,(x,y),(x+w, y+h),(0,255,255),2)
            cv2.rectangle(ir_np,(x,y),(x+w, y+h),(0,255,255),2)
            contour_list.append((x,y,w,h))
    if contour_list:
        if len(history_gesture_pos) >= 10:
            del history_gesture_pos[0]
            history_gesture_pos.append(contour_list[0])
        else:
            history_gesture_pos.append(contour_list[0])


    return rgb_np, ir_np, contour_list, history_gesture_pos
