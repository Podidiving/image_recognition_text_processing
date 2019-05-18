from PIL import Image
from src.helpers import convert_rgb_to_monochrome, transfer_list_to_img


def bradley_binarization(img : Image) -> Image:
    '''
    Bradley binarization algorithm

    @params img :  original image

    @return res : binarized image
    '''
    src = convert_rgb_to_monochrome(img)
    width, height = img.size
    S = width // 8
    s2 = S // 2
    thresh = 0.15
    integral_image = 0
    total, count, index = 0, 0, 0
    x1, x2, y1, y2 = 0, 0, 0, 0

    integral_image = [0 for _ in range(width * height)] 
    res = [0 for _ in range(width * height)]

    for i in range(width):
        total = 0
        for j in range(height):
            index = j * width + i
            total += src[index]
            if i==0:
                integral_image[index] = total
            else:
                integral_image[index] = integral_image[index - 1] + total
    
    for i in range(width):
        for j in range(height):
            index = j * width + i
            x1, x2, y1, y2 = i - s2, i + s2, j - s2, j + s2

            if x1 < 0:
                x1 = 0
            if x2 >= width:
                x2 = width - 1
            if y1 < 0:
                y1 = 0
            if y2 >= height:
                y2 = height - 1

            count = (x2 - x1) * (y2 - y1)

            total = integral_image[y2*width + x2] - integral_image[y1*width + x2] -\
				    integral_image[y2*width + x1] + integral_image[y1*width + x1]

            if src[index] * count < total * (1. - thresh):
                res[index] = 0
            else:
                res[index] = 255
    
    return transfer_list_to_img(res, img.size)

