# -*- coding: utf-8 -*-
#  main
from PyQt5.QtWidgets import QApplication
from mainwindow import MainWindow

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
