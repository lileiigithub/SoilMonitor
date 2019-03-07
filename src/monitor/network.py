# -*- coding: utf-8 -*-
#############################################################################
## 网络类,接收网络数据,即接收图片数组,其实为cv2传来的 nuppy.array / bgr array
## 将收到的 array 数据放在类属性 raw_img_arr 里,
#############################################################################
import cv2
import struct
import numpy as np
from datetime import datetime
import socket
import time
import threading
import os

class Network(object):
    # 类属性
    ImgName = ""
    raw_img_arr = 0

    def __init__(self):
        self.address = (("127.0.0.1",8080)) # 默认地址
        self.savePath = "data/receive" # 存储图片的路径

    def set_address(self,_address):
        self.address = _address

    def create_connnect(self,_address):
        # 创建连接
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
        s.connect(_address)
        self.socketObj = s
        print("创建连接,地址为：",self.address)

    def send_a_message(self):
        try:
            self.socketObj.send(b"ok")
            print("发送成功！")
        except Exception as e:
            print("出现异常,即将关闭连接：",e)
            self.close_connection()

    def receice_a_message(self):
        # 连接网络
        s = self.socketObj
        try:
            bin_stream = s.recv(4)
            stream_len = int.from_bytes(bin_stream,byteorder='big')
            print("接收字节数: ",stream_len)
            bin_stream=b''
            while len(bin_stream) != stream_len:
                bin_stream += s.recv(2048)
            # 解析二进制流
            w = np.frombuffer(bin_stream, dtype=np.uint32, count=1, offset=0)[0]
            h = np.frombuffer(bin_stream, dtype=np.uint32, count=1, offset=4)[0]
            img_arr = np.frombuffer(bin_stream, dtype=np.uint8, count=w*h*3, offset=8)
            img_arr.resize(w,h,3)
            Network.raw_img_arr = img_arr
            # img_name = datetime.now().date().strftime("%y%m%d")+datetime.now().time().strftime("_%H%M%S")+".jpg"
            # img_path = os.path.join(self.savePath,img_name)
            # cv2.imwrite(img_path,img_arr)
            # Network.ImgName = img_path
            print("接收图片大小: ",img_arr.shape)
            print("接收图片时间: ",str(datetime.now()))
        except Exception:
            print("出现异常,即将关闭连接：",Exception)
            self.close_connection()

    def close_connection(self):
        self.socketObj.close()

    # def connection(self):
    #     # 开启多线程接接收数据
    #     try:
    #         t1 = threading.Thread(target=self.__connect_to_internet,args=(self.address,))
    #         t1.start()
    #     except Exception as e:
    #         print("连接错误,错误原因:\n",e)

if __name__ == '__main__':
    net = Network()
    # net.connection()
    net.create_connnect(net.address)
    net.send_a_message()
    net.receice_a_message()
    time.sleep(2)
    net.send_a_message()
    net.receice_a_message()
    net.close_connection()
