# -*- coding: utf-8 -*-

#############################################################################
## 开启多线程接收网络数据，调用算法
##
#############################################################################

from threading import Thread
from PyQt5.QtCore import QObject,pyqtSignal
import time
from globalData import Data
from network import Network
from imgRecognition import RecognitionAlgorithm
from soilMonitorLog import SMLog

class ReceiceImg(Thread,QObject):
    isHandled = True # 是否已经处理接收到的图片
    # isReceived = False # 是否已经接收到图片
    receivedSignal = pyqtSignal()
    def __init__(self):
        Thread.__init__(self) # 调用父类构造函数,不调用报错
        QObject.__init__(self)

        if Data.isOnline == True:  #在线检测
            # 连接网络
            address = Data.address # 获取ip地址,端口
            self.net = Network()
            self.net.create_connnect(address)
            SMLog.info("创建并连接网络!")

    def run(self):
        # 接收图片
        if Data.isOnline == True:  # 在线检测
            while True:
                try:
                    if ReceiceImg.isHandled==True:
                        self.net.send_a_message()
                        self.net.receice_a_message()
                        Data.raw_img_arr.flags.writeable = True
                        # ReceiceImg.isReceived = True
                        self.recognition_algorithm() # 在多线程里调用算法
                        # time.sleep(4)
                        ReceiceImg.isHandled = False
                        self.receivedSignal.emit()
                        # self.conn
                except Exception as e:
                    SMLog.error("在线检测多线程错误,错误原因:%s", e)

        else:  # 离线检测
            while True:
                try:
                    if ReceiceImg.isHandled==True:
                        self.recognition_algorithm() # 在多线程里调用算法
                        ReceiceImg.isHandled = False
                        self.receivedSignal.emit()
                except Exception as e:
                    SMLog.error("离线检测多线程错误,错误原因:%s", e)

    def recognition_algorithm(self):
        # 预测图片的类别算法
        # 包含 图片处理 土壤检测 类别预测
        reg = RecognitionAlgorithm(Data.raw_img_arr)
        reg.implement()
        Data.algorithm_used_time = reg.used_time
        SMLog.info("图像算法总耗时(s)：%s", reg.used_time)
