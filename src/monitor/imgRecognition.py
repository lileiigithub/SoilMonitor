# -*- coding: utf-8 -*-

from preprocess import PreprocessImg
from soilDetectorGauss import GaussDetector
from dbscanClusterImg import Dbscan_cluster
from classification import Classification
import time
from datetime import datetime
import os
from globalData import Data
from soilMonitorLog import SMLog
from copy import deepcopy
import cv2

#############################################################################
## 图片识别算法,包括: 图像去噪、土壤图像分割、LAB转换、聚类
## 输入: 图片cv2的numpy数组
## 输出: 图片的分类序号(int)
#############################################################################

class RecognitionAlgorithm(object):

    def __init__(self,_bgr_arr,saveProImg = False):
        self.__start_time = time.time()
        self.bgr_arr = _bgr_arr
        self.saveProImg = saveProImg
        # 设置各种图片保存路径
        name_img_use_time = self.time_name()  # 180524_172850
        self.raw_img_path = Data.raw_img_folder+name_img_use_time+".jpg"
        self.filtered_img_path = Data.filtered_img_folder+name_img_use_time+".jpg"
        self.segmented_img_path = Data.segmented_img_folder+name_img_use_time+".jpg"
        self.clustered_img_path = Data.clustered_img_folder+name_img_use_time+".jpg"
        self.rectangle_img_path = Data.clustered_img_folder + name_img_use_time + "_sub.jpg"

    def implement(self):
        #
        bgr_arr = deepcopy(self.bgr_arr)
        cv2.imwrite(self.raw_img_path, bgr_arr) # 保存原始图片
        SMLog.info("保存原始图片")

        # 去噪处理
        # preprocess = PreprocessImg(bgr_arr)
        # preprocess.medianFilter()
        # bgr_arr = preprocess.get_filtered_arr()
        # Data.filtered_img_arr = bgr_arr  # 保存到Data
        # preprocess.save_filtered_img(self.filtered_img_path)  # 保存去噪后图片
        # SMLog.info("保存去噪后图片")
        # SMLog.info("去噪处理耗时(s): %s", preprocess.used_time)

        # 图像分割
        soildetector = GaussDetector(bgr_arr)
        segmented_bgr_arr = soildetector.soil_img_arr()
        Data.segmented_img_arr = soildetector.processed_rgb_arr_3d  # 保存到Data
        soildetector.save_segmented_img(self.segmented_img_path)  # 保存图像
        SMLog.info("保存分割后图片")
        SMLog.info("岩土检测耗时(s): %s", soildetector.used_time)

        # 区域聚类
        bgr_arr = deepcopy(segmented_bgr_arr)[250:350, 350:450, :]   #  截取中心 100*100 区域聚类
        db = Dbscan_cluster(bgr_arr)
        soil_mean = db.dbscan_cluster(db.lab_arr)

        rect_bgr_arr = deepcopy(segmented_bgr_arr)
        cv2.rectangle(rect_bgr_arr, (350, 250), (450, 350), (0, 0, 255))  # 画框
        cv2.imwrite(self.rectangle_img_path , rect_bgr_arr)
        SMLog.info("保存区域选择后图片")
        SMLog.info("岩土聚类中心：%s", soil_mean)
        bgr_arr = db.clustered_arr()
        Data.clustered_img_arr = bgr_arr  # 保存到Data
        cv2.imwrite(self.clustered_img_path,bgr_arr)  # 保存图像
        SMLog.info("保存聚类后图片")
        SMLog.info("岩土聚类耗时(s): %s", db.used_time)
        # 回归算法

        # imgprocessor = PreprocessImg(detected_img_arr)
        # X_data = imgprocessor.get_X()
        # Data.grayhist_img_arr = imgprocessor.thresh_gray_img
        # print("图片处理耗时(s): ", imgprocessor.used_time)
        # classifier = Classification(X_data)
        # class_index = classifier.predict()
        # print("图片分类耗时(s): ", classifier.used_time)
        # return class_index

    def time_name(self):
        img_time_name = datetime.now().date().strftime("%y%m%d") + datetime.now().time().strftime("_%H%M%S")
        return img_time_name

    @property
    def used_time(self):
        # 计算耗时
        return round(time.time()-self.__start_time,2)

if __name__ == '__main__':
    import cv2
    img_path = "data/180524_172941.jpg"
    reg = RecognitionAlgorithm(cv2.imread(img_path))
    print(reg.implement())
