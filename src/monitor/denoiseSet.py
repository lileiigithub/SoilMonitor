# -*- coding: utf-8 -*-
#############################################################################
#
#############################################################################

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QCheckBox, QDialog,
        QDialogButtonBox, QGridLayout, QHBoxLayout, QLabel, QLayout, QLineEdit,
        QPushButton, QVBoxLayout, QWidget)
from PyQt5.QtGui import QKeySequence,QFont,QPixmap,QImage,QRgba64
from globalData import Data

class DenoiseDialog(QDialog):
    def __init__(self, parent=None):
        super(DenoiseDialog, self).__init__(parent)

        filter_layout = QVBoxLayout()
        self.filter1 = QCheckBox("均值滤波")
        self.filter2 = QCheckBox("中值滤波")
        self.filter3 = QCheckBox("高斯低通滤波")
        self.filter2.setChecked(True)
        self.filter1.setFont(QFont("Roman times", 20))
        self.filter2.setFont(QFont("Roman times", 20))
        self.filter3.setFont(QFont("Roman times", 20))
        filter_layout.addWidget(self.filter1)
        filter_layout.addWidget(self.filter2)
        filter_layout.addWidget(self.filter3)
        filter_layout.setAlignment(Qt.AlignCenter)
        filter_layout.setSpacing(40)  #  设置控件间隔
        self.YesButton = QPushButton("确定")
        self.YesButton.setFont(QFont("Roman times", 15))
        self.NoButton = QPushButton("取消")
        self.NoButton.setFont(QFont("Roman times", 15))
        YN_layout = QHBoxLayout()
        YN_layout.addWidget(self.YesButton)
        YN_layout.addWidget(self.NoButton)

        # 主布局
        mainLayout = QVBoxLayout()
        # mainLayout.setSizeConstraint(QLayout.SetFixedSize)
        mainLayout.addLayout(filter_layout)
        mainLayout.addLayout(YN_layout)
        mainLayout.setSpacing(20)  #  设置控件间隔
        # mainLayout.setRowStretch(2, 1)
        self.setLayout(mainLayout)
        self.setWindowTitle("去噪滤波设置")
        self.resize(300,300)  #  设置Dialog大小
        self.NoButton.clicked.connect(self.cancel)
        self.YesButton.clicked.connect(self.ok) # 连接信号与槽

    def ok(self):
        self.close()
        # return self.address

    def cancel(self):
        self.close()

    def get_ip(self):
        return self.ip

    def get_port(self):
        return self.port

if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    dialog = DenoiseDialog()
    dialog.show()
    sys.exit(app.exec_())
