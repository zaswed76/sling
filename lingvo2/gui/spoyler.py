#!/usr/bin/env python3

import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from tools.handler import qt_message_handler
qInstallMessageHandler(qt_message_handler)

from libs.Spoiler import Spoiler

class SpoilerLabel(QLabel):
    def __init__(self, *__args):
        super().__init__(*__args)

class BaseLabel(QLabel):
    clicked = pyqtSignal()
    def __init__(self, *__args):
        super().__init__(*__args)

    def mousePressEvent(self, QMouseEvent):
        self.clicked.emit()

class QSpoilerBtn(QPushButton):
    def __init__(self, icon=None, *__args):
        super().__init__(*__args)
        self.icon = icon
        self.setCheckable(True)
        self.setText(">")

        # if icon is not None:
        #     self.setIcon(QIcon(icon))
        # self.setFlat(True)

    def mousePressEvent(self, e):

        if self.isChecked():
            self.setChecked(False)
            self.setText(">")
        else:
            self.setChecked(True)
            self.setText("<")




def fun(spoiler):
    if spoiler.isOpened():
        spoiler.close()
    else:
        spoiler.open()

class Main(QFrame):
    def __init__(self):
        super().__init__()
        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(0)

        self.baseLabel = BaseLabel("это надпись\nв две строки")
        self.baseLabel.clicked.connect(lambda: fun(self.spoiler))

        self.spBtn = QSpoilerBtn(">")

        self.spoilerLb = SpoilerLabel("это спойлер")
        self.spoilerLayout = QHBoxLayout()
        self.spoilerLayout.addWidget(self.spoilerLb)
        self.spoiler = Spoiler(Spoiler.Orientation.HORIZONTAL)
        self.spoiler.setContentLayout(self.spoilerLayout)


        self.grid.addWidget(self.baseLabel, 0, 0)
        self.grid.addWidget(self.spBtn, 1, 0)
        self.grid.addWidget(self.spoiler, 1, 1)


    def clickSpoyler(self):
        print("ddddddddd")

if __name__ == '__main__':
    import paths
    app = QApplication(sys.argv)
    stylepath = paths.CSS / "base/spoiler.css"
    app.setStyleSheet(open(stylepath, "r").read())
    main = Main()
    main.show()
    sys.exit(app.exec_())