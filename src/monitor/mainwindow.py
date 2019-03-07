#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############################################################################
## 主窗口
##
#############################################################################

from PyQt5.QtCore import QFile, QFileInfo, QSettings, Qt, QTextStream,QThread
from PyQt5.QtGui import QKeySequence,QFont,QPixmap,QImage,QRgba64
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow,QLabel,QPushButton,QWidget,QSpacerItem,
                             QMessageBox, QTextEdit, QGraphicsView, QTextBrowser, QGraphicsScene,QHBoxLayout,QVBoxLayout)
from PyQt5 import QtWidgets
from datetime import datetime
import cv2
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')

from networkset import NetworkDialog
from imgrecognition import RecognitionAlgorithm
from globaldata import Data
from thread import ReceiceImg

# 使用 matplotlib中的FigureCanvas (在使用 Qt5 Backends中 FigureCanvas继承自QtWidgets.QWidget)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MainWindow(QMainWindow):
    windowList = []

    def __init__(self):
        super(MainWindow, self).__init__()
        # 菜单
        self.recentFileActs = []
        # 将mainwindow的中心组件设置为widget,然后在里面布局
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.createActions()
        self.createMenus()
        self.statusBar()

        #主界面
        self.img_label = QLabel("原始土壤图片")
        self.img_label.setAlignment(Qt.AlignCenter) # label 居中
        self.img_label.setFont(QFont("Roman times", 12)) #, QFont.Bold
        self.raw_img_view = QGraphicsView()

        self.pro_img_label = QLabel("处理后土壤图片")
        self.pro_img_label.setAlignment(Qt.AlignCenter) # label 居中
        self.pro_img_label.setFont(QFont("Roman times", 12)) #, QFont.Bold
        self.pro_img_view = QGraphicsView()

        self.chooseImgButton = QPushButton("选取图片")
        self.onlineButton = QPushButton("在线检测")

        self.grayHistogram_label = QLabel("分类说明")
        self.grayHistogram_label.setAlignment(Qt.AlignCenter) # label 居中
        self.grayHistogram_label.setFont(QFont("Roman times", 12)) #, QFont.Bold
        self.gray_Hist_view = QTextBrowser()
        self.gray_Hist_view.setReadOnly(True)
        self.gray_Hist_view.setFont(QFont("Roman times", 12))
        information = "类别  ：    湿度\n"+"类别0： 0%-2.5%\n"+"类别1： 2.5%-7.5%\n"+"类别2： 7.5%-12.5%\n"+"类别3： 12.5%-17.5%\n"+"类别4： 17.5%-22.5%\n"+"类别5： 22.5%及以上\n"

        self.gray_Hist_view.setText(information)

        self.text_label = QLabel("湿度识别结果")
        self.text_label.setAlignment(Qt.AlignCenter) # label 居中
        self.text_label.setFont(QFont("Roman times", 12))
        self.result_text = QTextBrowser()
        self.result_text.setReadOnly(True)
        self.result_text.setFont(QFont("Roman times", 12))#, QFont.Bold
        self.hide_button = QPushButton("")
        # self.hide_button.setVisible(False)
        # 布局
        leftDown_layout = QHBoxLayout()
        leftDown_layout.addWidget(self.chooseImgButton)
        leftDown_layout.addWidget(self.onlineButton)

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.img_label)
        left_layout.addWidget(self.raw_img_view)
        left_layout.addWidget(self.pro_img_label)
        left_layout.addWidget(self.pro_img_view)
        left_layout.addLayout(leftDown_layout)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.grayHistogram_label)
        right_layout.addWidget(self.gray_Hist_view)
        right_layout.addWidget(self.text_label)
        right_layout.addWidget(self.result_text)
        right_layout.addWidget(self.hide_button)
        mainlayout = QHBoxLayout()
        mainlayout.addLayout(left_layout)
        mainlayout.addLayout(right_layout)
        self.widget.setLayout(mainlayout)
        #
        self.setWindowTitle("土壤含水量在线检测上位机")
        self.setGeometry(250,100,1080,820) # posx,posy,w,h

        self.chooseImgButton.clicked.connect(self.clicked_local_button) # 更新各种信息
        self.onlineButton.clicked.connect(self.clicked_online_button)  # 更新各种信息

        self.networkset = None  # 网络设置
        self.ReceiceImgThread = None # 多线程


    def newFile(self):
        other = MainWindow()
        MainWindow.windowList.append(other)
        other.show()

    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self)
        if fileName:
            self.loadFile(fileName)

    def save(self):
        pass

    def openRecentFile(self):
        action = self.sender()
        if action:
            self.loadFile(action.data())

    def about(self):
        QMessageBox.about(self, "soil monitor","土壤含水量在线检测系统上位机 ")

    def cameraSetDialog(self):
        pass

    def networkDialog(self):
        # 设置网络
        self.networkset = NetworkDialog()
        self.networkset.show()

    def online_show_analysis_calculate_image(self):
        self.showImageArray(Data.raw_img_arr,self.raw_img_view)
        self.showImageArray(Data.processed_img_arr, self.pro_img_view)
        self.show_result()
        # QApplication.processEvents()
        ReceiceImg.isHandled = True  # 标记已处理图片,可以开启新的接收

    def local_show_analysis_calculate_image(self):
        self.showImageArray(Data.processed_img_arr, self.pro_img_view)
        self.show_result()

    def clicked_local_button(self):
        # 本地检测功能
        Data.isOnline = False
        if self.chooseImg(): # 更新图片地址
            self.showImageArray(Data.raw_img_arr, self.raw_img_view)
            # if type(img_arr) == "":
            # self.local_show_analysis_calculate_image()
            if self.ReceiceImgThread == None:  # 确保线程只开启一次
                self.ReceiceImgThread = ReceiceImg()
                self.ReceiceImgThread.receivedSignal.connect(self.local_show_analysis_calculate_image)
                self.ReceiceImgThread.start()
            else:
                ReceiceImg.isHandled = True

    def clicked_online_button(self):
        # 在线检测功能
        Data.isOnline = True
        if self.ReceiceImgThread == None:  # 确保线程只开启一次
            self.ReceiceImgThread = ReceiceImg()
            self.ReceiceImgThread.receivedSignal.connect(self.online_show_analysis_calculate_image)
            self.ReceiceImgThread.start()

    def chooseImg(self):
        """
        选取本地图片并返回路径
        """
        img_path = ''
        imageFile, _ = QFileDialog.getOpenFileName(self,
                "Choose an image file to open", img_path, "Images (*.*)")
        if imageFile != '':
            img_path = imageFile
            print("img path: ",img_path)
            # Data.raw_img_path = img_path
            Data.raw_img_arr = cv2.imread(img_path)
            return True
        else: return False

    def showImageFile(self, imageFile, _QGraphicsView_obj):
        # 显示图片
        # input: image path, QGraphicsView object
        pixmap = QPixmap(imageFile)
        scene = QGraphicsScene()
        pixmap = pixmap.scaled(_QGraphicsView_obj.size(),Qt.KeepAspectRatio)
        scene.clear()
        scene.addPixmap(pixmap)
        _QGraphicsView_obj.setScene(scene)

    def showHistgram(self):
        hist_data = Data.grayhist_img_arr
        self.figure.clear()
        ax = self.figure.add_axes([0.1, 0.1, 0.6, 0.6])
        ax.hist(hist_data.ravel(), 256, [0, 256])
        self.gray_Hist_canvas.draw()


    def showImageArray(self, _bgrimg, _QGraphicsView_obj):
        # 显示图片
        # input: image path, QGraphicsView object
        rgbimg = cv2.cvtColor(_bgrimg, cv2.COLOR_BGR2RGB)
        qimg = QImage(rgbimg.data,rgbimg.shape[1],rgbimg.shape[0],QImage.Format_RGB888)
        pixmap = QPixmap(qimg)
        scene = QGraphicsScene()
        pixmap = pixmap.scaled(_QGraphicsView_obj.size(),Qt.KeepAspectRatio)
        scene.clear()
        scene.addPixmap(pixmap)
        _QGraphicsView_obj.setScene(scene)


    def show_result(self):
        #显示预测输出结果
        str_date = datetime.now().date().isoformat()
        str_time = datetime.now().time().isoformat()
        result_str = "日期: "+str_date+'\n'+"时间: "+str_time+'\n'+"预测类别结果为: "+"类别"+str(Data.predicted_classification)
        result_str += "\n算法耗时(s): "+str(Data.algorithm_used_time)
        self.result_text.setText(result_str)
        # self.result_text.show()

    def createActions(self):
        self.newAct = QAction("&New", self, shortcut=QKeySequence.New,
                              statusTip="Create a new file", triggered=self.newFile)

        self.openAct = QAction("&Open...", self, shortcut=QKeySequence.Open,
                               statusTip="Open an existing file", triggered=self.open)

        self.saveAct = QAction("&Save", self, shortcut=QKeySequence.Save,
                               statusTip="Save the document to disk", triggered=self.save)

        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q",
                               statusTip="Exit the application",
                               triggered=QApplication.instance().closeAllWindows)

        self.aboutAct = QAction("&About", self,
                                statusTip="Show the application's About box",
                                triggered=self.about)

        self.aboutQtAct = QAction("About &Qt", self,
                                  statusTip="Show the Qt library's About box",
                                  triggered=QApplication.instance().aboutQt)

        self.cameraSet = QAction("摄像头", self,
                                 statusTip="设置摄像头参数",
                                 triggered=self.cameraSetDialog)

        self.networkSet = QAction("网络", self,
                                 statusTip="设置网络连接",
                                 triggered=self.networkDialog)

    def createMenus(self):
        # 创建菜单
        self.fileMenu = self.menuBar().addMenu("&文件")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.separatorAct = self.fileMenu.addSeparator()
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.menuBar().addSeparator()
        self.setting = self.menuBar().addMenu("&设置")
        self.setting.addAction(self.cameraSet)
        self.setting.addAction(self.networkSet)

        self.helpMenu = self.menuBar().addMenu("&帮助")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def loadFile(self, fileName):
        pass

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
