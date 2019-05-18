from PIL import Image

def convert_rgb_to_monochrome(img : Image) -> list:
    '''
    Converts PIL.Image to monochrome image 

    @param img : original PIL.Image
    
    @return src : list of integers with len(img.width * img.height) - converting rgb to monochrome image
    '''
    r,g,b = img.split()
    r,g,b = r.tobytes(), g.tobytes(), b.tobytes()

    r_const = 0.2125
    g_const = 0.7154
    b_const = 0.0721
    return [int(r_const*r_ + g_const*g_ + b_const*b_) for (r_, g_, b_) in zip(r,g,b)]


def transfer_list_to_img(raw_img : list, size : tuple) -> Image:
    '''
    Transfer the list of integers back to PIL.Image
    
    @param raw_img : list of integers to convert to PIL.Image
    @param size : tuple(width, height) - shape of the result image !assert that len(raw_image) == (size[0] * size[1])

    @return img : PIL.Image
    '''
    return Image.frombytes("L", size, bytes(raw_img))