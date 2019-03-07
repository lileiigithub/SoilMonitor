# -*- coding: UTF-8
'''
将大尺寸的图片变为小尺寸(800*600)
'''

import cv2
from datetime import datetime
def zoomImage(_src_img,_dst_img):
    # 缩小一副图片
    # 输入: 图片名 ; 存储缩小后的图片
    img = cv2.imread(_src_img)
    tempimg = cv2.resize(img,(800,600),cv2.INTER_LINEAR)
    cv2.imwrite(_dst_img,tempimg)


if __name__ == '__main__':
    src_img = "20180403_181430.jpg"
    dst_img = datetime.now().date().strftime("%y%m%d")+datetime.now().time().strftime("_%H%M%S")+".jpg"
    zoomImage(src_img ,dst_img)
