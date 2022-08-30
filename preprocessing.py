import cv2

def cut_image_into_pieces(img, size):
    height, width, channels = img.shape
    print(height, width)
    height_unit = int(height/size)
    width_unit = int(width/size)
    print(height_unit, width_unit)

    for i in range(size):
        for j in range(size):
            puzzle_id = i*size + j 
            
            img_crop = img[height_unit*(i): height_unit*(i+1), width_unit*(j): width_unit*(j+1)]
            print(f'temp/{puzzle_id}.jpg')
            # print(img_crop.shape)
            cv2.imwrite(f'temp/{puzzle_id}.jpg', img_crop)
            
    return height_unit, width_unit    