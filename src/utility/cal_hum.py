# -*- coding: utf-8 -*-
'''
读取实验文件，计算含水量后重新写入。
'''
import numpy as np
import matplotlib.pyplot as plt
import time
time1 = time.time()

# 论文画图, 湿度曝光一定时，lab值随光强的变化

class CalHum(object):
    def __init__(self,_data_path):
        self.path = _data_path
        self.Lab = []
        self.weight = []
        self.hum = []
        self.read_data(self.path)
        self.weight2hum()

    def read_data(self,_path):
        arr = np.genfromtxt(fname=_path, delimiter=",")
        self.weight = arr[:,0]
        self.Lab = arr[:,1:]

    def weight2hum(self):
        # 实验含水量计算公式
        self.hum = (self.weight-1045)/(1045-240)
        self.hum = self.hum * 100
        self.hum = np.around(self.hum, decimals=3).reshape(-1,1)  #  设置精度
        return self.hum

    def write_data_to_csv(self,_file_path):
        arr_ = np.hstack((self.hum,self.Lab))
        np.savetxt(_file_path, arr_, fmt='%s', delimiter=',')
        pass


if __name__ == '__main__':
    PATH = r"updata\w_Lab_qian.csv"
    vs = CalHum(PATH)
    print(vs.hum.shape,vs.hum)
    print(vs.Lab.shape)
    save_path  = "updata\hum_Lab_qian.csv"
    vs.write_data_to_csv(save_path)
