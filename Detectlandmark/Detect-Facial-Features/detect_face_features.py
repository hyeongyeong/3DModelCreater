# import the necessary packages
from collections import OrderedDict
import numpy as np
import cv2
import argparse
import dlib
import imutils

facial_features_cordinates = {}

# define a dictionary that maps the indexes of the facial
# landmarks to specific face regions
FACIAL_LANDMARKS_INDEXES = OrderedDict([
    ("Jaw", (0, 17)),
    ("Right_Eyebrow", (17, 22)),
    ("Left_Eyebrow", (22, 27)),
    ("Nose", (27, 35)),
     ("Right_Eye", (36, 42)),
    ("Left_Eye", (42, 48)),
    ("Mouth", (48, 68)),
])

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
	help="path to facial landmark predictor")
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
args = vars(ap.parse_args())


def shape_to_numpy_array(shape, fileName):
    # initialize the list of (x, y)-coordinates
    coordinates = np.zeros((68, 2),dtype="int")
    splited = fileName.split('.')
    print(splited[0].split('/')[1])
    FN = "%s.pts" %(splited[0].split('/')[1])
    # loop over the 68 facial landmarks and convert them
    # to a 2-tuple of (x, y)-coordinates
    text = open(FN,'w')
    str1= ('version: 1')
    str2=('\nn_points: 68\n{\n')
    text.write(str1)
    text.write(str2)
    print(str1)
    print(str2)
    for i in range(0, 68):
        coordinates[i] = (shape.part(i).x, shape.part(i).y)
        data1 = ('%d' %(shape.part(i).x))
        data2 = (' %d\n' %(shape.part(i).y))
        print(data1,data2)
        text.write(data1)
        text.write(data2)

    str3 =('}')
    print(str3)
    text.write(str3) 
    text.close()
    # return the list of (x, y)-coordinates
    return coordinates

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

# load the input image, resize it, and convert it to grayscale
image = cv2.imread(args["image"])
# image = imutils.resize(image, width=500)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# detect faces in the grayscale image
rects = detector(gray, 1)

# loop over the face detections
for (i, rect) in enumerate(rects):
    # determine the facial landmarks for the face region, then
    # convert the landmark (x, y)-coordinates to a NumPy array
    shape = predictor(gray, rect)
    shape = shape_to_numpy_array(shape,args["image"])