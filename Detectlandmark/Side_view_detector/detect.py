# import the necessary packages
from collections import OrderedDict
import numpy as np
import cv2
import argparse
import dlib
import imutils
import sys
import os


def run(shape_predictor, image):
    
    cur_path = os.path.dirname(os.path.abspath(__file__))
    facial_features_cordinates = {}

    # define a dictionary that maps the indexes of the facial
    # landmarks to specific face regions
    FACIAL_LANDMARKS_INDEXES = OrderedDict([
        ("Nose", (0, 6)),
        ("Mouth", (6, 13)),
        ("Jaw", (13, 20)),
        ("Eyebrow", (20, 23)),
        ("Eye", (23, 26)),
        ("Forehead", (26, 28))
    ])




    def shape_to_numpy_array(shape, dtype="int"):
        # initialize the list of (x, y)-coordinates
        coordinates = np.zeros((28, 2), dtype=dtype)

        # loop over the 68 facial landmarks and convert them
        # to a 2-tuple of (x, y)-coordinates
        for i in range(0, 28):
            coordinates[i] = (shape.part(i).x, shape.part(i).y)

        # return the list of (x, y)-coordinates
        return coordinates


    def visualize_facial_landmarks(image, shape, file_name, colors=None, alpha=0.6):
        # create two copies of the input image -- one for the
        # overlay and one for the final output image
        overlay = image.copy()
        output = image.copy()

        # if the colors list is None, initialize it with a unique
        # color for each facial landmark region
        if colors is None:
            colors = [(0, 255, 109), (0, 0, 255), (255, 159, 0),
                    (255, 100, 255), (255, 255, 0),
                    (255, 0, 0), (180, 0, 255)]

        # loop over the facial landmark regions individually
        str1= ('version: 1')
        str2=('\nn_points: 28\n{\n')
        file_name.write(str1)
        file_name.write(str2)
        for (i, name) in enumerate(FACIAL_LANDMARKS_INDEXES.keys()):
            # grab the (x, y)-coordinates associated with the
            # face landmark
            print(name)
            (j, k) = FACIAL_LANDMARKS_INDEXES[name]
            pts = shape[j:k]
            facial_features_cordinates[name] = pts

            for point in pts:
                print(point[0], point[1])
                file_name.write("%d %d\n" % (point[0], point[1]))
                file_name.flush()
                cv2.circle(overlay, (point[0], point[1]), 2, (0,0,0), -1)



            # check if are supposed to draw the jawline
            if name == "Jaw" or name == "Forehead":
                # since the jawline is a non-enclosed facial region,
                # just draw lines between the (x, y)-coordinates
                for l in range(1, len(pts)):
                    ptA = tuple(pts[l - 1])
                    ptB = tuple(pts[l])
                    cv2.line(overlay, ptA, ptB, colors[i], 2)

            # otherwise, compute the convex hull of the facial
            # landmark coordinates points and display it
            else:
                hull = cv2.convexHull(pts)
                cv2.drawContours(overlay, [hull], -1, colors[i], -1)
        # apply the transparent overlay
        str3 =('}')
        file_name.write(str3)
        cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)

        # return the output image
    #    print(facial_features_cordinates)
        return output

    # initialize dlib's face detector (HOG-based) and then create
    # the facial landmark predictor
    #detector = dlib.get_frontal_face_detector()

    file_name = open(os.path.join(cur_path,'output/side_point.pts'), "w")
    cnn_face_detector = dlib.cnn_face_detection_model_v1(os.path.join(cur_path, 'cnn.dat'))
    predictor = dlib.shape_predictor(os.path.join(cur_path,shape_predictor))
    # load the input image, resize it, and convert it to grayscale
    image = cv2.imread(os.path.join(cur_path,'images/'+image))
    tif_name = os.path.join(cur_path, 'output/side.tif')
    cv2.imwrite(tif_name,image)
    #image = imutils.resize(image, width=500)
    #image = cv2.resize(image, dsize=(256,256))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # detect faces in the grayscale image
    #rects = detector(gray, 1)
    rects = cnn_face_detector(gray, 1)

    # loop over the face detections
    for (i, rect) in enumerate(rects):
        # determine the facial landmarks for the face region, then
        # convert the landmark (x, y)-coordinates to a NumPy array
        print("find %d face" % (i+1))
    #    shape = predictor(gray, rect)
        shape = predictor(gray, rect.rect)
        shape = shape_to_numpy_array(shape)

        output = visualize_facial_landmarks(image, shape, file_name)
        cv2.rectangle(output, (rect.rect.left(), rect.rect.top()), (rect.rect.right(), rect.rect.bottom()), (1, 0, 0))
        cv2.imshow("Side_landmark_Detect", output)
        cv2.waitKey(0)
    file_name.close()
