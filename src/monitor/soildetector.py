# -*- coding: utf-8 -*-
#############################################################################
## 土壤检测
##
##
#############################################################################
import numpy as np
import cv2
from sklearn.mixture import GaussianMixture
from sklearn.model_selection import StratifiedKFold
from datetime import datetime
import time
import os

class Detector(object):
    def __init__(self,_img_arr):
        self.start_time = time.time()

        self.rgb_or_gray = "rgb" # 选择训练rgb图
        self.rgb_arr_3d = _img_arr
        assert self.rgb_arr_3d.shape[-1] == 3 # 必须输入为彩图
        if self.rgb_or_gray == "rgb":
            self.rgb_arr_1d = self.rgb_arr_3d.reshape(-1,3)
            self.img_arr_1d = self.rgb_arr_1d
        else:
            self.gray_arr_3d = cv2.cvtColor(self.rgb_arr_3d,cv2.COLOR_RGB2GRAY) # 转灰度图
            self.gray_arr_1d = self.gray_arr_3d.reshape(-1, 1) # 拉平
            self.img_arr_1d = self.gray_arr_1d
        self.model = self.train()
        self.processed_rgb_arr_3d = 0  # 处理好之后的图片数组

    def train(self):
        # 训练
        # 训练可以使用无监督或有监督
        n_classes = 3
        _model = GaussianMixture(n_components=n_classes, covariance_type='full',random_state=0,max_iter=20)
        if self.rgb_or_gray == "rgb":
            _model.means_init = np.array([[0,0,0],[120,100,80],[225,225,225]]) # 使用标签初始化
        else:
            _model.means_init = np.array([[0], [100], [255]])  # 使用标签初始化
        _model.fit(self.img_arr_1d)
        return _model

    def test(self):
        _y = self.model.predict(self.img_arr_1d)
        return _y

    def soil_img_arr(self):
        _y_predict = self.test()
        classes = [0,1,2]  # 3个类别
        soil_class = self.get_soil_class()  # 减去土壤的类别
        #soil_class = 2
        print("soil_class: ",soil_class)
        del classes[soil_class]
        img_shape = self.rgb_arr_3d.shape
        img_arr_3d_flatten = self.rgb_arr_3d.reshape(-1,3) # (r,g,b)
        img_arr_3d_flatten[_y_predict == classes[0]] = [255]
        img_arr_3d_flatten[_y_predict == classes[1]] = [255]
        self.processed_rgb_arr_3d = img_arr_3d_flatten.reshape(img_shape)
        # Data.processed_img_arr = self.processed_rgb_arr_3d
        return self.processed_rgb_arr_3d

    def get_soil_class(self):
        '''
        选择土壤类别的条件:
        1: (r,g,b)  r<g<b --> (r-g)(g-b)>0 && (r-g)<0
        2: 满足1条件下所占像素点比例较多的类
        '''
        calss_mean = self.model.means_
        calss_weight = self.model.weights_
        judge_size = list((calss_mean[:,0]-calss_mean[:,1])*(calss_mean[:,1]-calss_mean[:,2]))
        # print("judge_size:",judge_size)
        judge_size1 = list((calss_mean[:,0]-calss_mean[:,1]))
        # print("judge_size1:",judge_size1)
        all_classes = [0,1,2]
        soil_class = []
        # 将不满足条件的类别从soil_class中删除
        for i in range(len(all_classes)):
            if judge_size[i]>0 and judge_size1[i]<0:
                soil_class.append(i)
            else:
                pass

        if len(soil_class) == 0:
            return 0
        elif len(soil_class) == 1:
            return soil_class[0]
        else:
            calss_weight = calss_weight[soil_class]
            return np.where(calss_weight==np.max(calss_weight))[0][0]

    def save_soil_picture(self,_save_path):
        cv2.imwrite(_save_path, self.processed_rgb_arr_3d)

    def time_relation_path(self):
        PATH = "data/pure"
        img_name = datetime.now().date().strftime("%y%m%d") + datetime.now().time().strftime("_%H%M%S") +"_"+ self.path.split('/')[-1]
        img_path = os.path.join(PATH, img_name)
        return img_path

    def save_pro_img(self,_path = "temp/pro_img.jpg"):
        # 保存图片到硬盘
        cv2.imwrite(_path, self.processed_rgb_arr_3d)

    @property
    def used_time(self):
        # 计算耗时
        return round(time.time()-self.start_time,2)

if __name__ == '__main__':
    import sys
    img_path = sys.argv[1] #"data/180524_172941.jpg"
    soildetctor = Detector(cv2.imread(img_path))
    print("model means:", soildetctor.model.means_)
    print("model weights:", soildetctor.model.weights_)
    soildetctor.soil_img_arr()
    # y_predict = soildetctor.test()
    # print(y_predict.shape,y_predict)
    pure_soil_path = img_path.split("/")[-1]
    soildetctor.save_soil_picture(pure_soil_path)
    # pure_soil_picture(img_path,y_predict)
