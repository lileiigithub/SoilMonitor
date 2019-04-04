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
        self.x = []
        self.hum = []
        self.train_x = []
        self.train_y = []
        self.test_x = []
        self.test_y = []

        self.read_data(self.file)
        self.now_test_x = self.x
        self.now_test_y = self.hum

    def read_data(self, _path):
        arr = np.genfromtxt(fname=_path, delimiter=",")
        self.hum = arr[:,0]  # hum
        self.x = arr[:,1:]  # features

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
        self.reg.fit(self.x, self.hum)  # self.train_x, self.train_y
        print("alpha_:",self.reg.alpha_)

    def regression_predict(self):
        # self.predict_y = self.reg.predict(self.test_x)
        self.predict_y = self.reg.predict(self.now_test_x)
        print("预测值：",self.predict_y.size,self.predict_y)
        print("真实值：",self.now_test_y.size,self.now_test_y)

    def calc_loss(self):
        temp = np.abs(self.predict_y - self.now_test_y)/np.array(self.now_test_y) # self.test_y
        print("误差：",temp*100)
        tmp = temp.sum()/self.now_test_x.size
        self.loss = tmp
        print("loss:",self.loss*100,"%")

    def RMSE(self):
        _sum = np.sum(np.square(self.predict_y - self.now_test_y))
        print(type(_sum),_sum)
        mse = _sum/float(self.predict_y.size)
        rmse = np.sqrt(mse)
        print("RMSE:",rmse)

    def validationShow(self):
        # 论文画图
        # font = FontProperties(fname=r"c:\windows\fonts\msyh.ttc", size=13)
        plt.xlabel("样本序号") #, fontproperties=font
        plt.ylabel("样本含水量(%)") # , fontproperties=font
        # plt.tick_params(labelsize=14)  #  set the font of scale
        # x = list(range(len(self.now_test_y)))
        x = np.arange(0, self.now_test_y.size, 4)  # 每隔 一定单位 下标显示整数
        plt.xticks(x)
        plt.plot(self.now_test_y ,'r^-')  # self.test_x,
        plt.plot(self.predict_y, 'bo-') # self.test_x,
        plt.legend(["真实值","预测值"])
        # plt.plot(self.predict_y,self.hum,'b*-') # self.test_x,
        # plt.savefig("data/paper/sim_high.jpg", frameon=True, dpi=250)  # , dpi=200
        plt.show()

    def save_model(self):
        joblib.dump(self.reg,"data/model/ridge.model")
        print("saved model.")

    def test_saved_model(self):
        self.reg = joblib.load("data/model/ridge.model")

if __name__ == '__main__':
    PATH = "updata/weight_lab.csv"
    PATH1 = r"I:\Projects\SoilMonitor\src\utility\updata\hum_lab_sim.csv"
    PATH2 = r"I:\Projects\SoilMonitor\src\utility\updata\hum_lab.csv"
    PATH3 = r"I:\Projects\SoilMonitor\src\utility\updata\hum_gray.csv"
    PATH4 = r"I:\Projects\SoilMonitor\src\utility\updata\hum_gray_jiangshu.csv"
    PATH5 = r"I:\Projects\SoilMonitor\src\utility\updata\sim_data.txt"
    PATH6 = r"I:\Projects\SoilMonitor\src\utility\updata\sim_data_low.txt"
    PATH7 = r"I:\Projects\SoilMonitor\src\utility\updata\sim_data_high.txt"
    PATH8 = r"I:\Projects\SoilMonitor\src\utility\updata\hum_Lab_qian_mdf.csv"
    hr = HumidityRegression(PATH8)
    hr.regression_model()
    # hr.save_model()
    # hr.test_saved_model()
    hr.regression_predict()
    # hr.calc_loss()
    hr.RMSE()
    hr.validationShow()
