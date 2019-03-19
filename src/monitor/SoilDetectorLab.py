# -*- coding: utf-8 -*-
#############################################################################
## 使用AB值算法  图像分割，岩土检测
##
##
#############################################################################
import numpy as np
import cv2
from datetime import datetime
import time
import os
from soilMonitorLog import SMLog

class LabDetector(object):
    def __init__(self,_img_arr):
        self.start_time = time.time()
        self.bgr_arr = _img_arr
        self.arr_shape = self.bgr_arr.shape
        self.lab_arr = cv2.cvtColor(self.bgr_arr, cv2.COLOR_BGR2LAB)
        self.processed_bgr_arr = 0  # 处理好之后的图片数组

    def soil_img_arr(self, _a_range = (115,140), _b_range = (125,150)):
        self.lab_arr = self.lab_arr.reshape(-1,3)
        self.bgr_arr = self.bgr_arr.reshape(-1,3)
        for index in range(len(self.lab_arr)):
            l = self.lab_arr[index][0]
            a = self.lab_arr[index][1]
            b = self.lab_arr[index][2]
            if (a>=_a_range[0] and a<=_a_range[1]) and (b>=_b_range[0] and b<=_b_range[1]):
                pass
            else:
                self.bgr_arr[index] = np.array([255,255,255])
                
        self.processed_bgr_arr = self.bgr_arr.reshape(self.arr_shape)
        return self.processed_bgr_arr

    def save_soil_picture(self,_save_path):
        cv2.imwrite(_save_path, self.processed_bgr_arr)

    def time_relation_path(self):
        img_name = datetime.now().date().strftime("%y%m%d") + datetime.now().time().strftime("_%H%M%S")
        return img_name

    def save_segmented_img(self,_path):
        # 保存图片到硬盘
        cv2.imwrite(_path, self.processed_bgr_arr)

    @property
    def used_time(self):
        # 计算耗时
        return round(time.time()-self.start_time,2)

if __name__ == '__main__':
    import sys
    # img_path = sys.argv[1] #"data/180524_172941.jpg"
    img_path = "data/test/3.jpg"
    soildetctor = LabDetector(cv2.imread(img_path))
    soildetctor.soil_img_arr()
    pure_soil_path = img_path.split(".")[0]+"_"+soildetctor.time_relation_path()+".jpg"
    soildetctor.save_soil_picture(pure_soil_path)
    print(soildetctor.used_time)
