#!/usr/bin/env python3

import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
def qt_message_handler(mode, context, message):
    if mode == QtInfoMsg:
        mode = 'INFO'
    elif mode == QtWarningMsg:
        mode = 'WARNING'
    elif mode == QtCriticalMsg:
        mode = 'CRITICAL'
    elif mode == QtFatalMsg:
        mode = 'FATAL'
    else:
        mode = 'DEBUG'
    print('qt_message_handler: line: %d, func: %s(), file: %s' % (
        context.line, context.function, context.file))
    print('  %s: %s\n' % (mode, message))

qInstallMessageHandler(qt_message_handler)




class Model(QObject):
    own_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.lbnum = 0

    def setView(self, view):
        self.view = view
        self.view.updateContent()


    def increase(self):
        self.lbnum+=1

    def decrease(self):
        self.lbnum-=1


class Label(QtWidgets.QLabel):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.model = None

    def setModel(self, model):
        self.model = model
        self.model.setView(self)

    def updateContent(self):
        self.setNum(self.model.lbnum)

class Widget(QtWidgets.QFrame):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.resize(500, 500)
        self.model = Model()
        self.model.own_signal.connect(self.upd)
        self.box = QtWidgets.QVBoxLayout(self)
        self.btn = QtWidgets.QPushButton("+")
        self.btn2 = QtWidgets.QPushButton("-")
        self.btn.clicked.connect(self.pressi)
        self.btn2.clicked.connect(self.pressd)
        self.lb = Label()
        self.lb2 = Label()
        self.lb2.setStyleSheet('background: grey;')
        self.lb.setModel(self.model)
        self.lb2.setModel(self.model)
        self.box.addWidget(self.btn)
        self.box.addWidget(self.btn2)
        self.box.addWidget(self.lb)
        self.box.addWidget(self.lb2)

    def upd(self):
        self.lb.updateContent()
        self.lb2.updateContent()


    def pressi(self):
        self.model.increase()
        self.model.own_signal.emit()


    def pressd(self):
        self.model.decrease()
        self.model.own_signal.emit()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet(open('./etc/{0}.qss'.format('style'), "r").read())
    main = Widget()
    main.show()
    sys.exit(app.exec_())