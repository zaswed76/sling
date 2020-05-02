#!/usr/bin/env python3

import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from tools.handler import qt_message_handler
qInstallMessageHandler(qt_message_handler)

from gui.spoiler.Spoiler import Spoiler

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
    def __init__(self, iconleft, iconright, *__args):
        super().__init__(*__args)

        self.iconright = iconright
        self.iconleft = iconleft
        self.setCheckable(True)

        # self.setIcon(QIcon(iconleft))
        # self.setFlat(True)

    # def mousePressEvent(self, e):
    #
    #     if self.isChecked():
    #         self.setChecked(False)
    #         self.setIcon(QIcon(self.iconleft))
    #         self.setFlat(True)
    #
    #     else:
    #         self.setChecked(True)
    #         self.setIcon(QIcon(self.iconright))
    #         self.setFlat(True)





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

        self.spBtn = QSpoilerBtn("./right.png", "./left.png")
        self.spBtn.setStyleSheet(open("spoiler.css", "r").read())

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
    main = Main()
    main.show()
    sys.exit(app.exec_())




