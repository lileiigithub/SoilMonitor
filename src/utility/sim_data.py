# -*- coding: utf-8 -*-
'''
data visualization
'''
import numpy as np
import matplotlib.pyplot as plt

range_hum = [0.1,18.51]
range_hum = np.linspace(0.1,18.51,32)
range_L = np.linspace(140.66,57.22,32)
range_a = np.linspace(124.34,132.73,32)
range_b = np.linspace(150.71,131.28,32)

hum = range_hum+np.random.rand(32)
L = range_L+np.random.rand(32)*3
a = range_a+np.random.rand(32)*1
b = range_b+np.random.rand(32)*1.5

# print(hum.shape)
with open("sim_data.txt","w") as file:
    for i in range(len(L)):
        file.writelines(str(round(hum[i],2))+","+str(round(L[i],2))+","+str(round(a[i],2))+","+str(round(b[i],2))+"\n")
plt.plot(hum, L, "*-")
plt.plot(hum, a, "*-")
plt.plot(hum, b, "*-")

plt.legend(["L值", 'a 值', 'b 值'])  # 图例
plt.xlabel("岩土湿度(%)")
plt.ylabel("数值")
plt.show()