import cv
import cv2
import os
import numpy as np
########################################
#   Numpy <=> Iplimage
########################################

def numpy_to_iplimage_grayscale(numpy_format):
    cvMat = cv.fromarray(numpy_format)
    cv.SaveImage('cvMat.png', cvMat) #Saves the image
    iplimage = cv.LoadImage('cvMat.png', cv.CV_LOAD_IMAGE_GRAYSCALE)
    os.system('rm cvMat.png')
    return iplimage

def numpy_to_iplimage_color(numpy_format):
    cvMat = cv.fromarray(numpy_format)
    cv.SaveImage('cvMat.png', cvMat) #Saves the image
    iplimage = cv.LoadImage('cvMat.png', cv.CV_LOAD_IMAGE_COLOR)
    fuck = cv.fromarray(numpy_format)
    os.system('rm cvMat.png')
    return iplimage

def iplimage_to_numpy_grayscale(iplimage):
    cv.SaveImage('iplimage.png', iplimage) #Saves the image
    mat = cv.LoadImageM('iplimage.png', cv.CV_LOAD_IMAGE_GRAYSCALE)
    narray = np.asarray(mat)
    os.system('rm iplimage.png')
    return narray

def iplimage_to_numpy_color(iplimage):
    cv.SaveImage('iplimage.png', iplimage) #Saves the image
    mat = cv.LoadImageM('iplimage.png', cv.CV_LOAD_IMAGE_COLOR)
    narray = np.asarray(mat)
    os.system('rm iplimage.png')
    return narray

########################################
#   cvMat <=> Numpy
########################################

def numpy_to_cvMat(numpy_format):
    cvMat = cv.fromarray(numpy_format)
    return cvMat

def cvMat_to_numpy(cvMat):
    narray = np.asarray(cvMat)
    return narray

########################################
#   Iplimage <=> cvMat
########################################

def iplimage_to_cvMat_color(iplimage):
    cv.SaveImage('iplimage.png', iplimage) #Saves the image
    cvMat = cv.LoadImageM('iplimage.png', cv.CV_LOAD_IMAGE_COLOR)
    os.system('rm iplimage.png')
    return cvMat

def iplimage_to_cvMat_grayscale(iplimage):
    cv.SaveImage('iplimage.png', iplimage) #Saves the image
    cvMat = cv.LoadImageM('iplimage.png', cv.CV_LOAD_IMAGE_GRAYSCALE)
    os.system('rm iplimage.png')
    return cvMat

def cvMat_to_iplimage_color(cvMat):
    cv.SaveImage('cvMat.png', cvMat) #Saves the image
    iplimage= cv.LoadImage('cvMat.png', cv.CV_LOAD_IMAGE_COLOR)
    os.system('rm cvMat.png')
    return iplimage

def cvMat_to_iplimage_grayscale(cvMat):
    cv.SaveImage('cvMat.png', cvMat) #Saves the image
    iplimage= cv.LoadImage('cvMat.png', cv.CV_LOAD_IMAGE_GRAYSCALE)
    os.system('rm cvMat.png')
    return iplimage
