#!/usr/bin/env python3

import sys
from PyQt5 import QtWidgets, QtCore

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from gui.custom.drag import *
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
class Top(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('background: grey;')

class Center(DragFrame):
    def __init__(self):
        super().__init__()
        self.box = QHBoxLayout(self)
        self.setStyleSheet('background: grey;')
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        if self.box.count() < 1:
            self.newLabel = DropLabel("WORD", self)
            self.newLabel.setFont(QFont("arial", 40))
            self.newLabel.setAlignment(Qt.AlignCenter)
            self.box.addWidget(self.newLabel)
        e.accept()

    def delLabel(self):
        self.box.removeWidget(self.newLabel)
        self.newLabel.deleteLater()
        self.newLabel = None

class Bottom(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('background: grey;')



class Left(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setStyleSheet('background: grey;')
        self.setFixedSize(200, 500)
        self.dragLabel = DragLabel("word", self)
        self.dragLabel.show()



class Labels(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedSize(500, 500)
        self.box = QtWidgets.QVBoxLayout(self)
        self.box.setSpacing(1)
        self.box.setContentsMargins(1, 1, 1, 1)
        self.t = Top()
        self.c = Center()
        self.b = Bottom()
        self.box.addWidget(self.t)
        self.box.addWidget(self.c)
        self.box.addWidget(self.b)


class Widget(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.box = QtWidgets.QHBoxLayout(self)
        self.box.setSpacing(1)
        self.box.setContentsMargins(1, 1, 1, 1)
        self.left = Left()
        self.box.addWidget(self.left)

        self.labels = Labels()
        self.box.addWidget(self.labels)





if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet(open('./etc/{0}.qss'.format('style'), "r").read())
    main = Widget()
    main.show()
    sys.exit(app.exec_())