# -*- coding: UTF-8
'''

'''
import cv2
import numpy as np
from matplotlib import pyplot as plt
import time

class PreprocessImg(object):
    def __init__(self,_img_arr):
        self.__start_time = time.time()
        self.img_arr = _img_arr
        self.labimg = cv2.cvtColor(self.img_arr,cv2.COLOR_BGR2LAB)

    def __average_gray_and_bebong_rgb(self):
        # bgr -> lab -> bgr -> gray
        #LAB空间变换，处理明度
        # rgbimage = cv2.imread(_fileName)
        labimage = self.labimg
        labimage[:, :, 0] = labimage[:, :, 0]//3  # 亮度降低为原来1/3
        image = cv2.cvtColor(labimage,cv2.COLOR_LAB2BGR)
        # cv2.imwrite(savepath,image)
        #转灰度
        # cv2.imwrite("ltest1.jpg",image)
        img = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
        # 阈值
        _, img = cv2.threshold(img, 65, 0, cv2.THRESH_TOZERO_INV)  # 大于阈值取0
        # img = cv2.imread(fileName, 0)
        #区密集区间，计算平均值
        print(img)
        self.thresh_gray_img = img
        # plt.show()
        originHist = cv2.calcHist([img],[0],None,[256],[0,256])
        print(originHist)
        originHist[0] = 0
        pos_max = np.where(originHist == np.max(originHist))
        position = pos_max[0][0]
        sum = 0
        count = 0
        average = 0
        for i in range(position-5,position+5):
            sum += originHist[i]*i
            count += originHist[i]
        average = sum / count
        print("position: ",position)
        return average,self.__find_rgb_in_gray(img,position-3,position+3)

    def __find_rgb_in_gray(self,_grayImg,_grayMin,_grayMax):
        # Gray = R*0.299 + G*0.587 + B*0.114
        # ipput:
        #  _rgbImg:rgb array
        # _grayImg:gray array
        # _grayMin～_grayMax: 灰度值采样范围
        index_list = [] # 装载被采样点的序号
        rgbImage = self.img_arr.reshape(-1,3) #将rgb图片数组拉平
        grayImg = _grayImg.reshape(-1,1) #将灰度图片数组拉平

        for index in range(len(grayImg)):
            # 选择符合条件的灰度值
            if grayImg[index]>_grayMin and grayImg[index]<_grayMax:
                index_list.append(index)

        _rgb_array = rgbImage[index_list]
        SAMPLING_NUMS = 300  # 采样数量
        if len(_rgb_array)>SAMPLING_NUMS:
            print("sampling..")
            # 使用np.random.choice函数采样,random_index为采样点的序号组成的列表
            random_index = np.random.choice(len(_rgb_array),SAMPLING_NUMS,replace=False)
        return _rgb_array[random_index]


    def save_hist_img(self,_path = "temp/grayhostigram.png"):
        img = self.thresh_gray_img
        plt.hist(img.ravel(), 256, [0, 256])
        plt.savefig(_path, dpi=800)

    @property
    def used_time(self):
        # 计算耗时
        return round(time.time()-self.__start_time,2)

    def get_X(self):
        X = []
        ave,rgb_array = self.__average_gray_and_bebong_rgb()
        if len(X) == 0:
            X = rgb_array.tolist()
        else:
            X += rgb_array.tolist()

        return np.array(X)


if __name__ == '__main__':
    img_path = "data/180529_202903_180524_172941.jpg"
    img_array = cv2.imread(img_path)

    pre = PreprocessImg(img_array)
    X = pre.get_X()
    # pre.save_hist_img()
    print("使用时间: ",pre.used_time)
    # print(len(X))
    print(X)

    # ave,rgb_array = average_gray_and_bebong_rgb("data/image/0.jpg")
    # print(ave,rgb_array.shape)



