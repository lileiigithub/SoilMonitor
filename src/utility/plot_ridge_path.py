"""
===========================================================
Plot Ridge coefficients as a function of the regularization
===========================================================

Shows the effect of collinearity in the coefficients of an estimator.

.. currentmodule:: sklearn.linear_model

:class:`Ridge` Regression is the estimator used in this example.
Each color represents a different feature of the
coefficient vector, and this is displayed as a function of the
regularization parameter.

This example also shows the usefulness of applying Ridge regression
to highly ill-conditioned matrices. For such matrices, a slight
change in the target variable can cause huge variances in the
calculated weights. In such cases, it is useful to set a certain
regularization (alpha) to reduce this variation (noise).

When alpha is very large, the regularization effect dominates the
squared loss function and the coefficients tend to zero.
At the end of the path, as alpha tends toward zero
and the solution tends towards the ordinary least squares, coefficients
exhibit big oscillations. In practise it is necessary to tune alpha
in such a way that a balance is maintained between both.
"""

# Author: Fabian Pedregosa -- <fabian.pedregosa@inria.fr>
# License: BSD 3 clause

print(__doc__)

import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei'] #指定默认字体   
mpl.rcParams['axes.unicode_minus'] = False #解决保存图像是负号'-'显示为方块的问题
# X is the 10x10 Hilbert matrix
X = 1. / (np.arange(1, 4) + np.arange(0, 3)[:, np.newaxis])
print(X)
y = np.ones(3)
# assert 0
# PATH = "updata/weight_lab.csv"
# Line = []
# X = []
# y = []
# with  open(PATH) as file:
#     for line in file.readlines():
#         if line == "\n" or line == "" or line.count("#") >= 1:
#             pass
#         else:
#             Line.append(line)
# for item in Line:
#     item = item.strip()
#     weight = float(item.split(",")[0])
#     L = float(item.split(",")[1])
#     a = float(item.split(",")[2])
#     b = float(item.split(",")[3])
#
#     x = [L, a, b]
#     _y = (weight - 856) / 616  # 实验一含水量计算公式
#     _y = _y * 100
#     # x = (x - 1438) / 1198  # 实验二 含水量计算公式
#     X.append(x)
#     y.append(_y)

# #############################################################################
# Compute paths

n_alphas = 200
alphas = np.logspace(-10, -1, n_alphas)

coefs = []
for a in alphas:
    ridge = linear_model.Ridge(alpha=a, fit_intercept=False)
    ridge.fit(X, y)
    coefs.append(ridge.coef_)

# #############################################################################
# Display results

ax = plt.gca()

ax.plot(alphas, coefs)
ax.set_xscale('log')
ax.set_xlim(ax.get_xlim()[::-1])  # reverse axis
plt.xlabel('alpha')
plt.ylabel('权值')
plt.legend(["L值","a值","b值"])
# plt.title('Ridge coefficients as a function of the regularization')
plt.axis('tight')

plt.savefig(r"data\save\ridge.png", dpi=320)
plt.show()