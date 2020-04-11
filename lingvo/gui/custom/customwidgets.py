#!/usr/bin/env python3

import sys
from PyQt5 import QtWidgets, QtCore



#!/usr/bin/env python3

import sys
from PyQt5 import QtWidgets, QtCore



class ToolTypeFrame(QtWidgets.QFrame):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName(name)
        self.setToolTip("{}".format(self.__class__))


class BoxLayout(QtWidgets.QBoxLayout):
    def __init__(self, direction, parent, **kwargs):
        super().__init__(direction, parent)
        self.setDirection(direction)
        self.setParent(parent)
        contentMargin = kwargs.get("content_margin", (0, 0, 0, 0))
        spacing = kwargs.get("spacing", 0)
        self.setContentsMargins(*contentMargin)
        self.setSpacing(spacing)

class Widget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.resize(500, 500)
        self.box = BoxLayout(QtWidgets.QBoxLayout.BottomToTop, self)
        self.box.addWidget(QtWidgets.QPushButton("1"))
        self.box.addWidget(QtWidgets.QPushButton("2"))
        self.box.addWidget(QtWidgets.QPushButton("3"))
        self.box.addWidget(QtWidgets.QPushButton("4"))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet(open('./etc/{0}.qss'.format('style'), "r").read())
    main = Widget()
    main.show()
    sys.exit(app.exec_())