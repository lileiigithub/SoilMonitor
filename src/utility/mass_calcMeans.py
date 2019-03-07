# -*- coding: utf-8 -*-
import cv2
import sys
import os
import time
time1 = time.time()
# from dbscanClusterImg import Dbscan_segmention

if __name__ == '__main__':
    # DIR_PATH = r"E:\UbuntuData\camera\bake"
    DIR_PATH = r"E:\UbuntuData\camera\-3expo-rgb"
    dir_list = os.listdir(DIR_PATH)
    command_dir_list = []
    for dir in dir_list:
        absolute_path = os.path.join(DIR_PATH,dir)
        if os.path.isdir(absolute_path) == True:
            command_dir_list.append(absolute_path)

    # excute the command
    for abDir in command_dir_list:
        destFile =abDir+".txt"
        commamnd = " python .\cut_CalcMeans.py "+abDir+" > "+ destFile
        print("执行命令：",commamnd)
        os.system(commamnd)
        print("now used time:",round(time.time()-time1,2))
