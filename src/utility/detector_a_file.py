# -*- coding: utf-8 -*-
#############################################################################
## 调用soildetector.py 接口检测一个文件夹的土壤图片
##
##
#############################################################################
# from collections import
import os
import cv2
from src.soildetector import Detector

def file_list(_path):
    # 从文件夹得到需要检测的文件
    imgs_list = []
    mainFile =  [os.path.join(_path,f) for f in os.listdir(_path)]
    print(mainFile)
    for file in mainFile:
        for imgs_name in [os.path.join(file,i) for i in os.listdir(file)]:
            if imgs_name.count(".jpg")>=1:
                print(imgs_name)
                imgs_list.append(imgs_name)
    return  imgs_list

def detect_soil(_img_name):
    # 输入：图片路径
    # 输出： 土壤高斯的中心点值
    print("图片：",_img_name,"\n")
    soildetctor = Detector(cv2.imread(_img_name))
    print("model means:", soildetctor.model.means_)
    # print("model weights:", soildetctor.model.weights_)
    soildetctor.soil_img_arr()
    pure_soil_path = "../data/pure/" + _img_name.split("/")[-2]+"_"+_img_name.split("/")[-1]
    soildetctor.save_soil_picture(pure_soil_path)
    print("高斯中心点：",soildetctor.model.means_[soildetctor.get_soil_class()])
    return soildetctor.model.means_[soildetctor.get_soil_class()]

def record2txt(_txt_path,_list):
    with open(_txt_path,"w") as file:
        for item in _list:
            s = "{:.2f} {:.2f} {:.2f}  {}\n".format(item[1][0], item[1][1], item[1][2], item[0])
            file.writelines(s)

if __name__ == '__main__':
    path = "/home/lilei/data/土壤烘干称重"
    txt_path = "record.txt"
    imgs_list = file_list(path)
    print_list = []
    for item in imgs_list:
        center = detect_soil(item).tolist()
        print_list.append([item,center])
    for item in print_list:
        print(item[0],item[1])
    record2txt(txt_path,print_list)





