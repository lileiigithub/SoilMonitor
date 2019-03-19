# -*- coding: utf-8 -*-
import cv2
import os
import sys

# 添加环境变量
CUR_PATH = os.getcwd()
SRC_PATH = os.path.dirname(CUR_PATH)
MONITOR_PATH = os.path.join(SRC_PATH, "monitor")
sys.path.append(SRC_PATH)
sys.path.append(MONITOR_PATH)
for _path in sys.path:
    print(_path)

from src.monitor.dbscanClusterImg import Dbscan_cluster
from src.monitor.soilMonitorLog import SMLog

import numpy as np
np.set_printoptions(precision=2)

class CutAndCalc(object):
    def __init__(self,_img_path):
        self.img_path = _img_path
        self.name = _img_path.split("\\")[-1].split(".")[0] # window '\' and linux '/'
        self.weight = _img_path.split("\\")[-2]
        self.img_arr = cv2.imread(_img_path)
        self.img_shape = self.img_arr.shape
        # self.check_img_size()
        self.img_width = self.img_shape[0]
        self.img_length = self.img_shape[1]
        self.labels = []
        self.n_clusters_ = 0

    def cut_and_cal_img(self,_save_dir):
        rec_p = (380, 250)  # 截图顶点，numpy切片与opencv坐标相反
        self.subimg = self.img_arr[rec_p[1]:rec_p[1] + 100, rec_p[0]:rec_p[0] + 100, :]
        subimg_path = os.path.join(_save_dir, self.weight+"_"+self.name + "_sub.png")
        cv2.imwrite(subimg_path, self.subimg)
        cv2.rectangle(self.img_arr, rec_p, (rec_p[0] + 100, rec_p[1] + 100), (0, 0, 255))
        cv2.imwrite(os.path.join(_save_dir, self.weight+"_"+self.name + "_0.jpg"),self.img_arr)

        img_array = cv2.imread(subimg_path)
        db = Dbscan_cluster(img_array)
        # db.dbscan_claster_lab()
        soil_lab_means = db.dbscan_cluster(db.lab_arr)  # 对 lab值聚类
        SMLog.info("sub image lab mean：%s", soil_lab_means)
        return soil_lab_means


if __name__ == '__main__':

    import sys
    if len(sys.argv) >1:
        img_path = sys.argv[1]  #" data/180524_172941.jpg"
    else:
        img_path = r"E:\SoilMonitorData\data\318"

    several_mean = {}
    imgs = 1  # 文件夹的图片数量

    if(img_path.count(".jpg")==1): # 输出文件
            objectC =  CutAndCalc(img_path)
            objectC.cut_and_cal_img("")

    elif(img_path.count(".jpg")==0):  # # 输出文件夹
        img_dir = img_path
        dir_list = os.listdir(img_dir)
        img_list = []

        # remove file that is not image
        for item in dir_list:
            if(item.count(".jpg")>=1 or item.count(".JPG")>=1):
                img_list.append(item)
        imgs = len(img_list)
        for a_img in img_list:
            a_img_path = os.path.join(img_dir,a_img)
            SMLog.debug("处理图片：%s",a_img_path)
            objectC = CutAndCalc(a_img_path)
            processDir = os.path.join(img_dir, "processed")
            if os.path.exists(processDir) == False:
                os.mkdir(processDir)
            mean = objectC.cut_and_cal_img(processDir)
            several_mean[a_img] = mean  #
        SMLog.info("文件夹各副子图中心点：%s",several_mean)
        SMLog.info("文件夹各副子图中心点 均值: %s", np.array(list(several_mean.values())).sum(axis = 0)/imgs)

    else:
        print("error!!")

