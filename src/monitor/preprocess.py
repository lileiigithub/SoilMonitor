# -*- coding: UTF-8
'''
 # 滤波预处理图像
'''
import cv2
import numpy as np
from matplotlib import pyplot as plt
import time

class PreprocessImg(object):
    # 滤波处理图像
    def __init__(self,_bgr_arr):
        self.__start_time = time.time()
        self.bgr_arr = _bgr_arr
        self.filtered_arr = None

    def averageFilter(self):
        # 均值滤波
        img = self.bgr_arr
        self.filtered_arr = cv2.blur(img, (3, 3))

    def medianFilter(self):
        # 中值滤波
        img = self.bgr_arr
        self.filtered_arr = cv2.medianBlur(img, 3)

    def gaussianFilter(self):
        # 高斯滤波
        img = self.bgr_arr
        self.filtered_arr = cv2.GaussianBlur(img, (3, 3), 0)

    def save_filtered_img(self,_path):
        # 保存滤波后图像
        cv2.imwrite(_path, self.filtered_arr)

    def get_filtered_arr(self):
        return self.filtered_arr

    @property
    def used_time(self):
        # 计算耗时
        return round(time.time()-self.__start_time,2)

if __name__ == '__main__':
    img_path = "data/180529_202903_180524_172941.jpg"
    img_array = cv2.imread(img_path)
    pre = PreprocessImg(img_array)
    print("使用时间: ",pre.used_time)





