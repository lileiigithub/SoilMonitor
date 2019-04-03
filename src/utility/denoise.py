# -*- coding: utf-8 -*-
'''
用于论文：图像预处理去噪对比图
使用均值滤波、中值滤波、高斯低通滤波
'''
import cv2
import numpy as np
from numpy import random
import matplotlib.pyplot as plt
from skimage.util import random_noise
from skimage import io
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
        cv2.imwrite(self.img_folder+"_filter_aver.jpg", blur)

    def medianFilter(self):
        img = self.img_arr
        median = cv2.medianBlur(img, 3)
        cv2.imwrite(self.img_folder+"_filter_mid.jpg", median)

    def gaussianFilter(self):
        img = self.img_arr
        blur = cv2.GaussianBlur(img, (3, 3), 0)
        cv2.imwrite(self.img_folder+"_filter_gaus.jpg", blur)


############class AddNoise##############
class AddNoise(object):
    def __init__(self,_img_path):
        self.img_arr = cv2.imread(_img_path)
        self.img_shape = self.img_arr.shape
        self.img_width = self.img_shape[0]
        self.img_length = self.img_shape[1]
        self.img_path = _img_path
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
        cv2.imwrite(self.img_folder + "_noise_salt.jpg", SP_NoiseImg)

    def addGaussianNoise(self):
        # 添加高斯噪声
        # #error
        image = io.imread("data/denoise/1_noise_salt.jpg")
        G_Noiseimg = random_noise(image,mode='gaussian',var=0.02)
        io.imsave(self.img_folder + "_noise_salt_gauss.jpg", G_Noiseimg)

if __name__ == '__main__':
    src_img_path = "data/denoise/1.jpg"
    an = AddNoise(src_img_path)
    an.addSaltNoise(0.05)
    an.addGaussianNoise()

    src_img_path = "data/denoise/1_noise_salt_gauss.jpg"
    dn = Denoise(src_img_path)
    dn.averageFilter()
    dn.medianFilter()
    dn.gaussianFilter()

