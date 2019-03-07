# -*- coding: utf-8 -*-

import numpy as np

# a = np.array([1.0,2.2220,3.3322232])
#
# _list = [["abc",a.tolist()],["ac",a.tolist()]]
# with open("temp.txt","w") as file:
#     for item in _list:
#         s = "{:.2f} {:.2f} {:.2f}  {}\n".format(item[1][0],item[1][1],item[1][2],item[0])
#         file.writelines(s)


def fun():
    data = np.array([[64.08152365,76.75372223, 94.59553887]
                     ,[69.60514858,81.74918722,95.66822552]
                     ,[76.41495419,87.85854913,101.99691074]
                     ,[80.38801348,95.45640507,110.73533877]
                     ,[81.63248319,95.99268262,113.06713954]
                     ,[95.7815344,115.85959532,126.3773868]])
    lux = [340,345,380,390,420,480]

    for i in range(6):
        print(data[i]/lux[i])
        # print(data/lux)

fun()
