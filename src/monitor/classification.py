import sys
import time
import cv2
import numpy as np
from matplotlib import pyplot as plt
from sklearn import svm
from preprocess import PreprocessImg
from sklearn.externals import joblib
import collections
#############################################################################
## 分类类,接收cv2 imgarray,将数据分类
##
#############################################################################
class Classification(object):
    def __init__(self,_X_data):
        self.__start_time = time.time()
        self.X = _X_data
        self.model = joblib.load("model/train_model.m")  # load model

    def predict(self):
        # 输出: 预测的类别 (int)
        output_matrix = self.model.predict(self.X)
        count_dict = dict(collections.Counter(output_matrix))  # 统计生成字典
        print("预测细节：", count_dict)
        sorted_count_dict = sorted(count_dict.items(), key=lambda x: x[1], reverse=True)  # 根据字典value排序 eg:[(2, 260), (3, 40)]
        return sorted_count_dict[0][0]

    @property
    def used_time(self):
        # 计算耗时
        return round(time.time() - self.__start_time,2)

if __name__ == '__main__':
    '''测试'''
    img_path = "data/test.jpg"
    clf = Classification(img_path)
    print("测试结果: ",clf.predict())
