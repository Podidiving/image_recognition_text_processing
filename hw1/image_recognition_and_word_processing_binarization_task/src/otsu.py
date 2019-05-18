from PIL import Image
from src.helpers import convert_rgb_to_monochrome, transfer_list_to_img


# The number of intensity levels of the image.
INTENSITY_LAYER_NUMBER = 256


def binarize_by_threshold(src : list, threshold : float, size: tuple) -> Image:
    '''
    Binarize src image by threshold

    @param src : flattened monochrome image
    @param threshold : threshold to binarize by
    @param size : size of the resulting image (width, height)

    @return img : binarized image
    '''
    res = [0 for _ in range(size[0]*size[1])]
    for i in range(len(src)):
        if src[i] < threshold:
            res[i] = 0
        else:
            res[i] = 255
    return transfer_list_to_img(res, size)


def calculate_hist(src : list) -> list:
    '''
    Returns the histogram by image intensity
    
    @param src : flattened monochrome image
    
    @return hist : resulting histogram
    '''
    hist = [0 for _ in range(INTENSITY_LAYER_NUMBER)]
    for i in range(len(src)):
        hist[src[i]] += 1
    return hist


def calculate_intensity_sum(src : list) -> int:
    '''
    Calculate the sum of all intensities.

    @param src : flattened monochrome image

    @return total : resulting sum
    '''
    total = 0
    for i in range(len(src)):
        total += src[i]
    return total


def otsu_binarization(img: Image) -> Image:
    '''
    Otsu binarization algorithm

    @params img :  original image

    @return res : binarized image
    '''
    src = convert_rgb_to_monochrome(img)
    width, height = img.size
    hist = calculate_hist(src)
    all_pixels_count = width * height
    all_intensity_sum = calculate_intensity_sum(src)
    best_thresh = 0
    best_sigma = 0.

    first_class_pixel_count = 0
    first_class_intensity_sum = 0

    for threshold in range(INTENSITY_LAYER_NUMBER - 1):
        first_class_pixel_count += hist[threshold]
        first_class_intensity_sum += threshold * hist[threshold]
        if first_class_pixel_count == all_pixels_count:
            break
        elif first_class_pixel_count == 0:
            continue

        first_class_prob = first_class_pixel_count / float(all_pixels_count)
        second_class_prob = 1. - first_class_prob

        first_class_mean = first_class_intensity_sum / float(first_class_pixel_count)
        second_class_mean = (all_intensity_sum - first_class_intensity_sum) / \
                             float(all_pixels_count - first_class_pixel_count)
        
        mean_delta = first_class_mean - second_class_mean
        sigma = first_class_prob * second_class_prob * mean_delta * mean_delta

        if sigma > best_sigma:
            best_sigma = sigma
            best_thresh = threshold

    return binarize_by_threshold(src, best_thresh, img.size)

