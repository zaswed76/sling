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
        self.setFont(QFont("Arial", 12))
        self.setDragEnabled(True)
        self.setFixedWidth(150)
        self.l1 = QListWidgetItem("Word")
        self.l1.setTextAlignment(Qt.AlignLeft)

        self.l2 = QListWidgetItem("Перевод")
        self.l2.setTextAlignment(Qt.AlignLeft)

        self.l3 = QListWidgetItem("Транскрипция")
        self.l3.setTextAlignment(Qt.AlignLeft)

        self.l4 = QListWidgetItem("Пример")
        self.l4.setTextAlignment(Qt.AlignLeft)

        self.insertItem(0, self.l1)
        self.insertItem(1, self.l2)
        self.insertItem(2, self.l3)
        self.insertItem(3, self.l4)

    def mouseMoveEvent(self, e):
        mimeData = QMimeData()
        mimeData.setText(self.currentItem().text())
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        dropAction = drag.exec_(Qt.MoveAction)


class View(QtWidgets.QFrame):
    def __init__(self, main):
        super().__init__()

        self.main = main
        self.setFixedSize(510, 510)
        self.box = QtWidgets.QVBoxLayout(self)
        self.box.setSpacing(0)
        self.box.setContentsMargins(1, 1, 1, 1)

        self.t = Top()
        self.c = Center()
        self.b = Bottom()

        self.box.addWidget(self.t, stretch=5)
        self.box.addWidget(self.c, stretch=5)
        self.box.addWidget(self.b, stretch=5)


class CardEditView(QtWidgets.QFrame):
    def __init__(self, main):
        """
        todo examples style
        :param main:
        """
        super().__init__()
        self.setFixedSize(700, 700)
        self.currentSide = "front"
        self.main = main
        self.box = QtWidgets.QHBoxLayout(self)
        self.box.setSpacing(1)
        self.box.setContentsMargins(1, 1, 1, 1)
        self.left = Left()
        self.box.addWidget(self.left)
        self.box.addStretch(1)
        self.lbSide = LbSide(True, self)
        self.vcbox = QtWidgets.QVBoxLayout(self)
        self.vcbox.setSpacing(50)
        self.vcbox.setContentsMargins(1, 1, 1, 1)
        self.cardsStack = QStackedWidget()
        self.vcbox.addStretch(7)
        self.vcbox.addWidget(self.lbSide)
        self.vcbox.addWidget(self.cardsStack)
        self.vcbox.addStretch(10)

        self.sides = dict(
            front=View(self.main),
            back=View(self.main)
        )
        self.sides["back"].setStyleSheet('background: #033367;')
        self.cardsStack.addWidget(self.sides["front"])

        self.cardsStack.addWidget(self.sides["back"])

        self.cardsStack.setCurrentWidget(self.sides[self.currentSide])

        self.box.addLayout(self.vcbox)
        self.box.addStretch(1)

    def changeSide(self, side):
        self.currentSide = side
        self.cardsStack.setCurrentWidget(self.sides[self.currentSide])


class LbSide(QLabel):
    def __init__(self, side, parent, *__args):
        super().__init__(*__args)
        self.parent = parent
        self.side = side
        self.textSide = {True: "front", False: "back"}
        self.setText(self.textSide[self.side])
        self.setFont(QFont("arial", 20))
        self.setAlignment(Qt.AlignCenter)

    def mousePressEvent(self, e):
        self.changeSide()

    def changeSide(self):
        self.side = not self.side
        self.setText(self.textSide[self.side])
        self.parent.changeSide(self.textSide[self.side])


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet(open('./etc/{0}.qss'.format('style'), "r").read())
    main = Widget()
    main.show()
    sys.exit(app.exec_())
