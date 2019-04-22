# -*- coding: utf-8 -*-
#############################################################################
## 网络类,接收网络数据,即接收图片数组,其实为cv2传来的 nuppy.array / bgr array
## 将收到的 array 数据放在类属性 raw_img_arr 里,
#############################################################################
import numpy as np
from datetime import datetime
import socket
import time
from globalData import Data
from soilMonitorLog import SMLog

class Network(object):
    # 类属性
    ImgName = ""
    raw_img_arr = 0

    def __init__(self):
        self.address = (("127.0.0.1",8080)) # 默认地址

    def set_address(self,_address):
        self.address = _address

    def create_connnect(self,_address):
        # 创建连接
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
        s.connect(_address)
        self.socketObj = s
        SMLog.debug("创建连接成功!")

    def send_a_message(self):
        try:
            self.socketObj.send(b"ok")
            SMLog.debug("发送 ok 成功!")
        except Exception as e:
            SMLog.error("出现异常,即将关闭连接：",e)
            self.close_connection()

    def receice_a_message(self):
        # 连接网络
        s = self.socketObj
        try:
            bin_stream = s.recv(4)
            stream_len = int.from_bytes(bin_stream,byteorder='big')
            SMLog.info("接收字节数: %s",stream_len)
            bin_stream=b''
            while len(bin_stream) != stream_len:
                bin_stream += s.recv(2048)
            # 解析二进制流
            w = np.frombuffer(bin_stream, dtype=np.uint32, count=1, offset=0)[0]
            h = np.frombuffer(bin_stream, dtype=np.uint32, count=1, offset=4)[0]
            img_arr = np.frombuffer(bin_stream, dtype=np.uint8, count=w*h*3, offset=8)
            img_arr.resize(w,h,3)
            Data.raw_img_arr = img_arr
            SMLog.info("接收图片大小: %s",img_arr.shape)
            SMLog.info("接收图片时间: %s",str(datetime.now()))
        except Exception:
            SMLog.error("出现异常,即将关闭连接：%s",Exception)
            self.close_connection()

    def close_connection(self):
        self.socketObj.close()

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
