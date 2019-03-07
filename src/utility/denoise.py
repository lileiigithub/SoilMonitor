# -*- coding: utf-8 -*-
'''
用于论文：图像预处理去噪对比图
使用均值滤波、中值滤波、高斯低通滤波
'''
import cv2
import numpy as np
from numpy import random
import matplotlib.pyplot as plt
import time
time1 = time.time()

############class Denoise##############
class Denoise(object):

    def __init__(self,_img_path):
        self.img_arr = cv2.imread(_img_path)
        self.img_shape = self.img_arr.shape
        self.img_width = self.img_shape[0]
        self.img_length = self.img_shape[1]
        self.img_folder = _img_path[:-4]

    def averageFilter(self):
        img = self.img_arr
        blur = cv2.blur(img, (3, 3))
        cv2.imwrite(self.img_folder+"_aver.jpg", blur)

    def medianFilter(self):
        img = self.img_arr
        median = cv2.medianBlur(img, 3)
        cv2.imwrite(self.img_folder+"_mid.jpg", median)

    def gaussianFilter(self):
        img = self.img_arr
        blur = cv2.GaussianBlur(img, (3, 3), 0)
        cv2.imwrite(self.img_folder+"_gaus.jpg", blur)


############class AddNoise##############
class AddNoise(object):
    def __init__(self,_img_path):
        self.img_arr = cv2.imread(_img_path)
        self.img_shape = self.img_arr.shape
        self.img_width = self.img_shape[0]
        self.img_length = self.img_shape[1]
        self.img_folder = _img_path[:-4]

    def addNoise(self):
        # img = self.img_arr
        # noise = cv2.addSaltNoise(img,)
        # cv2.imwrite(self.img_folder+"_noise.jpg", noise)
        # pass
        # self.addGaussianNoise(0.1)
        pass

    def addSaltNoise(self, percetage):
        # 添加椒盐噪声
        src  = self.img_arr
        SP_NoiseImg = src
        SP_NoiseNum = int(percetage * src.shape[0] * src.shape[1])
        print(SP_NoiseNum)
        for i in range(SP_NoiseNum):
            randX = random.random_integers(0, src.shape[0] - 1)
            randY = random.random_integers(0, src.shape[1] - 1)
            if random.random_integers(0, 1) == 0:
                SP_NoiseImg[randX, randY] = 0
            else:
                SP_NoiseImg[randX, randY] = 255
        cv2.imwrite(self.img_folder + "_salt_noise.jpg", SP_NoiseImg)

    def addGaussianNoise(self, percetage):
        # 添加高斯噪声
        # #error
        image = self.img_arr
        G_Noiseimg = image
        G_NoiseNum = int(percetage * image.shape[0] * image.shape[1])
        for i in range(G_NoiseNum):
            temp_x = np.random.randint(20, 40)
            temp_y = np.random.randint(20, 40)
            G_Noiseimg[temp_x][temp_y] = 255
            cv2.imwrite(self.img_folder + "_gaus_noise.jpg", G_Noiseimg)

if __name__ == '__main__':
    # src_img_path = "data/denoise/1.jpg"
    # an = AddNoise(src_img_path)
    # an.addGaussianNoise(0.1)

    src_img_path = "data/denoise/1_salt.jpg"
    dn = Denoise(src_img_path)
    dn.averageFilter()
    dn.medianFilter()
    dn.gaussianFilter()

