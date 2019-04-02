import matplotlib.pyplot as plt
import numpy as np
import cv2
# lab_arr = np.array([[[139,124,149]]])
# # rgb_arr = cv2.cvtColor(lab_arr, cv2.COLOR_LAB2RGB)
# gray = cv2.cvtColor(lab_arr, cv2.COLOR_RGB2GRAY)
# print(gray)
def RGB2L(_r,_g,_b):
    Y = 0.212671*_r+0.715160*_g+0.072169*_b

    # Y = Y/100.0
    print("Y:", Y)
    if Y>0.008856:
        L = 116*(Y**(1/3))
    else:
        L = 903.3*Y
    return L*255/719

def RGB2gray(_r,_g,_b):
    return 0.299*_r+0.587*_g+0.114*_b

def rgb2lab(inputColor):
    num = 0
    RGB = [0, 0, 0]

    for value in inputColor:
        value = float(value) / 255

        if value > 0.04045:
            value = ((value + 0.055) / 1.055) ** 2.4
        else:
            value = value / 12.92

        RGB[num] = value * 100
        num = num + 1

    XYZ = [0, 0, 0, ]

    X = RGB[0] * 0.4124 + RGB[1] * 0.3576 + RGB[2] * 0.1805
    Y = RGB[0] * 0.2126 + RGB[1] * 0.7152 + RGB[2] * 0.0722
    Z = RGB[0] * 0.0193 + RGB[1] * 0.1192 + RGB[2] * 0.9505
    XYZ[0] = round(X, 4)
    XYZ[1] = round(Y, 4)
    XYZ[2] = round(Z, 4)

    # Observer= 2°, Illuminant= D65
    XYZ[0] = float(XYZ[0]) / 95.047         # ref_X =  95.047
    XYZ[1] = float(XYZ[1]) / 100.0          # ref_Y = 100.000
    XYZ[2] = float(XYZ[2]) / 108.883        # ref_Z = 108.883

    num = 0
    for value in XYZ:
        if value > 0.008856:
            value = value ** (0.3333333333333333)
        else:
            value = (7.787 * value) + (16 / 116)
        XYZ[num] = value
        num = num + 1
    Lab = [0, 0, 0]
    L = (116 * XYZ[1]) - 16
    a = 500 * (XYZ[0] - XYZ[1])
    b = 200 * (XYZ[1] - XYZ[2])
    Lab[0] = round(L, 4)
    Lab[1] = round(a, 4)
    Lab[2] = round(b, 4)
    return Lab

def visual_data(_rgb_list):
    L = []
    gray = []
    for rgb in _rgb_list:
        # L.append(RGB2L(rgb[0],rgb[1],rgb[2]))
        l_ = rgb2lab(rgb)[0]
        L.append(l_*255/100)
    for rgb in _rgb_list:
        gray.append(RGB2gray(rgb[0],rgb[1],rgb[2]))
    print("L",L)
    print("gray:",gray)
    plt.plot(L,"o-")
    plt.plot(gray, "o-")
    plt.legend(['L','gray'])  # 图例
    # plt.xlabel("岩土湿度(%)")
    # plt.ylabel("数值")
    # plt.savefig(r"data\paper\lab_hum.png", dpi=250)
    plt.show()

arr = np.random.randint(0,255,(50,3))
arr = arr.tolist()
print(arr)
# arr = [[0,0,0],[255,255,255]]
visual_data(arr)

