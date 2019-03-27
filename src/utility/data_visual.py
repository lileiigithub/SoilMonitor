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
        self.read_data(self.path)
        # self.split_data(self.line)

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
            # y = self.weight2hum_old(weight)
            y = self.hum2hum(weight)
            self.x.append(x)
            self.y.append(y)

    def weight2hum(self,_weight):
        # 实验一含水量计算公式
        _w = _weight
        _w = (_w - 1045) / (1045 - 240)
        _w = _w * 100
        return _w

    def hum2hum(self,_hum):
        # 实验一含水量计算公式
        return _hum

    def visual_data(self):
        # print(self.x)
        x,y = [],[]
        for item in self.line:
            item = item.strip()
            hum, L, a, b = float(item.split(",")[0]), float(item.split(",")[1]), float(item.split(",")[2]),float(item.split(",")[3])
            x, y = [L, a, b], hum
            self.x.append(x)
            self.y.append(y)
        plt.plot(self.y,self.x,"o-")
        plt.legend(["L值",'a 值','b 值'])  # 图例
        plt.xlabel("岩土湿度(%)")
        plt.ylabel("数值")
        # plt.savefig(r"data\paper\lab_hum.png", dpi=250)
        plt.show()

    def jiangsuPaper(self):
        for item in self.line:
            item = item.strip()
            hum,gray = float(item.split(",")[0]),float(item.split(",")[1])
            x,y = hum,gray
            self.x.append(x)
            self.y.append(y)
        plt.plot(self.x, self.y, "bo-")
        # plt.legend(["L值",'a 值','b 值'])  # 图例
        # plt.tick_params(labelsize=14)  # set the font of scale
        plt.xlabel("土壤含水量(%)")
        plt.ylabel("图像灰度值")
        plt.savefig("data/paper/jiangsuPaperGray.jpg", frameon=True, dpi=250)
        plt.show()

    def write_data_to_csv(self,_file_path):
        with open(_file_path,"w") as file:
            for index in range(len(self.x)).__reversed__():
                linein = str(round(self.y[index],2))+","+str(self.x[index][0])+","+str(self.x[index][1])+","+str(self.x[index][2])+"\n"
                file.writelines(linein)


if __name__ == '__main__':
    file_path = r"updata\visual_data.csv"
    file_path = r"updata\hum_lab_sim.csv"
    PATH = r"I:\Projects\SoilMonitor\src\utility\updata\hum_gray_jiangshu.csv"
    PATH = r"I:\Projects\SoilMonitor\src\utility\updata\hum_lab.csv"
    vs = VisualData(PATH)
    # vs.visual_data()
    vs.jiangsuPaper()
