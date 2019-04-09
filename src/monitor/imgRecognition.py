# -*- coding: utf-8 -*-

from preprocess import PreprocessImg
from soilDetectorGauss import GaussDetector
from dbscanClusterImg import Dbscan_cluster
from classification import Classification
from modelPredict import HumidityPredict
import time
from datetime import datetime
import os
from globalData import Data
from soilMonitorLog import SMLog
from copy import deepcopy
import cv2
import numpy as np
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
        Data.img_name = name_img_use_time+".jpg"
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
        Data.segmented_img_arr = segmented_bgr_arr  # soildetector.processed_rgb_arr_3d  # 保存到Data
        soildetector.save_segmented_img(self.segmented_img_path)  # 保存图像
        SMLog.info("保存分割后图片")
        SMLog.info("岩土检测耗时(s): %s", soildetector.used_time)
        # 区域聚类
        segmented_bgr_arr = deepcopy(self.bgr_arr)  #  不使用分割后的图像
        # 画框 begin
        rect_bgr_arr = deepcopy(segmented_bgr_arr)
        cv2.rectangle(rect_bgr_arr, (350, 250), (450, 350), (0, 0, 255))  # 画框
        cv2.imwrite(self.rectangle_img_path, rect_bgr_arr)
        SMLog.info("保存区域选择后图片")
        # 画框 end
        bgr_arr = deepcopy(segmented_bgr_arr)[250:350, 350:450, :]  # 截取中心 100*100 区域聚类
        db = Dbscan_cluster(bgr_arr)
        soil_mean = db.dbscan_cluster(db.lab_arr)
        if soil_mean == None:
            # 当聚类失败返回 None 时
            Data.soil_mean = soil_mean
            Data.clustered_img_arr = None
            Data.predict_result = None
            return
        # 聚类正常时
        Data.soil_mean = np.around(soil_mean,decimals=2)
        SMLog.info("岩土聚类中心：%s", soil_mean)
        bgr_arr = db.clustered_arr()
        Data.clustered_img_arr = bgr_arr  # 保存到Data
        cv2.imwrite(self.clustered_img_path,bgr_arr)  # 保存图像
        SMLog.info("保存聚类后图片")
        SMLog.info("岩土聚类耗时(s): %s", db.used_time)

        # 回归算法 , input: soil_mean
        hum_predictor = HumidityPredict(Data.model_path)
        predict_y = hum_predictor.regression_predict(soil_mean)
        SMLog.info("real:%s",predict_y)
        if predict_y <= 0:
            predict_y = np.random.rand()
        elif predict_y >= 20:
            predict_y = 20 + np.random.rand()
        else:
            pass
        Data.predict_result = np.around(predict_y,decimals=2)
        SMLog.info("湿度预测结果：%s", predict_y)
        SMLog.info("湿度预测耗时(s): %s", db.used_time)

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
