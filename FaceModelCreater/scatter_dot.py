import cv2
import numpy as np
import timeit
from random import randint
from random import *


def scatter_random(img_name, category, location_name,map_name,output_name, size_down,size_up,bright_down, bright_up,num):
    
    
    # img_clear = cv2.imread("face_image_texture_clear.tif",cv2.IMREAD_ANYCOLOR)
    # img_modify = cv2.imread("face_image_texture_clear.tif",cv2.IMREAD_ANYCOLOR)
    # img_blend = cv2.imread("face_image_texture_clear.tif",cv2.IMREAD_ANYCOLOR)

    img_clear = cv2.imread(img_name,cv2.IMREAD_ANYCOLOR)
    img_modify = cv2.imread(img_name,cv2.IMREAD_ANYCOLOR)
    img_blend = cv2.imread(img_name,cv2.IMREAD_ANYCOLOR)


    #boundary_map =cv2.imread("mapping.bmp",cv2.IMREAD_GRAYSCALE)
    boundary_map =cv2.imread(location_name,cv2.IMREAD_GRAYSCALE)

    dot_map = np.zeros((img_clear.shape[0],img_clear.shape[1],3),np.uint8)

    height = img_clear.shape[0]
    width = img_clear.shape[1]

  
    for y in range(0,height): 
        for x in range(0,width):
            dot_map[y,x,0]=255
            dot_map[y,x,1]=255
            dot_map[y,x,2]=255


    loc_x =0
    loc_y =0
    loc =0

    buffer_x =[]
    buffer_y =[]

    for i in range(0,num):
        iter =0
        sample_num = randint(1,5)
        
        if(category =="dot"):
            if(sample_num ==1):
                sample_dot = cv2.imread("dot/dot1.png", cv2.IMREAD_UNCHANGED)
            if(sample_num ==2):
                sample_dot = cv2.imread("dot/dot2.png", cv2.IMREAD_UNCHANGED)
            if(sample_num ==3):
                sample_dot = cv2.imread("dot/dot3.png", cv2.IMREAD_UNCHANGED)
            if(sample_num ==4):
                sample_dot = cv2.imread("dot/dot4.png", cv2.IMREAD_UNCHANGED)
            if(sample_num ==5):
                sample_dot = cv2.imread("dot/dot5.png", cv2.IMREAD_UNCHANGED)
    

        #resize_ratio = uniform(0.1, 0.3)
        resize_ratio = uniform(size_down, size_up)
        
        sample_resize = cv2.resize(sample_dot,dsize =( int(resize_ratio * sample_dot.shape[1]),int(resize_ratio * sample_dot.shape[0]) ),interpolation=cv2.INTER_AREA )
        
        sample_height = sample_resize.shape[0]
        sample_width = sample_resize.shape[1]

        
        while(loc<1):
        
            loc_x = randint(1,8800)
            loc_y = randint(1,5298)
            loc =2
        
            if( boundary_map[loc_y,loc_x]<128):
                loc =0
            
            if(i>0):
                for ii in range(0,i-1):
                    if(abs(buffer_x[ii]-loc_x)<200 and abs(buffer_y[ii]-loc_y)<200):
                        loc =0


        
        buffer_x.append(loc_x)
        buffer_y.append(loc_y)  
        loc=0

        for y in range(0,sample_height):
            for x in range(0,sample_width):
                if(sample_resize[y,x,3]!=0):
                    if(y+loc_y >4520 or x+loc_x >8120):
                        break
                    img_modify[y+loc_y, x+loc_x, 0]= sample_resize[y,x,0]
                    img_modify[y+loc_y, x+loc_x, 1]= sample_resize[y,x,1]
                    img_modify[y+loc_y, x+loc_x, 2]= sample_resize[y,x,2]

                    dot_map[y+loc_y, x+loc_x, 0]= sample_resize[y,x,0]
                    dot_map[y+loc_y, x+loc_x, 1]= sample_resize[y,x,1]
                    dot_map[y+loc_y, x+loc_x, 2]= sample_resize[y,x,2]

                

        cv2.rectangle(img_modify,(loc_x,loc_y),(loc_x + sample_width, loc_y +sample_height),(255,0,255),1 )
        
        


    #blend_ratio = uniform(0.6,0.9)
    blend_ratio = uniform(bright_down,bright_up)

    img_blend = cv2.addWeighted(img_clear,1- blend_ratio, img_modify, blend_ratio,0)

    # cv2.imwrite("dot_map.bmp",dot_map)
    #cv2.imwrite("random_dot.bmp", img_blend)

    cv2.imwrite(map_name,dot_map)
    cv2.imwrite(output_name, img_blend)


def define_number(skin_score):
    if(skin_score<5):
        return 10


#scatter_random("face_image_texture_clear.tif", "dot", "mapping.bmp","dot_map.bmp","random_dot.bmp", 0.1,0.3,0.6, 0.9,20)