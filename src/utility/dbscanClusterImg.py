# -*- coding: utf-8 -*-
'''
use dbscan algorithm to segment img of soil;
'''
import cv2
from sklearn.cluster import DBSCAN
from sklearn import metrics
import numpy as np
import os
import time
time1 = time.time()

class Dbscan_segmention(object):
    def __init__(self,_img_bgr_arr):
        self.gbr_arr = _img_bgr_arr
        self.img_shape = self.gbr_arr.shape
        self.img_width = self.img_shape[0]
        self.img_length = self.img_shape[1]
        self.labels = []
        self.n_clusters_ = 0
        self.lab_arr = cv2.cvtColor(self.gbr_arr, cv2.COLOR_BGR2LAB)

    def dbscan_cluster(self,_arr,_EPS = 4):
        # input: lab or rgb cluster; the EPS
        # output: the mean of cluster

        mean = []
        amount_clusting = []
        X = _arr.reshape(-1,3)  # 将数据拉平为 3维
        EPS = _EPS
        MINPTS = self.img_width*self.img_length/10  #  MinPts半径设为 w*h # /10

        db = DBSCAN(eps=EPS, min_samples=MINPTS).fit(X)
        # core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        # core_samples_mask[db.core_sample_indices_] = True
        self.labels = db.labels_

        print(self.labels)
        self.n_clusters_ = len(set(self.labels)) - (1 if -1 in self.labels else 0)
        # print("labels:",self.labels)
        # print("n_clusters:",self.n_clusters_)
        for i in range(self.n_clusters_):
            amount_clusting.append(len(self.labels[self.labels[:] == i]))
            mean_of_cluster = [np.mean(X[self.labels == i][:, 0]), np.mean(X[self.labels == i][:, 1]), np.mean(X[self.labels == i][:, 2])]
            mean.append(mean_of_cluster)
            print(i, ":","mean: ","[",round(mean_of_cluster[0],2),round(mean_of_cluster[1],2),round(mean_of_cluster[2],2),"]")
            # print(i,":",mean)
        ratio = len(self.labels[self.labels[:] == -1]) / len(self.labels)
        print("noise ratio: ", ratio)
        return mean_of_cluster  # 返回了最后一个聚类中心点，后期需要改为返回最大的类的中心点

    def dbscan_claster_ab(self):
        # 将ab值聚类
        ab = self.lab_arr[:,:,1:3]
        print("ab:", ab)
        mean = []
        amount_clusting = []
        X = ab.reshape(-1, 2)
        EPS = 4
        MINPTS = self.img_width * self.img_length / 10
        db = DBSCAN(eps=EPS, min_samples=MINPTS).fit(X)
        # core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        # core_samples_mask[db.core_sample_indices_] = True
        self.labels = db.labels_
        self.n_clusters_ = len(set(self.labels)) - (1 if -1 in self.labels else 0)
        print(self.labels)
        print(self.n_clusters_)
        for i in range(self.n_clusters_):
            print(i, ":")
            amount_clusting.append(len(self.labels[self.labels[:] == i]))
            mean_of_cluster = [np.mean(X[self.labels == i][:, 0]), np.mean(X[self.labels == i][:, 1])]
            mean.append(mean_of_cluster)
            print("mean: ", "[", round(mean_of_cluster[0], 2), round(mean_of_cluster[1], 2), "]")
        ratio = len(self.labels[self.labels[:] == -1]) / len(self.labels)
        print("noise ratio: ", ratio)

    def save_segmented_imgs(self,_save_path):
        for i in range(self.n_clusters_):
            gbr_arr_flatten = self.gbr_arr.reshape(-1, 3)  # (r,g,b)
            gbr_arr_flatten[self.labels != i] = [255]
            clustered_arr_3d = gbr_arr_flatten.reshape(self.gbr_arr.shape)
            cv2.imwrite(_save_path, clustered_arr_3d)


if __name__ == '__main__':
    import sys
    # img_path = sys.argv[1] #"data/180524_172941.jpg"
    img_path = "data/dbscan_test_1.png"
    # PATH = "1006-340.png"
    img_arr = cv2.imread(img_path)
    db = Dbscan_segmention(img_arr)
    # db.dbscan_claster_lab()
    db.dbscan_cluster(db.lab_arr, 5)
    save_path = "data/cluster/dbscan_test_c.png"
    db.save_segmented_imgs(save_path)
    time2 = time.time()
    print('time:', time2 - time1)

