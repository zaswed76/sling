#!/usr/bin/env python3
import datetime
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

class Top(DragFrame):
    def __init__(self):
        super().__init__()


class Center(DragFrame):
    def __init__(self):
        super().__init__()





class Bottom(DragFrame):
    def __init__(self):
        super().__init__()




class Left(QtWidgets.QListWidget):
    def __init__(self):
        super().__init__()
        self.setFont(QFont("Arial", 24))
        self.setDragEnabled(True)
        self.setFixedSize(250, 500)
        self.l1 = QListWidgetItem("Word")
        self.l1.setTextAlignment(Qt.AlignCenter)

        self.l2 = QListWidgetItem("Перевод")
        self.l2.setTextAlignment(Qt.AlignCenter)

        self.l3 = QListWidgetItem("Транскрипция")
        self.l3.setTextAlignment(Qt.AlignCenter)

        self.l4 = QListWidgetItem("Пример")
        self.l4.setTextAlignment(Qt.AlignCenter)

        self.insertItem(0, self.l1)
        self.insertItem(1, self.l2)
        self.insertItem(2, self.l3)
        self.insertItem(3, self.l4)


    def mouseMoveEvent(self, e):
        mimeData = QMimeData()
        mimeData.setText(self.currentItem().text)
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        dropAction = drag.exec_(Qt.MoveAction)


class CardView(QtWidgets.QFrame):
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

        self.labels = CardView()
        self.box.addWidget(self.labels)





if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet(open('./etc/{0}.qss'.format('style'), "r").read())
    main = Widget()
    main.show()
    sys.exit(app.exec_())