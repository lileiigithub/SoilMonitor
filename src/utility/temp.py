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

fun()
