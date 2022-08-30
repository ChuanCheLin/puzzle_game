import cv2
import numpy as np
margin = 0.2

def cut_image_into_pieces(img, size):
    height, width, channels = img.shape
    print(height, width)
    height_unit = int(height/size)
    width_unit = int(width/size)
    print(height_unit, width_unit)

    # create alpha channel
    b_channel, g_channel, r_channel = cv2.split(img)
    alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255 # 0-255, 255 means no transparency
    # img = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
        
    for i in range(size):
        for j in range(size):
            img = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
            puzzle_id = i*size + j 
            
            if i == (size-1) and j == (size-1):
                img_crop = img[height_unit*(i): height_unit*(i+1)
                               , width_unit*(j): width_unit*(j+1)]
            elif i == (size-1): 
                img_crop = img[height_unit*(i): int(height_unit*(i+1)), 
                               width_unit*(j): int(width_unit*(j+1+margin))]
                cut_edges_convex(img_crop, "right", height_unit, width_unit)
            elif j == (size-1):       
                img_crop = img[height_unit*(i): int(height_unit*(i+1+margin)), 
                               width_unit*(j): int(width_unit*(j+1))]
                cut_edges_convex(img_crop, "bottom", height_unit, width_unit)
            else:
                img_crop = img[height_unit*(i): int(height_unit*(i+1+margin)), 
                               width_unit*(j): int(width_unit*(j+1+margin))]
                cut_edges_convex(img_crop, "right", height_unit, width_unit)
                cut_edges_convex(img_crop, "bottom", height_unit, width_unit)
            
            if i != 0:
                cut_edges_concave(img_crop, "top", height_unit, width_unit)
            if j != 0:
                cut_edges_concave(img_crop, "left", height_unit, width_unit)
            
            print(f'temp/{puzzle_id}.png')
            print(img_crop.shape)
            cv2.imwrite(f'temp/{puzzle_id}.png' ,img_crop)
            
    return height_unit, width_unit 

def cut_edges_convex(img_crop, side, height_unit, width_unit):
    if side == "right":
        img_crop[:int((1/3)*height_unit), width_unit:, 3] = 0
        img_crop[int((2/3)*height_unit):, width_unit:, 3] = 0
    elif side == "bottom":
        img_crop[height_unit:, :int((1/3)*width_unit), 3] = 0
        img_crop[height_unit:, int((2/3)*width_unit):, 3] = 0

def cut_edges_concave(img_crop, side, height_unit, width_unit):
    if side == "left":
        img_crop[int((1/3)*height_unit):int((2/3)*height_unit)
                 , :int(margin*width_unit), 3] = 0
    elif side == "top":
        img_crop[:int(margin*height_unit)
                 , int((1/3)*width_unit):int((2/3)*width_unit), 3] = 0