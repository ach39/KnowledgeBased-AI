# -*- coding: utf-8 -*-
"""
Created on Fri Sep 09 16:24:35 2016
 Utility functions  for Image processing

@author: achauhan
"""
import numpy as np
from PIL import Image
from PIL import ImageChops
import math,operator
from itertools import izip


#==============================================================================
#  Binarize : reutrns binary np array
#==============================================================================  
def binarize(im):
    im_L = im.convert('L')
    np_arr = np.array(im_L, dtype=np.uint8)

    for x in xrange(np_arr.shape[0]):
        for y in xrange(np_arr.shape[1]):
            np_arr[x][y] /= 255
    return np_arr
    
#******************************************************************************
# http://rosettacode.org/wiki/Percentage_difference_between_images 
# % of pixel difference in 2 images
#******************************************************************************
def find_image_diff(i1 , i2):
    pairs = izip(i1.getdata(), i2.getdata())
    if len(i1.getbands()) == 1:
        # for gray-scale jpegs
        dif = sum(abs(p1-p2) for p1,p2 in pairs)
    else:
        dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))
     
    ncomponents = i1.size[0] * i1.size[1] * 3
    #print "Difference (percentage):", (dif / 255.0 * 100) / ncomponents
    return (dif / 255.0 * 100) / ncomponents
 
#******************************************************************************
# Return Diff matrix for 2 givem np arrays . Consider using ImageChops.difference
#******************************************************************************
def find_diff(np1, np2):
    diff_matrix = get_diff_matrix(np1, np2)
    return np.sum(diff_matrix)/float(np1.shape[0] * np1.shape[1])   
    
def get_diff_matrix(np1, np2):    
    row =np1.shape[0]
    col =np1.shape[1]
    
    diff_np = np.zeros( (row, col) , dtype = float)
    for x in xrange(row):
        for y in xrange(col):
            diff_np[x][y] = abs( float(np1[x][y]) - float(np2[x][y]) )
            
    #diff_ratio = np.sum(diff_np)/float(row * col)       
    #print "diff_ratio = ", round(diff_ratio, 5)   
    return diff_np


    
#******************************************************************************
# RMS diff : Calculate the root-mean-square difference between two images"
#******************************************************************************
def rmsdiff(im1, im2):
    h = ImageChops.difference(im1, im2).histogram()

    # calculate rms
    return math.sqrt(reduce(operator.add,
        map(lambda h, i: h*(i**2), h, range(256))
    ) / (float(im1.size[0]) * im1.size[1]))   
    
#******************************************************************************
# Convert image to black and white
#******************************************************************************
def convert_bw(im):
    im_L = im.convert('L')
    np_arr = np.array(im_L, dtype=np.uint8)
    res = np.where(np_arr >= 128, 0, 1) 
    return res

#def convert_bw(image):
#    im_bw = image.convert('1')  
#    return im_bw
    
#******************************************************************************
# Returns ratio of blk_pixel_cnt of im2 to im1
# NOTE : 1 here denotes black pixel
#******************************************************************************
def get_blk_pixel_ratio(im1, im2):
    bw1 = convert_bw(im1)
    bw2 = convert_bw(im2)
    bw_ratio = float(np.count_nonzero(bw2)) / (np.count_nonzero(bw1))
    return bw_ratio

def get_blk_intersection_ratio(im1, im2) :
    bw1 = convert_bw(im1)
    bw2 = convert_bw(im2)
        
    combined_blk_pixel = np.count_nonzero(bw1) + np.count_nonzero(bw2)
    
    blk_intersect_cnt = 0.0
    intx_ratio = 0.0
    for x in xrange(bw1.shape[0]):
        for y in xrange(bw1.shape[1]):
            if(bw1[x][y] == 1) and (bw2[x][y] == 1) :
                blk_intersect_cnt += 1
        
    if(combined_blk_pixel>0):
        intx_ratio = blk_intersect_cnt/combined_blk_pixel
    
    #print  "blk_intersect_cnt :" ,  blk_intersect_cnt , "intx ratio = " , intx_ratio
    #print  "intx ratio = " , round(intx_ratio,5)
    return intx_ratio


#******************************************************************************
#******************************************************************************

    
    
    
#***************************************************************************************
def get_blk_pixel_cnt_L(im_np_arr):
    Total_pixel_cnt = float(im_np_arr.shape[0] * im_np_arr.shape[1])
    white_pixel_cnt = float(np.count_nonzero(im_np_arr))
    black_pixel_cnt = float(Total_pixel_cnt - white_pixel_cnt)
    return float(black_pixel_cnt)
    
#***************************************************************************************    
def get_blk_intersection_ratio_L(im1_np , im2_np) :

    if im1_np.shape != im2_np.shape :
        print "Size don't match"
        
    combined_blk_pixel = get_blk_pixel_cnt(im1_np) + get_blk_pixel_cnt(im2_np)
    #print combined_blk_pixel
    
    blk_intersect_cnt = 0.0
    intx_ratio = 0.0
    for x in xrange(im1_np.shape[0]):
        for y in xrange(im1_np.shape[1]):
            if(im1_np[x][y] == im2_np[x][y]) and (im1_np[x][y] == 0) :
                blk_intersect_cnt += 1
        
    if(combined_blk_pixel>0):
        intx_ratio = blk_intersect_cnt/combined_blk_pixel
    
    #print  "blk_intersect_cnt :" ,  blk_intersect_cnt , "intx ratio = " , intx_ratio
    #print  "intx ratio = " , round(intx_ratio,5)
    return intx_ratio

#***************************************************************************************
def get_blk_pixel_ratio_diff_L(im1 , im2):
    ratio_diff = abs(float(get_blk_pixel_ratio(im1)) - float(get_blk_pixel_ratio(im2)))
    print "blk_pixel_ratio_diff ;" , ratio_diff
    return ratio_diff
#***************************************************************************************
def get_blk_pixel_ratio_L(im_np_arr):    
    Total_pixel_cnt = float(im_np_arr.shape[0] * im_np_arr.shape[1])
    black_pixel_cnt = float(get_blk_pixel_cnt(im_np_arr))
    
    black_pixel_ratio =  black_pixel_cnt/Total_pixel_cnt
        
    # cross check B & W pixel via iteration
    zero_cnt =0 
    one_cnt  = 0
    for x in xrange(im_np_arr.shape[0]):
        for y in xrange(im_np_arr.shape[1]):
            if im_np_arr[x][y] == 0 :
                zero_cnt += 1
            else :
                one_cnt += 1
    #print  "1(White) cnt=" ,  one_cnt, "0(Black) cnt = " , zero_cnt ,
    #print " Blk Ratio= ", round(black_pixel_ratio,5)
    
    return black_pixel_ratio    
    