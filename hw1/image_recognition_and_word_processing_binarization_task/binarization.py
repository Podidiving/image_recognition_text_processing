import PIL
from PIL import Image
import sys
import os
import time

from src.bradley import bradley_binarization
from src.otsu import otsu_binarization

if __name__ == '__main__':
    assert len(sys.argv) == 3 or len(sys.argv) == 4,  'Invalid number of parametres: ' +\
        'Must be : <path/to/dataset/folder/> <path/to/target/folder> ' +\
        '(optional) <binarization method (otsu or bradley) : bradley by default>'
    
    dataset_dir = sys.argv[1]
    target_dir = sys.argv[2]
    method = bradley_binarization

    if len(sys.argv) == 4:
        if sys.argv[3].lower() == 'otsu':
            method = otsu_binarization
        elif sys.argv[3].lower() == 'bradley':
            method = bradley_binarization
        else:
            print("Binarization method hasn't been recognized.\nUsing Bradley by default")

    if dataset_dir[-1] != '/':
        dataset_dir += '/'
    if target_dir[-1] != '/':
        target_dir += '/'

    assert os.path.isdir(dataset_dir), "Invalid path for dataset directory. It must be an existing directory"

    if not os.path.isdir(target_dir):
        os.mkdir(target_dir)


    average_second_per_mpx_speed = []
    for filename in os.listdir(dataset_dir):
        assert filename[-3:].lower() == 'jpg', 'Invalid image format: must be jpg'
        img = Image.open(dataset_dir + filename)

        start_time = time.time()
        res_img = method(img)
        finish_time =  time.time()

        work_time = finish_time - start_time

        secs_per_mpx = work_time / ((img.size[0] * img.size[1]) / 1000000.)
        average_second_per_mpx_speed.append(secs_per_mpx)
        print('work on {} done in {} seconds. \nsecond per megapixel speed: {}'
            .format(filename, round(work_time,5), round(secs_per_mpx,5)))
        res_img.save(target_dir + filename[:-3] + "png", "png")

    print("Algorithm done it's work")
    print("Binarized {} images".format(len(average_second_per_mpx_speed)))
    print("Average second per megapixel speed : {}"
        .format(sum(average_second_per_mpx_speed) / float(len(average_second_per_mpx_speed)) ))