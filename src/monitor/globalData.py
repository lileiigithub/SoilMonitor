# -*- coding: utf-8 -*-

class Data(object):
    # 各个全局参数,以及流动的数据
    # 类属性

    # socket address
    address = ("127.0.0.1",8080)
    #  array
    raw_img_arr = None  # raw image array
    filtered_img_arr = None  # processed image array
    segmented_img_arr = None # segmented image array
    clustered_img_arr = None  # gray histogram image array
    #  folder
    raw_img_folder = "data/raw/"
    filtered_img_folder = "data/filtered/"
    segmented_img_folder = "data/segmented/"
    clustered_img_folder = "data/clustered/"
    # the predicted result of classification
    predicted_classification = -1

    algorithm_used_time = 0  # the used time of algorithm

    isOnline = False  # 是否为在线检测
