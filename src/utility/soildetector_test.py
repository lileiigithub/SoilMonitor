# -*- coding: utf-8 -*-
import numpy as np
import cv2
from sklearn import datasets
from sklearn.mixture import GaussianMixture
from sklearn.model_selection import StratifiedKFold
from datetime import datetime
import os

def train(_x_data):
    # 训练
    # 训练可以使用无监督或有监督
    n_classes = 3
    _model = GaussianMixture(n_components=n_classes, covariance_type='full',random_state=0,max_iter=20)
    _model.means_init = np.array([[0,0,0],[120,100,80],[225,225,225]]) # 使用标签初始化
    _model.fit(_x_data)
    return _model

def test(_model,_x_data):
    _y = _model.predict(_x_data)
    return _y

def pure_soil_picture(_raw_img_path,_y_predict):
    # _y_predict: 0:背景 1:土壤
    # if np.mean(_y_predict)<0.5: # 认为占比少的类为背景
    #     hidden_class = 0 # 隐藏类别１
    # else:hidden_class = 1 # 隐藏类别0
    hidden_class = 1
    PATH = "data/pure"
    img_name = datetime.now().date().strftime("%y%m%d") + datetime.now().time().strftime("_%H%M%S") +"_"+ _raw_img_path.split('/')[-1]
    img_path = os.path.join(PATH, img_name)
    img_arr = cv2.imread(_raw_img_path)
    img_shape = img_arr.shape
    img_arr_flatten = img_arr.reshape(-1,3)
    img_arr_flatten[_y_predict == 1] = [225,225,225]
    img_arr_flatten[_y_predict == 2] = [225, 225, 225]
    cv2.imwrite(img_path,img_arr_flatten.reshape(img_shape))

if __name__ == '__main__':
    import sys
    img_path = sys.argv[1] #"data/180524_172941.jpg"
    img_arr = cv2.imread(img_path)
    img_arr_flt = img_arr.reshape(-1,3)
    model = train(img_arr_flt)
    print("model means:", model.means_)
    print("model weights:", model.weights_)
    y_predict = test(model,img_arr_flt)
    print(y_predict.shape,y_predict)
    pure_soil_picture(img_path,y_predict)
