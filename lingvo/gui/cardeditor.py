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
    def __init__(self, parent, object_name, cfg):
        super().__init__(parent, object_name, cfg)





class Center(DragFrame):
    def __init__(self, parent, object_name, cfg):
        super().__init__(parent, object_name, cfg)




class Bottom(DragFrame):
    def __init__(self, parent, object_name, cfg):
        super().__init__(parent, object_name, cfg)


class DropItem(QListWidgetItem):
    def __init__(self, type, *__args):
        super().__init__(*__args)
        self.type = type



class Left(QtWidgets.QListWidget):
    def __init__(self, main, name, cfg):
        super().__init__()
        self.cfg = cfg
        self.name = name
        self.main = main
        self.setFont(QFont("Arial", 12))
        self.setDragEnabled(True)
        self.setFixedWidth(150)

        self.dropItems = self.cfg["card"]["dropItems"]
        self._setItems(self.dropItems)


    def _setItems(self, drop_itrms):

        for id, text in enumerate(drop_itrms):
            text, type = text.split("_")
            item = DropItem(type, text)
            item.setTextAlignment(Qt.AlignLeft)
            self.insertItem(id, item)


    def mouseMoveEvent(self, e):
        mimeData = QMimeData()
        mimeText = "_".join((self.currentItem().text(), self.currentItem().type))
        mimeData.setText(mimeText)
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        dropAction = drag.exec_(Qt.MoveAction)


class View(QtWidgets.QFrame):
    def __init__(self, main, cfg, object_name):
        super().__init__()
        self.setObjectName(object_name)

        self.cfg = cfg
        self.main = main
        self.setFixedSize(510, 510)
        self.Mbox = QtWidgets.QHBoxLayout(self)
        self.box = QtWidgets.QVBoxLayout()
        self.Mbox.addLayout(self.box)
        self.box.setSpacing(0)
        self.box.setContentsMargins(1, 1, 1, 1)

        self.t = Top(self, "top", self.cfg)
        self.c = Center(self, "center", self.cfg)
        self.b = Bottom(self, "bottom", self.cfg)

        self.box.addWidget(self.t, stretch=5)
        self.box.addWidget(self.c, stretch=5)
        self.box.addWidget(self.b, stretch=5)


class CardEditView(QtWidgets.QFrame):
    def __init__(self, main, name=None, config=None):
        """
        todo examples style
        :param main:
        """
        super().__init__()
        self.setObjectName(name)
        self.config = config if config is not None else {}

        self.setFixedSize(700, 700)
        self.currentSide = "front"
        self.main = main
        self.box = QtWidgets.QHBoxLayout(self)
        self.box.setSpacing(1)
        self.box.setContentsMargins(1, 1, 1, 1)
        self.left = Left(self.main, "left", self.config)
        self.box.addWidget(self.left)
        self.box.addStretch(1)
        self.lbSide = LbSide(True, self)
        self.vcbox = QtWidgets.QVBoxLayout()
        self.vcbox.setSpacing(50)
        self.vcbox.setContentsMargins(1, 1, 1, 1)
        self.cardsStack = QStackedWidget()
        self.vcbox.addStretch(7)
        self.vcbox.addWidget(self.lbSide)
        self.vcbox.addWidget(self.cardsStack)
        self.vcbox.addStretch(10)

        self.sides = dict(
            front=View(self.main, self.config, "front"),
            back=View(self.main, self.config, "back")
        )
        self.sides["back"].setStyleSheet('background: #EFEFEF;')
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
