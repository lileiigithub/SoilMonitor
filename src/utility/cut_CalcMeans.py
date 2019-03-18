# -*- coding: utf-8 -*-
import cv2
import sys
import os
# # from dbscanClusterImg import Dbscan_cluster
import sys
sys.path.append("..")
print(sys.path)

from ..monitor.dbscanClusterImg import Dbscan_cluster
from ..monitor.soilMonitorLog import SMLog

import numpy as np
np.set_printoptions(precision=2)

class CutAndCalc(object):
    def __init__(self,_img_path):
        print("the path: ",_img_path)
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

    # cut the endless part
    def check_img_size(self):
        if self.img_shape == (672,802,3):
            self.img_arr = self.img_arr[50:650, 1:801, :]
            self.img_shape = self.img_shape
            cv2.imwrite(self.img_path, self.img_arr)
            print("截图!")

    def cut_and_cal_img(self,_save_dir = "tmpImg"):
        self.img1 = self.img_arr[200:300, 300:400, :]
        self.img2 = self.img_arr[200:300, 400:500, :]
        self.img3 = self.img_arr[300:400, 300:400, :]
        self.img4 = self.img_arr[300:400, 400:500, :]
        img1_path = os.path.join(_save_dir, self.weight+"_"+self.name + "_1.png")
        img2_path = os.path.join(_save_dir, self.weight+"_"+self.name + "_2.png")
        img3_path = os.path.join(_save_dir, self.weight+"_"+self.name + "_3.png")
        img4_path = os.path.join(_save_dir, self.weight+"_"+self.name + "_4.png")
        cv2.imwrite(img1_path, self.img1)
        cv2.imwrite(img2_path, self.img2)
        cv2.imwrite(img3_path, self.img3)
        cv2.imwrite(img4_path, self.img4)

        cv2.rectangle(self.img_arr,(300,200),(500,400),(0,0,255))
        cv2.line(self.img_arr,(300,300),(500,300),(0,0,255))
        cv2.line(self.img_arr, (400, 200), (400, 400), (0, 0, 255))
        cv2.imwrite(os.path.join(_save_dir, self.weight+"_"+self.name + "_0.jpg"),self.img_arr)
        imgs_path = [img1_path,img2_path,img3_path,img4_path]
        Lab_center_list = []
        for path in imgs_path:
            img_array = cv2.imread(path)
            db = Dbscan_cluster(img_array)
            # db.dbscan_claster_lab()
            means = db.dbscan_cluster(db.lab_arr)  #  对 lab值聚类
            Lab_center_list.append(means)
            Lab_center_list.sort()
        lab_mean = (np.array(Lab_center_list[1])+np.array(Lab_center_list[2]))/2  # mean
        SMLog.info("Lab_center_list: %s", Lab_center_list)
        SMLog.info("均值：%s",lab_mean)
        return lab_mean

if __name__ == '__main__':
    import sys
    img_path = sys.argv[1] #"data/180524_172941.jpg"
    # img_path = r"E:\UbuntuData\camera\bake"
    several_mean = []
    if(img_path.count(".jpg")==1): # input is a image name
    # path = "person.jpg"
        objectC =  CutAndCalc(img_path)
        objectC.cut_and_cal_img()

    elif(img_path.count(".jpg")==0):  # # input is a file of images
        img_dir = img_path
        dir_list = os.listdir(img_dir)
        img_list = []
        # remove file that is not image
        for item in dir_list:
            if(item.count(".jpg")>=1 or item.count(".JPG")>=1):
                img_list.append(item)
        for a_img in img_list:
            a_img_path = os.path.join(img_dir,a_img)
            print()
            print("################################")
            print("图片：",a_img_path)
            objectC = CutAndCalc(a_img_path)
            processDir = os.path.join(img_dir, "processed")
            if os.path.exists(processDir)==False:
                os.mkdir(processDir)
            mean = objectC.cut_and_cal_img(processDir)
            several_mean.append(mean.tolist())  # from array to list
        several_mean.sort()
        if len(several_mean)==4:
            print('\n', "4幅图片均值：", (np.array(several_mean[1]) + np.array(several_mean[2])) / 2)
        elif len(several_mean)==2:
            print('\n', "2幅图片均值：",(np.array(several_mean[0]) + np.array(several_mean[1])) / 2)
        else:
            print("图片不是2张或4张")
    else:
        print("error!!")

