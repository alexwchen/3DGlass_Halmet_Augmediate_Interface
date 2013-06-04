# Standard Library
import cv
import cv2
import sys
import numpy as np
from scipy.misc import imresize
from scipy.io import loadmat
from recognition_on_video import *

# Personal Library
from predict import *
from operation import *
from contour import *

def run_recognition_on_video(video_name, para_path, Labels):
    f = video_name

    # Read From Video
    capture = cv.CaptureFromFile(f)
    print capture
    print cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH)
    print cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT)

    # Neuronet Configuration
    resize_row = 20
    resize_width = 20

    weights = loadmat(para_path)
    T1 = weights['Theta1']
    T2 = weights['Theta2']


    # Start Loading Video

    history_prediction = []

    while True:
        frame = cv.QueryFrame(capture)
        process_vector = np.zeros((1, resize_row*resize_width))

        # Processing Video Frames
        if frame:

            color, contour_list = extract_and_draw_countour_above_area_threshold(frame, 20000)

            if contour_list:
                color, history_prediction = gesture_recognition_and_labeling(color, contour_list, T1, T2, Labels, history_prediction, True)

            display_cvMat = numpy_to_cvMat(color)
            cv.ShowImage('Real Time Recognition', display_cvMat)
            cv.WaitKey(1)

        # Keyboard interrupt for Exit
        c=cv.WaitKey(2)
        if c==27: #Break if user enters 'Esc'.
            break
