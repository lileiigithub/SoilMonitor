# -*- coding: utf-8 -*-
import cv2
import sys

def rgb2gray(_src_path,dst_path):
    img_arr = cv2.imread(_src_path)
    gray_gray = cv2.cvtColor(img_arr, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(dst_path,gray_gray)

if __name__ == '__main__':
    args = sys.argv
    if len(args)!=3:
        print("参数个数错误")
        assert 0
    rgb2gray(args[1],args[2])

