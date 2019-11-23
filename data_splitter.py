'''
This is the script that was used to create the split dataset from the original cityscapes dataset.

'''

import glob
import os

import cv2 as cv
from cv2 import IMREAD_COLOR, WINDOW_AUTOSIZE, FILLED

cityscapes_dir = "/home/kirepreshanth/Documents/Dissertation/datasets/cityscapes"
gtFine_leftImg8bit_dir = cityscapes_dir + "/gtFine_trainvaltest/leftImg8bit"
split_dataset_dir = cityscapes_dir + "/split_dataset/leftImg8bit/"

def creatDirectoryIfNotExists(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)

creatDirectoryIfNotExists(split_dataset_dir)

for filePath in glob.glob(gtFine_leftImg8bit_dir + "/**/**/*.png"):
    pathParts = filePath.split('/')
    
    fileName = pathParts[-1]
    city = pathParts[-2]
    data_split = pathParts[-3]
        
    name, ext = fileName.split('.')
    fileName_split1 = name + "_01." + ext
    fileName_split2 = name + "_02." + ext
    fileName_split3 = name + "_03." + ext
        
    output_dir = split_dataset_dir + data_split + "/" + city + "/"
    creatDirectoryIfNotExists(split_dataset_dir + data_split)
    creatDirectoryIfNotExists(output_dir)

    '''
    Apply image resizing and split
    '''
    
    img = cv.imread(filePath, IMREAD_COLOR)
    scale = 50
    height = int(img.shape[0] * scale / 100)
    width = int(img.shape[1] * scale / 100)

    img = cv.resize(img, (width, height), interpolation = cv.INTER_AREA)
    shape = img.shape
    split_width = int(shape[1] / 3)

    split1 = img[0:height, 0:0+split_width]
    split2 = img[0:height, split_width:split_width*2]
    split3 = img[0:height, split_width*2:]
    
    '''
    Write final split images to directory
    '''
    
    cv.imwrite(output_dir + fileName_split1, split1)
    cv.imwrite(output_dir + fileName_split2, split2)
    cv.imwrite(output_dir + fileName_split3, split3)