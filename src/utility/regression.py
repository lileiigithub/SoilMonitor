import time
time1 = time.time()
import cv2
from sklearn.cluster import DBSCAN
from sklearn import metrics
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.linear_model import ElasticNet
from sklearn import linear_model
from sklearn import tree
from sklearn import svm
from sklearn.kernel_ridge import  KernelRidge
from sklearn.neural_network import MLPClassifier
from matplotlib.font_manager import FontProperties
import time
time1 = time.time()
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei'] #指定默认字体   
mpl.rcParams['axes.unicode_minus'] = False #解决保存图像是负号'-'显示为方块的问题

class HumidityRegression(object):
    def __init__(self,_data_file):
        self.file = _data_file
        self.line = []
        self.x = []
        self.y = []
        self.train_x = []
        self.train_y = []
        self.test_x = []
        self.test_y = []

        self.read_data(self.file)
        self.split_data(self.line)
        self.split_dataset()

        self.now_test_x = self.x
        self.now_test_y = self.y

    def read_data(self, _path):
        with  open(_path) as file:
            for line in file.readlines():
                if line == "\n" or line == "" or line.count("#")>=1:
                    pass
                else:
                    self.line.append(line)

    def split_data(self, _line_list):
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
            y = (y-856)/616  # 实验一含水量计算公式
            y = y*100
            # x = (x - 1438) / 1198  # 实验二 含水量计算公式
            self.x.append(x)
            self.y.append(y)

    def split_dataset(self):
        for index in range(len(self.x)):
            if index%4 == 3:
                self.test_x.append(self.x[index])
                self.test_y.append(self.y[index])
            else :
                self.train_x.append(self.x[index])
                self.train_y.append(self.y[index])

    def regression_model(self):
        # self.reg = linear_model.Lasso(alpha=0.1)
        # self.reg = linear_model.LassoLars(alpha=.1)
        # self.reg = linear_model.BayesianRidge()
        self.reg = ElasticNet(alpha=0.1, l1_ratio=0.2)
        # self.reg  = tree.DecisionTreeRegressor()
        # self.reg  = svm.SVR()
        # self.reg = linear_model.Ridge (alpha = .5)
        # self.reg = KernelRidge(alpha = .8)
        # self.reg = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5,5), random_state=1)
        self.reg.fit(self.train_x, self.train_y)

    def regression_predict(self):
        # self.predict_y = self.reg.predict(self.test_x)
        self.predict_y = self.reg.predict(self.now_test_x)
        print(self.predict_y)
        print(self.now_test_y)

    def calc_loss(self):
        temp = np.abs(np.array(self.predict_y) - np.array(self.now_test_y)) # self.test_y
        print(temp)
        temp = temp/np.array(self.now_test_y)
        print("误差：",temp*100)
        tmp = temp.sum()/len(self.now_test_x)
        self.loss = tmp
        print("loss:",self.loss)

    def show_data(self):
        print(self.now_test_y)
        print(self.predict_y)
        plt.plot(self.now_test_y, 'r*-')  # self.test_x,
        plt.plot(self.predict_y,'b*-') # self.test_x,
        plt.show()
        # print(self.train_x)
        # print(self.train_y)
        # print(self.test_x)
        # print(self.test_y)
    def show_L_hum(self):
        # plt.plot(np.array(self.x)[:,0],self.y ,'r*-')  # self.test_x,
        # plt.plot(np.array(self.now_test_x)[:, 0], self.predict_y, 'b*-')  # self.test_x,
        # 论文画图
        font = FontProperties(fname=r"c:\windows\fonts\msyh.ttc", size=13)
        plt.xlabel("样本序号", fontproperties=font)
        plt.ylabel("样本含水量(%)", fontproperties=font)
        plt.tick_params(labelsize=14)  #  set the font of scale
        plt.plot(self.now_test_y ,'k^-',label="真实值")  # self.test_x,
        plt.legend()  # loc ='upper right',
        plt.plot(self.predict_y, 'ko-',label="预测值")  # self.test_x,
        plt.legend() #loc ='upper right',
        # plt.plot(self.predict_y,self.y,'b*-') # self.test_x,
        # plt.show()
        # plt.rcParams['savefig.dpi'] = 300  # 图片像素
        # plt.figure(frameon=False, dpi=250)
        plt.savefig("save/3.jpg",frameon=True, dpi=250)#, dpi=200


if __name__ == '__main__':
    PATH = "-3expo.txt"
    # PATH = r"E:\UbuntuData\camera\-3expo-rgb\-3expo-rgb.txt"
    hr = HumidityRegression(PATH)
    hr.regression_model()
    hr.elatic_net_predict()
    hr.calc_loss()
    # hr.show_data()
    hr.show_L_hum()