# -*- coding: utf-8 -*-
'''
data visualization
'''
import cv2
from sklearn.cluster import DBSCAN
from sklearn import metrics
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from pylab import mpl
import time
time1 = time.time()
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei'] #指定默认字体   
mpl.rcParams['axes.unicode_minus'] = False #解决保存图像是负号'-'显示为方块的问题
# 论文画图, 湿度曝光一定时，lab值随光强的变化
def visual_lab_step_Lux():
    mpl.rcParams['font.sans-serif'] = ['SimHei'] #指定默认字体  
    data = [ [ 115.01 ,133.27 , 149.34],[ 138.37 , 127.56 , 150.93],[ 172.59 , 123.45 , 148.27], [ 196.65 , 115.91 , 153.16],
             [217.4  , 114.82 , 149.73],[ 236.01 , 115.06 ,145.62],[ 244.4 ,  115.33 , 145.05],[ 246.82 , 115.81 , 144.44]]
    lux = [235,371,510,652,799,891,922,952]
    data = np.array(data)
    l = data[:,0]
    a = data[:,1]
    b = data[:,2]
    # plt.subplot(3,1,1)
    font = FontProperties(fname=r"c:\windows\fonts\msyh.ttc", size=13)
    plt.tick_params(labelsize=14)  # set the font of scale
    plt.plot(lux,l,'k*-')
    plt.xlabel("光强/Lux",fontproperties=font)
    plt.ylabel("L 值",fontproperties=font)
    # plt.subplot(3,1,2)
    # plt.plot(lux,a)
    # plt.ylabel("a value")
    # plt.subplot(3,1,3)
    # plt.plot(lux,b)
    # plt.ylabel("b value")
    # plt.show()
    plt.savefig("save/stepLux_L.jpg",dpi=250)

def visual_rgb():
    data = [[ 78.02,103.49 ,121.23 ], [ 67.69 ,105.8, 120.93 ], [ 83.62, 107.29, 125.29 ], [ 80.26, 111.17 ,129.14 ],
            [81.65 ,107.86 ,128.4], [ 81.71 ,116.12 ,134.23 ], [ 82.68 ,119.17 ,137.85 ], [ 99.37, 127.87 ,141.21 ]]
    x = [14.51, 13.2, 12.3, 11.2, 9.1, 7.9, 6.9, 5.8]
    data = np.array(data)
    b = data[:,0]
    g = data[:,1]
    r = data[:,2]
    plt.subplot(3,1,1)
    plt.plot(x,r)
    plt.ylabel("R")
    plt.subplot(3,1,2)
    plt.plot(x,g)
    plt.ylabel("G")
    plt.subplot(3,1,3)
    plt.plot(x,b)
    plt.ylabel("B")
    plt.show()

class VisualData(object):
    def __init__(self,_data_path):
        self.path = _data_path
        self.line = []
        self.x = []
        self.y = []
        self.read_data(self.path);
        # print(self.line)
        self.split_data(self.line)
        # self.visual_data()
        # print(len(self.x),self.x)
        # print(len(self.y),self.y)

    def read_data(self,_path):
        with  open(_path) as file:
            for line in file.readlines():
                if line == "\n" or line == "" or line.count("#")>=1:
                    pass
                else:
                    self.line.append(line)

    def split_data(self,_line_list):
        for item in _line_list:
            item = item.strip()
            y = float(item.split(":")[0])
            x = item.split(":")[1]
            temp = x.strip().split("[")[-1].split("]")[0].strip()
            temp = temp.split(" ")
            temp_list = []
            for s in temp:
                if s!='':
                    temp_list.append(s)
            # print(temp_list)
            x = [float(temp_list[0]),float(temp_list[1]),float(temp_list[2])]
            y = (y - 856) / 616  # 实验一含水量计算公式
            y = y*100
            # x = (x - 1438) / 1198  # 实验二 含水量计算公式
            self.x.append(x)
            self.y.append(y)

    def visual_data(self):
        print(self.x)
        self.x = np.array(self.x)
        print(self.x.shape)
        a = self.x[:,1]
        b = self.x[:,2]

        plt.plot(self.y,a, 'o-')
        plt.plot(self.y,b, '*-')
        plt.legend(['a 值','b 值'])  # 图例
        plt.xlabel("岩土湿度(%)")
        plt.ylabel("数值")
        # plt.show()
        plt.savefig(r"data\save\lab_hum.png",dpi=320)

    def write_data_to_csv(self,_file_path):
        with open(_file_path,"w") as file:
            for index in range(len(self.x)).__reversed__():
                linein = str(round(self.y[index],2))+","+str(self.x[index][0])+","+str(self.x[index][1])+","+str(self.x[index][2])+"\n"
                file.writelines(linein)

if __name__ == '__main__':
    # visual_lab_step_Lux()
    # visual_lab_Lux922()
    # visual_level1()
    # visual_rgb()
    # visual_lab_Lux915()
    file_path = "data/-3expo.txt"
    # file_path = r"E:\UbuntuData\camera\-3expo-rgb\-3expo-rgb.txt"
    # file_path = "data_result.txt"
    # file_path = "bake.txt"
    vs = VisualData(file_path)
    vs.visual_data()
    # vs.write_data_to_csv("hum_lab.txt")











































