# -*- coding: utf-8 -*-

class Data(object):
    # 各个全局参数,以及流动的数据
    # 类属性

    # socket address
    address = ("127.0.0.1",8080)

    raw_img_path = ""  # raw image path
    raw_img_arr = 0  # raw image array

    processed_img_path = "temp/pro_img.jpg"  # processed image path
    processed_img_arr = 0  # processed image array

    grayhist_img_path = "temp/grayhostigram.png"  # gray histogram image path
    grayhist_img_arr = 0  # gray histogram image array

    # the predicted result of classification
    predicted_classification = -1

    algorithm_used_time = 0  # the used time of algorithm

    isOnline = False  # 是否为在线检测
