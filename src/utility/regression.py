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
from sklearn.externals import joblib

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
        self.get_xy(self.line)
        # self.split_dataset()

        self.now_test_x = self.x
        self.now_test_y = self.y

    def read_data(self, _path):
        with  open(_path) as file:
            for line in file.readlines():
                if line == "\n" or line == "" or line.count("#")>=1:
                    pass
                else:
                    self.line.append(line)

    def get_xy(self, _line_list):
        for item in _line_list:
            item = item.strip()

            # hum,L,a,b = float(item.split(",")[0]),float(item.split(",")[1]),float(item.split(",")[2]),float(item.split(",")[3])
            # x,y = [L,a,b],hum
            hum,gray = float(item.split(",")[0]),float(item.split(",")[1])
            x,y = [gray],hum
            # y = (weight-856)/616  # 实验一含水量计算公式
            # y = y*100
            # x = (x - 1438) / 1198  # 实验二 含水量计算公式
            self.x.append(x)
            self.y.append(y)

    def split_dataset(self):
        for index in range(len(self.x)):
            if index%4 == 0:
                self.test_x.append(self.x[index])
                self.test_y.append(self.y[index])
            else :
                self.train_x.append(self.x[index])
                self.train_y.append(self.y[index])

    def regression_model(self):
        # self.reg = linear_model.Lasso(alpha=0.1)
        # self.reg = linear_model.LassoLars(alpha=.1)
        # self.reg = linear_model.BayesianRidge()
        # self.reg = ElasticNet(alpha=0.1, l1_ratio=0.2)
        # self.reg  = tree.DecisionTreeRegressor()
        # self.reg  = svm.SVR()
        # self.reg = linear_model.Ridge (alpha = .5)
        alphas_ = np.arange(0.1,1,0.1)
        self.reg = linear_model.RidgeCV(alphas=alphas_, cv=4)  #  自带交叉验证，优化alpha参数
        # self.reg = KernelRidge(alpha = .8)
        # self.reg = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5,5), random_state=1)
        self.reg.fit(self.x, self.y)  # self.train_x, self.train_y
        print("alpha_:",self.reg.alpha_)

    def regression_predict(self):
        # self.predict_y = self.reg.predict(self.test_x)
        self.predict_y = self.reg.predict(self.now_test_x)
        print("预测值：",len(self.predict_y),self.predict_y)
        print("真实值：",len(self.now_test_y),self.now_test_y)

    def calc_loss(self):
        temp = np.abs(np.array(self.predict_y) - np.array(self.now_test_y)) # self.test_y
        # print(temp)
        temp = temp/np.array(self.now_test_y)
        print("误差：",temp*100)
        tmp = temp.sum()/len(self.now_test_x)
        self.loss = tmp
        print("loss:",self.loss)

    def show_data(self):
        # print(self.now_test_y)
        # print(self.predict_y)
        plt.plot(self.now_test_y, 'ro-')  # self.test_x,
        plt.plot(self.predict_y,'b*-') # self.test_x,
        plt.legend(["真实值","预测值"])
        plt.show()


    def validationShow(self):
        # plt.plot(np.array(self.x)[:,0],self.y ,'r*-')  # self.test_x,
        # plt.plot(np.array(self.now_test_x)[:, 0], self.predict_y, 'b*-')  # self.test_x,
        # 论文画图
        # font = FontProperties(fname=r"c:\windows\fonts\msyh.ttc", size=13)
        plt.xlabel("样本序号") #, fontproperties=font
        plt.ylabel("样本含水量(%)") # , fontproperties=font
        # plt.tick_params(labelsize=14)  #  set the font of scale
        # x = list(range(len(self.now_test_y)))
        # x = np.arange(0,20,4)
        # print(x)
        # plt.xticks(x)
        plt.plot(self.now_test_y ,'r^-')  # self.test_x,
        plt.plot(self.predict_y, 'bo-') # self.test_x,
        plt.legend(["真实值","预测值"])
        # plt.plot(self.predict_y,self.y,'b*-') # self.test_x,
        plt.savefig("data/paper/jiangsuPaper.jpg", frameon=True, dpi=250)  # , dpi=200
        plt.show()
        # plt.rcParams['savefig.dpi'] = 300  # 图片像素
        # plt.figure(frameon=False, dpi=250)
        # plt.savefig("save/3.jpg",frameon=True, dpi=250)#, dpi=200

    def save_model(self):
        joblib.dump(self.reg,"data/model/ridge.model")
        print("saved model.")

    def test_saved_model(self):
        self.reg = joblib.load("data/model/ridge.model")

if __name__ == '__main__':
    PATH = "updata/weight_lab.csv"
    PATH = r"I:\Projects\SoilMonitor\src\utility\updata\hum_lab_sim.csv"
    PATH = r"I:\Projects\SoilMonitor\src\utility\updata\hum_lab.csv"
    PATH = r"I:\Projects\SoilMonitor\src\utility\updata\sim_data.txt"
    # PATH = r"I:\Projects\SoilMonitor\src\utility\updata\hum_gray.csv"
    PATH = r"I:\Projects\SoilMonitor\src\utility\updata\hum_gray_jiangshu.csv"
    hr = HumidityRegression(PATH)
    hr.regression_model()

    # hr.save_model()
    # hr.test_saved_model()
    hr.regression_predict()
    hr.calc_loss()
    hr.validationShow()
    # hr.show_data()
    # hr.validationShow()