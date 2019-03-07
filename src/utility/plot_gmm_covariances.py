"""
===============
GMM covariances
===============

Demonstration of several covariances types for Gaussian mixture models.

See :ref:`gmm` for more information on the estimator.

Although GMM are often used for clustering, we can compare the obtained
clusters with the actual classes from the dataset. We initialize the means
of the Gaussians with the means of the classes from the training set to make
this comparison valid.

We plot predicted labels on both training and held out test data using a
variety of GMM covariance types on the iris dataset.
We compare GMMs with spherical, diagonal, full, and tied covariance
matrices in increasing order of performance. Although one would
expect full covariance to perform best in general, it is prone to
overfitting on small datasets and does not generalize well to held out
test data.

On the plots, train data is shown as dots, while test data is shown as
crosses. The iris dataset is four-dimensional. Only the first two
dimensions are shown here, and thus some points are separated in other
dimensions.
"""

# Author: Ron Weiss <ronweiss@gmail.com>, Gael Varoquaux
# Modified by Thierry Guillemot <thierry.guillemot.work@gmail.com>
# License: BSD 3 clause

import matplotlib as mpl
import matplotlib.pyplot as plt

import numpy as np

from sklearn import datasets
from sklearn.mixture import GaussianMixture
from sklearn.model_selection import StratifiedKFold

# print(__doc__)

iris = datasets.load_iris()

# Break up the dataset into non-overlapping training (75%) and testing
# (25%) sets.
skf = StratifiedKFold(n_splits=4)
# Only take the first fold.
train_index, test_index = next(iter(skf.split(iris.data, iris.target)))

X_train = iris.data[train_index]
y_train = iris.target[train_index]
X_test = iris.data[test_index]
y_test = iris.target[test_index]

print("X_train shape:",X_train.shape)
print("X_test shape:",X_test.shape)

# 训练
# 训练可以使用无监督或有监督
n_classes = 3
clf = GaussianMixture(n_components=n_classes, covariance_type='full',random_state=0,max_iter=20)
clf.means_init = np.array([X_train[y_train == i].mean(axis=0)for i in range(n_classes)]) # 使用标签初始化
clf.fit(X_test)
print("model means:",clf.means_)
print("model weights:",clf.weights_)
# 预测
#预测trian
y_predict = clf.predict(X_train)
print("train:",np.mean(y_predict.ravel()==y_train.ravel()))
#预测test
y_predict = clf.predict(X_test)
print("test:",np.mean(y_predict.ravel()==y_test.ravel()))

