# -*- coding: utf-8 -*-
'''
data visualization
'''
import numpy as np
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
        self.x = []
        self.hum = []
        self.read_data(self.path)

    def read_data(self,_path):
        arr = np.genfromtxt(fname=_path, delimiter=",")
        self.hum = arr[:,0]  # hum
        self.x = arr[:,1:]  # features

    def visual_data(self):
        plt.plot(self.hum,self.x,"o-")
        plt.legend(["L值",'a 值','b 值'])  # 图例
        plt.xlabel("岩土湿度(%)")
        plt.ylabel("数值")
        # plt.savefig(r"data\paper\lab_hum.png", dpi=250)
        plt.show()

    def jiangsuPaper(self):
        plt.plot( self.hum,self.x, "bo-")
        plt.xlabel("土壤含水量(%)")
        plt.ylabel("图像灰度值")
        # plt.savefig("data/paper/jiangsuPaperGray.jpg", frameon=True, dpi=250)
        plt.show()

    def weight2hum(self,_weight):
        # 实验一含水量计算公式
        _w = _weight
        _w = (_w - 1045) / (1045 - 240)
        _w = _w * 100
        return _w

    def write_data_to_csv(self,_file_path):
        # np.savetxt(_file_path, arr_, fmt='%s', delimiter=',')
        pass


if __name__ == '__main__':
    file_path = r"updata\visual_data.csv"
    file_path = r"updata\hum_lab_sim.csv"
    # PATH = r"I:\Projects\SoilMonitor\src\utility\updata\hum_gray_jiangshu.csv"
    PATH = r"I:\Projects\SoilMonitor\src\utility\updata\hum_lab.csv"
    vs = VisualData(PATH)
    vs.visual_data()
    # vs.jiangsuPaper()
