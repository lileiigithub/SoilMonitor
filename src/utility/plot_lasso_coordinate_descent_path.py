"""
=====================
Lasso and Elastic Net
=====================

Lasso and elastic net (L1 and L2 penalisation) implemented using a
coordinate descent.

The coefficients can be forced to be positive.
"""
print(__doc__)

# Author: Alexandre Gramfort <alexandre.gramfort@inria.fr>
# License: BSD 3 clause

from itertools import cycle
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import lasso_path, enet_path
from sklearn import datasets
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei'] #指定默认字体   
mpl.rcParams['axes.unicode_minus'] = False #解决保存图像是负号'-'显示为方块的问题
# diabetes = datasets.load_diabetes()
# X = diabetes.data
# y = diabetes.target

# X /= X.std(axis=0)  # Standardize data (easier to set the l1_ratio parameter)
PATH = "updata/weight_lab.csv"
Line = []
X = []
Y = []
with  open(PATH) as file:
    for line in file.readlines():
        if line == "\n" or line == "" or line.count("#") >= 1:
            pass
        else:
            Line.append(line)
for item in Line:
    item = item.strip()
    weight = float(item.split(",")[0])
    L = float(item.split(",")[1])
    a = float(item.split(",")[2])
    b = float(item.split(",")[3])

    x = [L, a, b]
    y = (weight - 856) / 616  # 实验一含水量计算公式
    y = y * 100
    # x = (x - 1438) / 1198  # 实验二 含水量计算公式
    X.append(x)
    Y.append(y)

# Compute paths

eps = 5e-3  # the smaller it is the longer is the path

print("Computing regularization path using the lasso...")
alphas_lasso, coefs_lasso, _ = lasso_path(X, Y, eps, fit_intercept=False)


print("Computing regularization path using the elastic net...")
alphas_enet, coefs_enet, _ = enet_path(
    X, Y, eps=eps, l1_ratio=0.8, fit_intercept=False)

# Display results

plt.figure(1)
colors = cycle(['b', 'r', 'g', 'c', 'k'])
neg_log_alphas_lasso = -np.log10(alphas_lasso)
neg_log_alphas_enet = -np.log10(alphas_enet)

for coef_l, coef_e, c in zip(coefs_lasso, coefs_enet, colors):
    print(len(neg_log_alphas_lasso), len(coef_l))
    print(neg_log_alphas_lasso,coef_l)
    l1 = plt.plot(neg_log_alphas_lasso, coef_l, c=c)
    l2 = plt.plot(neg_log_alphas_enet, coef_e, linestyle='--', c=c)

plt.xlabel('-Log(alpha)')
plt.ylabel('权值')
# plt.title('Lasso and Elastic-Net Paths')
plt.legend((l1[-1], l2[-1]), ('Lasso', 'Elastic-Net'), loc='lower left')
plt.axis('tight')
plt.savefig(r"data\save\elastic_lasso.png", dpi=320)
plt.show()
