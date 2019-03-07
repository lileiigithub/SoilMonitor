# -*- coding: utf-8 -*-
from PyQt5.QtCore import QObject,pyqtSignal

class A(QObject):

    trigger = pyqtSignal()
    def __init__(self):
        QObject.__init__(self)

    def connect_and_emit_trigger(self):
        # do something
        self.trigger.emit()

    def handle_trigger(self):
        print("A be invoked!")


class B(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.a = A()
        self.a.trigger.connect(self.something)

        # self.connet(self,A.receivedSignal,self.something)
    def invoke(self):
        self.a.connect_and_emit_trigger()

    def something(self):
        print("B be invoked!")


if __name__ == '__main__':
    b = B()
    b.invoke()