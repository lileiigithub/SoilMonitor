# -*- coding: utf-8 -*-

import numpy as np
import collections
import cv2


def fun():
    img_arr = cv2.imread("data/test/people.jpg")
    rec_p = (450,350) #  截图顶点
    subimg = img_arr[rec_p[1]:rec_p[1]+100, rec_p[0]:rec_p[0]+100, :]
    cv2.rectangle(img_arr, rec_p, (rec_p[0]+100,rec_p[1]+100), (0, 0, 255))
    cv2.imwrite("data/test/people_rectangle.jpg", img_arr)
    cv2.imwrite("data/test/people_roi.jpg", subimg)


def creat_csv():
    path1 = r"data/-3expo.txt"
    path2 = ""
    values=  []
    with  open(path1) as file:
        for line in file.readlines():
            if line == "\n" or line == "" or line.count("#") >= 1:
                pass
            else:
                weight = line.split(":")[0]
                Labline = line.split("[")[1].split("]")[0]
                print(Labline)
                Labline1 = []
                for item in Labline:
                    if item != '':
                        Labline1.append(item)
                # print(Labline1)
                L = Labline1[0]
                a = Labline1[1]
                b = Labline1[2]
                values.append([weight,L,a,b])
    print(values)
    # with open(path2,'w') as file:

if __name__ == '__main__':
    creat_csv()
