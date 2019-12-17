'''
This is the script that is used to create the occluded dataset from the original cityscapes dataset.

The output is a dataset with 3 occlusions.

'''

import glob
import os

import cv2 as cv
from cv2 import IMREAD_COLOR, WINDOW_AUTOSIZE, FILLED

cityscapes_dir = "datasets/cityscapes"
gtFine_leftImg8bit_dir = cityscapes_dir + "/gtFine_trainvaltest/leftImg8bit/val"
occluded_centerOcclusion_dir = cityscapes_dir + "/occluded_dataset/leftImg8bit/"
occlusion_size = 256

def creatDirectoryIfNotExists(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)

creatDirectoryIfNotExists(occluded_centerOcclusion_dir)


# Loop through the images in the original dataset folder
for filePath in glob.glob(gtFine_leftImg8bit_dir + "/**/*.png"):
    
    '''
    Create Directories for output dataset
    '''
    
    pathParts = filePath.split('/')
    
    fileName = pathParts[-1]
    city = pathParts[-2]
    data_split = pathParts[-3]
            
    output_dir = occluded_centerOcclusion_dir + data_split + "/" + city + "/"
    creatDirectoryIfNotExists(occluded_centerOcclusion_dir)
    creatDirectoryIfNotExists(occluded_centerOcclusion_dir + data_split)
    creatDirectoryIfNotExists(output_dir)

    '''
    Apply image transformation and occlusion
    '''
    
    img = cv.imread(filePath, IMREAD_COLOR)
    scale = 100
    height = int(img.shape[0] * scale / 100)
    width = int(img.shape[1] * scale / 100)

    img = cv.resize(img, (width, height), interpolation = cv.INTER_AREA)
    shape = img.shape
    
    center_split = (int(shape[1] / 2), int(shape[0] / 2))
    
    ## Split the width of the image by 3
    split_width = int(shape[1] / 3)    
    
    first_split = (int(split_width / 2), int(shape[0] / 2))
    last_split = ((split_width * 2) + first_split[0], int(shape[0] / 2))

    occlusion_width = int(occlusion_size * scale / 100)
    occlusion_height = int(occlusion_size * scale / 100)
    
    half_occlusion_width = int(occlusion_width / 2) - 2
    half_occlusion_height = int(occlusion_height / 2) - 2
    
    # Calculate the start and end of the first occlusion
    firstStart = (first_split[0] + half_occlusion_width), (first_split[1] + half_occlusion_height)
    firstEnd = (first_split[0] - half_occlusion_width), (first_split[1] - half_occlusion_height)
    
    # Calculate the start and end of the second occlusion
    centerStart = (center_split[0] + half_occlusion_width), (center_split[1] + half_occlusion_height)
    centerEnd = (center_split[0] - half_occlusion_width), (center_split[1] - half_occlusion_height)
    
    # Calculate the start and end of the third occlusion
    lastStart = (last_split[0] + half_occlusion_width), (last_split[1] + half_occlusion_height)
    lastEnd = (last_split[0] - half_occlusion_width), (last_split[1] - half_occlusion_height)
    
    # Past all three occlusions in the original image
    cimg = cv.rectangle(img.copy(), firstStart, firstEnd, (255, 255, 255), thickness=FILLED)
    cimg = cv.rectangle(cimg, centerStart, centerEnd, (255, 255, 255), thickness=FILLED)
    cimg = cv.rectangle(cimg, lastStart, lastEnd, (255, 255, 255), thickness=FILLED)

    '''
    Write final occluded images to directory
    '''
    
    cv.imwrite(output_dir + fileName, cimg)