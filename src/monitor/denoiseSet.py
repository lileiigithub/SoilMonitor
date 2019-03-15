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

        self.ip_label = QLabel("IP地址:")
        self.ip_lineEdit = QLineEdit()
        ip_layout = QHBoxLayout()
        ip_layout.addWidget(self.ip_label)
        ip_layout.addWidget(self.ip_lineEdit)

        self.port_label = QLabel("端口号:")
        self.port_lineEdit = QLineEdit()
        port_layout = QHBoxLayout()
        port_layout.addWidget(self.port_label)
        port_layout.addWidget(self.port_lineEdit)

        self.YesButton = QPushButton("确定")
        self.NoButton = QPushButton("取消")
        YN_layout = QHBoxLayout()
        YN_layout.addWidget(self.YesButton)
        YN_layout.addWidget(self.NoButton)

        # 主布局
        mainLayout = QVBoxLayout()
        # mainLayout.setSizeConstraint(QLayout.SetFixedSize)
        mainLayout.addLayout(ip_layout)
        mainLayout.addLayout(port_layout)
        mainLayout.addLayout(YN_layout)

        # mainLayout.setRowStretch(2, 1)
        self.setLayout(mainLayout)
        self.setWindowTitle("network setting")
        self.resize(250,200)
        self.NoButton.clicked.connect(self.cancel)
        self.YesButton.clicked.connect(self.ok) # 连接信号与槽

    def ok(self):
        ip = self.ip_lineEdit.text()
        port = self.port_lineEdit.text()
        if port!="" and ip !="":
            Data.address = (ip,int(port))
            print("设置新网络连接：",Data.address)
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
    dialog = NetworkDialog()
    dialog.show()
    sys.exit(app.exec_())
