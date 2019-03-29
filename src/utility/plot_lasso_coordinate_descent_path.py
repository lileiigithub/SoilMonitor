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
diabetes = datasets.load_diabetes()
X = diabetes.data
Y = diabetes.target

X /= X.std(axis=0)  # Standardize data (easier to set the l1_ratio parameter)

PATH = "updata/sim_data.txt"
arr = np.genfromtxt(PATH, delimiter=",")
Y = arr[:, 0]  # hum
X = arr[:, 1:]  # features
# X /= X.std(axis=0)  # Standardize data (easier to set the l1_ratio parameter)
# Compute paths

eps = 5e-3  # the smaller it is the longer is the path

print("Computing regularization path using the lasso...")
alphas_lasso, coefs_lasso, _ = lasso_path(X, Y, eps, n_alphas = 100, fit_intercept=False)


print("Computing regularization path using the elastic net...")
alphas_enet, coefs_enet, _ = enet_path(
    X, Y, eps=eps, l1_ratio=0.5, fit_intercept=False)

# Display results

plt.figure(1)
colors = cycle(['b', 'r', 'g', 'c', 'k'])
neg_log_alphas_lasso = -np.log10(alphas_lasso)
neg_log_alphas_enet = -np.log10(alphas_enet)

for coef_l, coef_e, c in zip(coefs_lasso, coefs_enet, colors):
    print(len(neg_log_alphas_lasso), len(coef_l))
    print(coef_l)  # neg_log_alphas_lasso
    l1 = plt.plot( coef_l, c=c)  # neg_log_alphas_lasso,
    l2 = plt.plot( coef_e, linestyle='--', c=c) # neg_log_alphas_enet,

plt.xlabel('坐标下降步数') # -Log(alpha)
plt.ylabel('权值')
# plt.title('Lasso and Elastic-Net Paths')
# plt.legend((l1[-1]), ('Lasso')) # , loc='lower left'
plt.legend((l1[-1], l2[-1]), ('Lasso', 'Elastic-Net')) # , loc='lower left'
# plt.axis('tight')
plt.savefig(r"data\paper\elastic_lasso.png", dpi=250)
plt.show()
