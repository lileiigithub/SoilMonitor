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
    def __init__(self,_img_path):
        self.img_path = _img_path
        self.img_arr = cv2.imread(_img_path)
        self.img_shape = self.img_arr.shape
        self.img_width = self.img_shape[0]
        self.img_length = self.img_shape[1]
        self.labels = []
        self.n_clusters_ = 0
        self.labimg = cv2.cvtColor(self.img_arr, cv2.COLOR_BGR2LAB)

    def dbscan_claster(self,model = 0,_EPS = 4):
        # input: lab or rgb cluster; the EPS
        # output: the mean of cluster
        # mod==0:lab , 1:Rgb
        # print(self.img_arr)
        print()
        print(self.img_path,":")
        # print(self.img_length,self.img_width)
        mean = []
        amount_clusting = []
        if(model == 1): # choose rgb
            X = self.img_arr.reshape(-1,3)
        else:  #  # choose lab
            X = self.labimg.reshape(-1,3)
        EPS = _EPS
        MINPTS = self.img_width*self.img_length/10
        db = DBSCAN(eps=EPS, min_samples=MINPTS).fit(X)
        # core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
        # core_samples_mask[db.core_sample_indices_] = True
        self.labels = db.labels_
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
        return mean_of_cluster

    def dbscan_claster_ab(self):
        ab = self.labimg[:,:,1:3]
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
            img_arr_3d_flatten = self.img_arr.reshape(-1, 3)  # (r,g,b)
            img_arr_3d_flatten[self.labels != i] = [225]
            processed_arr_3d = img_arr_3d_flatten.reshape(self.img_arr.shape)
            path = os.path.join(_save_path,self.img_path.split(".")[0]+"_c"+str(i)+".png")
            cv2.imwrite(path, processed_arr_3d)


if __name__ == '__main__':
    import sys
    # img_path = sys.argv[1] #"data/180524_172941.jpg"
    img_path = "dbscan_test.png"
    # PATH = "1006-340.png"
    db = Dbscan_segmention(img_path)
    # db.dbscan_claster_lab()
    db.dbscan_claster(1,5)
    db.save_segmented_imgs("tmpImg")
    time2 = time.time()
    print('time:', time2 - time1)

