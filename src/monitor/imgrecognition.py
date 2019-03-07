# -*- coding: utf-8 -*-

from src.soildetector import Detector
from src.preprocess import PreprocessImg
from src.classification import Classification
import time
from src.globaldata import Data
#############################################################################
## 图片识别算法,包括: 土壤检测,图片处理,图片分类 三部分
## 输入: 图片cv2的numpy数组
## 输出: 图片的分类序号(int)
#############################################################################

class RecognitionAlgorithm(object):
    def __init__(self,_img_arr,saveProImg = False):
        self.__start_time = time.time()
        self.img_arr = _img_arr
        self.saveProImg = saveProImg

    @property
    def used_time(self):
        # 计算耗时
        return round(time.time()-self.__start_time,2)

    def implement(self):
        # output: the index of classification /int
        soildetector = Detector(self.img_arr)
        detected_img_arr = soildetector.soil_img_arr()
        if self.saveProImg == True: soildetector.save_pro_img()
        Data.processed_img_arr = soildetector.processed_rgb_arr_3d
        print("土壤检测耗时(s): ", soildetector.used_time)

        imgprocessor = PreprocessImg(detected_img_arr)
        X_data = imgprocessor.get_X()
        Data.grayhist_img_arr = imgprocessor.thresh_gray_img
        print("图片处理耗时(s): ", imgprocessor.used_time)

        classifier = Classification(X_data)
        class_index = classifier.predict()
        print("图片分类耗时(s): ", classifier.used_time)

        return class_index

if __name__ == '__main__':
    import cv2
    img_path = "data/180524_172941.jpg"
    reg = RecognitionAlgorithm(cv2.imread(img_path))
    print(reg.implement())