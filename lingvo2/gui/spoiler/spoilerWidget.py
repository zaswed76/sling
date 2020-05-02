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
        self.setScaledContents(True)

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





class SpoilerWidget(QFrame):
    def __init__(self, iconleft=None, iconright=None):
        super().__init__()
        self.iconright = iconright
        self.iconleft = iconleft

        self.box1 = QHBoxLayout(self)
        self.box1.setContentsMargins(0, 0, 0, 0)
        self.box1.setSpacing(0)

        self.box = QVBoxLayout()
        self.box1.addLayout(self.box)
        self.box.addStretch(10)

        self.spBtn = QSpoilerBtn(self.iconright, self.iconleft)
        self.spBtn.setStyleSheet(open("spoiler.css", "r").read())

        self.box.addWidget(self.spBtn, alignment=Qt.AlignLeft)

        self.rbox = QVBoxLayout()
        self.box1.addLayout(self.rbox)

        self.baseSpoilerLabel = BaseLabel()
        self.baseSpoilerLabel.clicked.connect(self.runSpoiler)

        self.rbox.addWidget(self.baseSpoilerLabel, alignment=Qt.AlignLeft | Qt.AlignTop)



        self.spoilerLabel = SpoilerLabel()




        self.rbox.addWidget(self.spoilerLabel)

    def runSpoiler(self):
        self.spoilerLabel.hide()

    def setText(self, text):
        self.baseSpoilerLabel.setText(text)

    def setSpoilerText(self, text):
        self.spoilerLabel.setText(text)

class Widget(QFrame):
    def __init__(self):
        super().__init__()
        box = QHBoxLayout(self)
        spoilerWidget = SpoilerWidget()
        spoilerWidget.setText("это какой нибудь пример")
        spoilerWidget.setSpoilerText("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
        box.addWidget(spoilerWidget)

if __name__ == '__main__':
    import paths
    app = QApplication(sys.argv)
    main = Widget()
    main.show()
    sys.exit(app.exec_())




