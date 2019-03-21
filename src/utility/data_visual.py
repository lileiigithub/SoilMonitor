# -*- coding: utf-8 -*-
'''
data visualization
'''
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

class VisualData(object):
    def __init__(self,_data_path):
        self.path = _data_path
        self.line = []
        self.x = []
        self.y = []
        self.read_data(self.path);
        self.split_data(self.line)

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
            weight = float(item.split(",")[0])
            x = [float(item.split(",")[1]),float(item.split(",")[2]),float(item.split(",")[3])]
            y = weight
            y = (y - 1045)/(1045-240)  # 实验一含水量计算公式
            y = y*100
            self.x.append(x)
            self.y.append(y)

    def visual_data(self):
        print(self.x)
        self.x = np.array(self.x)
        [L, a, b] = self.x.T  #装置后按行取
        plt.plot(self.y, L, "*-")
        plt.plot(self.y, a, "*-")
        plt.plot(self.y, b, "*-")
        plt.legend(["L值",'a 值','b 值'])  # 图例
        plt.xlabel("岩土湿度(%)")
        plt.ylabel("数值")
        plt.show()
        # plt.savefig(r"data\save\lab_hum.png",dpi=320)

    def write_data_to_csv(self,_file_path):
        with open(_file_path,"w") as file:
            for index in range(len(self.x)).__reversed__():
                linein = str(round(self.y[index],2))+","+str(self.x[index][0])+","+str(self.x[index][1])+","+str(self.x[index][2])+"\n"
                file.writelines(linein)


if __name__ == '__main__':
    file_path = r"updata\visual_data.csv"
    vs = VisualData(file_path)
    vs.visual_data()
