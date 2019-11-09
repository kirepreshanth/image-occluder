'''
This is the script that is used to create the occluded dataset from the original cityscapes dataset.

First dataset will be each quarter of the center of the image occluded.

TODO: abstract out the functionality to apply the occlusion to the image so that different occlusions can be applied to the dataset.

'''

import glob
import os

import cv2 as cv
from cv2 import IMREAD_COLOR, WINDOW_AUTOSIZE, FILLED

cityscapes_dir = "/home/kirepreshanth/Documents/Dissertation/datasets/cityscapes"
gtFine_leftImg8bit_dir = cityscapes_dir + "/gtFine_trainvaltest/leftImg8bit"
occluded_centerOcclusion_dir = cityscapes_dir + "/occluded_dataset/leftImg8bit_coa/"
occlusion_size = 256

def creatDirectoryIfNotExists(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)

creatDirectoryIfNotExists(occluded_centerOcclusion_dir)

for filePath in glob.glob(gtFine_leftImg8bit_dir + "/**/**/*.png"):
    pathParts = filePath.split('/')
    
    fileName = pathParts[-1]
    city = pathParts[-2]
    data_split = pathParts[-3]
        
    name, ext = fileName.split('.')
    # fileName_cul = name + "_cul." + ext
    # fileName_cur = name + "_cur." + ext
    # fileName_cbl = name + "_cbl." + ext
    # fileName_cbr = name + "_cbr." + ext
    
    fileName_c = name + "_c256x256." + ext
    
    output_dir = occluded_centerOcclusion_dir + data_split + "/" + city + "/"
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
    center = (int(shape[1] / 2), int(shape[0] / 2))

    occlusion_width = int(occlusion_size * scale / 100)
    occlusion_height = int(occlusion_size * scale / 100)

    # upperLeft = (center[0] - occlusion_width, center[1] - occlusion_height)
    # upperRight = (center[0] + occlusion_width, center[1] - occlusion_height)
    # bottomLeft = (center[0] - occlusion_width, center[1] + occlusion_height)
    # bottomRight = (center[0] + occlusion_width, center[1] + occlusion_height)

    # #UPPER LEFT OF CENTER
    # ulimg = cv.rectangle(img.copy(), center, upperLeft, (255, 255, 255), thickness=FILLED)
    # #UPPER RIGHT OF CENTER
    # urimg = cv.rectangle(img.copy(), upperRight, center, (255, 255, 255), thickness=FILLED)
    # #BOTTOM LEFT OF CENTER
    # blimg = cv.rectangle(img.copy(), bottomLeft, center, (255, 255, 255), thickness=FILLED)
    # #BOTTOM RIGHT OF CENTER
    # brimg = cv.rectangle(img.copy(), bottomRight, center, (255, 255, 255), thickness=FILLED)

    half_occlusion_width = int(occlusion_width / 2) - 2
    half_occlusion_height = int(occlusion_height / 2) - 2


    centerStart = (center[0] + half_occlusion_width), (center[1] + half_occlusion_height)
    centerEnd = (center[0] - half_occlusion_width), (center[1] - half_occlusion_height)
    cimg = cv.rectangle(img.copy(), centerStart, centerEnd, (255, 255, 255), thickness=FILLED)

    '''
    Write final occluded images to directory
    '''
    
    # cv.imwrite(output_dir + fileName_cul, ulimg)
    # cv.imwrite(output_dir + fileName_cur, urimg)
    # cv.imwrite(output_dir + fileName_cbl, blimg)
    # cv.imwrite(output_dir + fileName_cbr, brimg)
    
    cv.imwrite(output_dir + fileName_c, cimg)

# cv.namedWindow( "Test Image 1", WINDOW_AUTOSIZE);
# cv.namedWindow( "Test Image 2", WINDOW_AUTOSIZE);
# cv.namedWindow( "Test Image 3", WINDOW_AUTOSIZE);
# cv.namedWindow( "Test Image 4", WINDOW_AUTOSIZE);
# cv.imshow("Test Image 1", ulimg)
# cv.imshow("Test Image 2", urimg)
# cv.imshow("Test Image 3", blimg)
# cv.imshow("Test Image 4", brimg)
# cv.waitKey(10000)
# cv.destroyAllWindows()