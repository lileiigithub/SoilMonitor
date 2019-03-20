# -*- coding: utf-8 -*-

class Data(object):
    # 各个全局参数,以及流动的数据
    # 类属性
    address = ("127.0.0.1",8080) # socket address
    algorithm_used_time = 0  # the used time of algorithm
    isOnline = False  # 是否为在线检测
    img_name = None
    #  可视化的array
    raw_img_arr = None  # raw image array
    filtered_img_arr = None  # processed image array
    segmented_img_arr = None # segmented image array
    clustered_img_arr = None  # gray histogram image array

    #  存储图片的folder
    raw_img_folder = "data/raw/"
    filtered_img_folder = "data/filtered/"
    segmented_img_folder = "data/segmented/"
    clustered_img_folder = "data/clustered/"

    # the predict about
    model_path = "model/ridge.model"
    predicted_classification = -1

    # 中间以及最后结果
    soil_mean = None
    predict_result = None


