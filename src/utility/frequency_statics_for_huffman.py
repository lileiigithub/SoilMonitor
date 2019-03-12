# -*- coding: utf-8 -*-
'''
用于论文：绘制图像个字符的统计直方图
再使用huffman编码压缩
'''
import cv2
import numpy as np
from numpy import random
import matplotlib.pyplot as plt
import time
time1 = time.time()
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei'] #指定默认字体   
mpl.rcParams['axes.unicode_minus'] = False #解决保存图像是负号'-'显示为方块的问题

from HuffmanCoding import huffman_encode,huffman_store

def frency_statics(_img_arr):
    # 画统计图
    arr_flatten = _img_arr.flatten()
    plt.ylabel("频数")
    plt.xlabel("像素点值")
    plt.hist(arr_flatten,255)
    # plt.title("直方图")
    plt.savefig("data/freqStatics/1p.1.jpg", frameon=True, dpi=150)  # , dpi=200
    # plt.show()


if __name__ == '__main__':
    img_src = "data/freqStatics/1p.jpg"
    img_arr = cv2.imread(img_src)
    img_arr = img_arr.flatten()
    frency_statics(img_arr)
    # huffman_info = huffman_encode(img_arr)
    # path = 'test'
    # f = open(path, 'wb')
    # huffman_store(f, huffman_info)
    # f.close()

    # f1 = open(path, 'rb')
    # huffman_info_ = huffman_restore(f1)
    # # original_arr = huffman_decode(huffman_info_)
    # # print(original_arr)
    # f1.close()