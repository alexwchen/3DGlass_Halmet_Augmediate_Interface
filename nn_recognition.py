# Standard Library
import cv
import cv2
import sys
import numpy as np
from scipy.misc import imresize
from scipy.io import loadmat
from recognition_on_video import *
from freenect import sync_get_depth as get_depth, sync_get_video as get_video

# Personal Library
from predict import *
from operation import *
from contour import *
from ui import *
from billard import *


Labels = ['',
        '1_Paper_Right',
        '2_Rock_Right_Ang',
        '3_Rock_Right_St',
        '4_Point_Right_Ang',
        '5_Point_Right_St',
        '6_Gun_Up',
        '7_Gun_Down',
        '8_Paper_Left',
        '9_Rock_Left_Ang',
        '10_Rock_Left_St',
        '11_Point_Left_Ang',
        '12_Point_Left_St'
        ]

def run_real_time_recognition(para_path, Labels):

    status_dictionary = {}
    # status, pos, radias, color, text, ,pos, font_color
    # states:
    #   0 -> waiting to be hovered
    #   1 -> hovered waiting to be selected(clicked)
    #   2 -> selected waiting to be unselected(clicked)
    start_time = 0
    status_dictionary['b1'] = [False, (530, 70), 60, (255, 255, 0), 'Record', (490, 70), (0,0,0), [], False]
    status_dictionary['b2'] = [False, (380, 70), 60, (0, 255, 0), 'Select', (350, 70), (0,0,0), [], False]
    status_dictionary['b3'] = [False, (240, 70), 60, (0, 255, 255), 'Billard', (210, 70),(0,0,0), [], False]
    status_dictionary['b4'] = [False, (100, 270), 90, (255, 255, 255), 'Drag Me', (70, 270),(0,0,0), [], False]

    global depth,ir, rgb
    count = 0

    # frame_size = (480,640)
    # Setting web cam config
    capture=cv.CaptureFromCAM(0)
    fourcc = cv.CV_FOURCC('X','V','I','D')
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FPS, 25)
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 640)
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 480)

    # Neuronet Configuration
    resize_row = 20
    resize_width = 20
    weights = loadmat(para_path)
    T1 = weights['Theta1']
    T2 = weights['Theta2']
    history_prediction = [] # smoothing and other purpose
    history_gesture_pos = [] # smoothing and other purpose

    # Recording
    record_st = False
    rgb_writer = cv.CreateVideoWriter("recording.avi", cv.CV_FOURCC('X','V','I','D'), 5, (640, 480), True)

    # Capture frames IR, RGB, Depth
    while True:

        # Web cam feed (300, 400, 3)
        rgb_ipl = cv.QueryFrame(capture)

        # Depth IR feed
        (depth,_), (ir,_) = get_depth(), get_video(format=2)

        ir = (ir>150).astype(float)
        ir = ir*255
        ir_ipl = resize_ir_callibrate_with_rgb(ir)

        new_rgb_ipl = cv.CreateImage(cv.GetSize(rgb_ipl), 8, 3)


        #Billard Mode
        yo = rgb_ipl
        f = iplimage_to_numpy_color(yo)
        green_mono = f[:,:,1]
        #image = cv.fromarray(np.array(green_mono[:,:]))
        #cv.ShowImage('G', image)

        rgb_np, threshold_np, contour_list = billard_extract_and_draw_countour(f, 20, green_mono, 120, 0)
        image = cv.fromarray(np.array(rgb_np))

        #print contour_list
        maxx = (0,0,0,0)
        for pos in contour_list:
            if pos[1] > maxx[1]:
                maxx = pos
        #print maxx

        for item in contour_list:
            if maxx != item:
                cv.Line(image, (maxx[0]+maxx[2]/2, maxx[1]+maxx[3]/2), (item[0]+item[2]/2,item[1]+item[3]/2), (0,255,0), thickness=1, lineType=8, shift=0)
        #cv.ShowImage('G Threshold', image)
        new_rgb_ipl = cvMat_to_iplimage_color(image)
        #cv.ShowImage('G Threshold', new_rgb_ipl)







        # Hand Sengmentation
        rgb_np, ir_np, contour_list, history_gesture_pos = real_time_extract_and_draw_countour(ir_ipl, rgb_ipl, 20000, history_gesture_pos)

        # Gesture Recognition
        if contour_list:
            ir_ipl, rgb_ipl, history_prediction = real_time_gesture_recognition_and_labeling(ir_np, rgb_np, contour_list, T1, T2, Labels, history_prediction, False)

            # Update button status
            status_dictionary, start_time = update_button_status(contour_list, history_prediction, Labels, status_dictionary, history_gesture_pos, False, start_time)

        draw_menu_button(ir_ipl, rgb_ipl, status_dictionary, start_time)


        # resize for full screen display
        """
        rgb_np = iplimage_to_numpy_color(rgb_ipl)
        rgb_np = imresize(rgb_np, (800, 1066))
        image = cv.fromarray(np.array(rgb_np))
        cv.ShowImage('rgb', image)
        """
        if status_dictionary['b3'][0]:
            opacity = 0.4
            cv.AddWeighted(new_rgb_ipl, opacity, rgb_ipl, 1 - opacity, 0, rgb_ipl)

        if status_dictionary['b1'][0]:
            cv.WriteFrame(rgb_writer, rgb_ipl)
        else:
            record_status=False

        cv.ShowImage('rgb', rgb_ipl)
        cv.ShowImage('ir', ir_ipl)

        c=cv.WaitKey(5)
        if c==27: #Break if user enters 'Esc'.
            break

#run_recognition_on_video('./videos/paper_rock_point_test.avi', './params/para_12_gesture_v2.mat', Labels)
#run_recognition_on_video('./videos/gunup_gundown_test.avi', './params/para_12_gesture_v2.mat', Labels)
run_real_time_recognition('./params/para_12_gesture_v3.mat', Labels)
