# -*- coding: utf-8 -*-
#############################################################################
#
#############################################################################

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QCheckBox, QDialog,
        QDialogButtonBox, QGridLayout, QHBoxLayout, QLabel, QLayout, QLineEdit,
        QPushButton, QVBoxLayout, QWidget)
from globaldata import Data

class DenoiseDialog(QDialog):
    def __init__(self, parent=None):
        super(DenoiseDialog, self).__init__(parent)

        filter_layout = QVBoxLayout()
        self.filter1 = QCheckBox("均值滤波")
        self.filter2 = QCheckBox("中值滤波")
        self.filter3 = QCheckBox("高斯低通滤波")

        filter_layout.addWidget(self.filter1)
        filter_layout.addWidget(self.filter2)
        filter_layout.addWidget(self.filter3)
        filter_layout.setAlignment(Qt.AlignCenter)
        self.YesButton = QPushButton("确定")
        self.NoButton = QPushButton("取消")
        YN_layout = QHBoxLayout()
        YN_layout.addWidget(self.YesButton)
        YN_layout.addWidget(self.NoButton)

        # 主布局
        mainLayout = QVBoxLayout()
        # mainLayout.setSizeConstraint(QLayout.SetFixedSize)
        mainLayout.addLayout(filter_layout)
        mainLayout.addLayout(YN_layout)

        # mainLayout.setRowStretch(2, 1)
        self.setLayout(mainLayout)
        self.setWindowTitle("滤波设置")
        self.resize(250,200)
        self.NoButton.clicked.connect(self.cancel)
        self.YesButton.clicked.connect(self.ok) # 连接信号与槽

    def ok(self):
        ip = self.ip_lineEdit.text()
        port = self.port_lineEdit.text()
        if port!="" and ip !="":
            Data.address = (ip,int(port))
            print("设置滤波算法：",Data.address)
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
