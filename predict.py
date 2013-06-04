from numpy import *
from scipy import *
from datetime import datetime
from scipy.misc import imresize
import cv
from operation import *
import collections
#######################################
# Neural Nets Functions
#######################################

def sigmoid(z):
    g = 1.0 / (1.0 + exp(-z));
    return g

def predict(Theta1, Theta2, X):
    vector_ones = ones(X.shape[0]).reshape(X.shape[0],1)

    # input layer
    a1 = hstack((vector_ones,X))

    # middle layer
    Z1 = dot(a1, Theta1.transpose())
    a2 = sigmoid(Z1)
    a2 = hstack((vector_ones,a2))

    # final layer
    Z2 = dot(a2, Theta2.transpose())
    a3 = sigmoid(Z2)

    #print a3.shape
    #print a3

    agmax = (a3.argmax(axis=1)+1).reshape(X.shape[0],1)
    return agmax, a3


def real_time_gesture_recognition_and_labeling(ir_np, rgb_np, contour_list, T1, T2, Labels, history_prediction, debug):

    ir_ipl = numpy_to_iplimage_color(ir_np)
    rgb_ipl = numpy_to_iplimage_color(rgb_np)

    # Label all contour bounding box
    if debug:
        print '================================'
        print contour_list

    for box in contour_list:

        # Crop & Resize
        cv.SetImageROI(ir_ipl, box) #cv.SetImageROI(image, (x,y,w,h))
        crop_frame = iplimage_to_cvMat_grayscale(ir_ipl)
        resize_image = imresize(crop_frame, (20,20))

        # Predict - Max Probability
        array = np.asarray(resize_image)
        process_vector = array.reshape(1,400)
        para, prob = predict(T1, T2, process_vector)
        classify_label = Labels[para[0]]

        if debug:
            print classify_label
            print history_prediction

        # Smoothing - History Prediction
        # Probablity Rank For NN Output Node
        rank = [(prob[0][i],i+1) for i in range(len(prob[0]))]
        rank.sort()

        # History Probablity Recording
        if len(history_prediction) > 20:
            history_prediction.pop(0)
            history_prediction.append(rank[-1][1])
        else:
            history_prediction.append(rank[-1][1])


        if rank[-1][0] - rank[-2][0] < 0.05:
            # Majority Vote for History
            history_count =collections.Counter(history_prediction)
            # (1, 9) 1-> label, 9-> occurance
            l = history_count.most_common(1)
            classify_label = Labels[l[0][0]]
            if debug:
                print 'TIE BREAK SMOOTHING'
                print Labels[rank[-1][1]], Labels[rank[-2][1]]
                print history_count, l[0]
                print classify_label
        if debug:
            print '\n'

        # Draw Prediction
        cv.SetImageROI(ir_ipl, (0,0,640,480)) #cv.SetImageROI(image, (x,y,w,h))
        cv.SetImageROI(rgb_ipl, (0,0,640,480)) #cv.SetImageROI(image, (x,y,w,h))
        x = box[0]
        y = box[1]
        thickness = 1
        font_height = 0.5
        font_weight = 0.5
        font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, font_height, font_weight, 0, thickness, 8) #Creates a font
        cv.PutText(ir_ipl, classify_label, (x,y+15), font, (0,255,0))
        cv.PutText(rgb_ipl, classify_label, (x,y+15), font, (0,255,0))
    if debug:
        print '================================'

    return ir_ipl, rgb_ipl, history_prediction


"""
    This function is only used by video recording testing function
"""
def gesture_recognition_and_labeling(numpy_frame, contour_list, T1, T2, Labels, history_prediction, debug):

    frame = numpy_to_iplimage_color(numpy_frame)

    # Label all contour bounding box
    if debug:
        print '================================'
        print contour_list
    for box in contour_list:

        # Crop & Resize
        cv.SetImageROI(frame, box) #cv.SetImageROI(image, (x,y,w,h))
        crop_frame = iplimage_to_cvMat_grayscale(frame)
        resize_image = imresize(crop_frame, (20,20))

        # Predict - Max Probability
        array = np.asarray(resize_image)
        process_vector = array.reshape(1,400)
        para, prob = predict(T1, T2, process_vector)
        classify_label = Labels[para[0]]

        if debug:
            print classify_label
            print history_prediction

        # Smoothing - History Prediction
        # Probablity Rank For NN Output Node
        rank = [(prob[0][i],i+1) for i in range(len(prob[0]))]
        rank.sort()

        # History Probablity Recording
        if len(history_prediction) > 20:
            history_prediction.pop(0)
            history_prediction.append(rank[-1][1])
        else:
            history_prediction.append(rank[-1][1])


        if rank[-1][0] - rank[-2][0] < 0.05:
            # Majority Vote for History
            history_count =collections.Counter(history_prediction)
            # (1, 9) 1-> label, 9-> occurance
            l = history_count.most_common(1)
            classify_label = Labels[l[0][0]]
            if debug:
                print 'TIE BREAK SMOOTHING'
                print Labels[rank[-1][1]], Labels[rank[-2][1]]
                print history_count, l[0]
                print classify_label
        if debug:
            print '\n'

        # Draw Prediction
        cv.SetImageROI(frame, (0,0,640,480)) #cv.SetImageROI(image, (x,y,w,h))
        x = box[0]
        y = box[1]
        thickness = 1
        font_height = 0.5
        font_weight = 0.5
        font = cv.InitFont(cv.CV_FONT_HERSHEY_SIMPLEX, font_height, font_weight, 0, thickness, 8) #Creates a font
        cv.PutText(frame, classify_label, (x,y+15), font, (0,255,0))
    if debug:
        print '================================'

    numpy_frame = iplimage_to_numpy_color(frame)
    return numpy_frame, history_prediction
