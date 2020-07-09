import cv2
import numpy as np 
import timeit


def change_color_uvmap(img_name,out_name, bright_value):
    
    img = cv2.imread(img_name,cv2.IMREAD_COLOR)
    out = img.copy()

    b,g,r = cv2.split(img)
    imgre = cv2.merge((b,g,r))

    height = img.shape[0]
    width = img.shape[1]

    bright = bright_value

    if(bright<0):
        M= np.ones(img.shape, dtype ="uint8")*bright *(-1)
        out = cv2.subtract(img, M)

    if(bright>0):
        M= np.ones(img.shape, dtype ="uint8")*bright
        out = cv2.add(img, M)

    cv2.imwrite(out_name,out)

    return out


change_color_uvmap("face_image_texture_clear.tif","face_CL_albedo_color.bmp", 30)
