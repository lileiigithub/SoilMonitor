import cv2
import numpy as np
from matplotlib import pyplot as plt
import time
import os

class Rgb2lab:
    def __init__(self, _img_path):
        self.__start_time = time.time()
        self.img_path = _img_path
        self.img_name_ = self.img_path.split("/")[-1]
        self.img_arr = cv2.imread(_img_path)
        self.img_shape = self.img_arr.shape
        self.img_width = self.img_shape[0]
        self.img_length = self.img_shape[1]
        self.labimg = cv2.cvtColor(self.img_arr, cv2.COLOR_BGR2LAB)
        self.L = self.labimg[:, :, 0:1].flatten().reshape(self.img_width, self.img_length)
        self.a = self.labimg[:, :, 1:2].flatten().reshape(self.img_width, self.img_length)
        self.b = self.labimg[:, :, 2:3].flatten().reshape(self.img_width, self.img_length)
        print(self.labimg.shape,self.labimg)
        print("L:",self.L)
        print("a:",self.a)
        print("b:", self.b)

    def saveLabImgs(self,_save_path):
        pathL = os.path.join(_save_path, self.img_name_.split(".")[0] + "_l"  + ".jpg")
        patha = os.path.join(_save_path, self.img_name_.split(".")[0] + "_a"  + ".jpg")
        pathb = os.path.join(_save_path, self.img_name_.split(".")[0] + "_b" + ".jpg")
        cv2.imwrite(pathL, self.L)
        cv2.imwrite(patha, self.a)
        cv2.imwrite(pathb, self.b)

if __name__ == '__main__':
    PATH = "data/LabImage/1.jpg"
    obj = Rgb2lab(PATH)
    obj.saveLabImgs("data/LabImage")

