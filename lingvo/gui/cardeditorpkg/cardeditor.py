#!/usr/bin/env python3
import datetime
import sys
# from PyQt5 import QtWidgets, QtCore

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import paths
from gui.custom.drag import *
from gui.cardeditorpkg.droplistview import DropListWidget


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





class CardModelView(QFrame):
    def __init__(self, main, cfg, object_name):
        super().__init__()
        self.setObjectName(object_name)

        self.cfg = cfg
        self.main = main

        self.Mbox = QHBoxLayout(self)
        self.box = QVBoxLayout()
        self.Mbox.addLayout(self.box)
        self.box.setSpacing(0)
        self.box.setContentsMargins(1, 1, 1, 1)
        self._initSections()

    def _initSections(self):
        self.t = Top(self, "top", self.cfg)
        self.c = Center(self, "center", self.cfg)
        self.b = Bottom(self, "bottom", self.cfg)
        self.box.addWidget(self.t, stretch=5)
        self.box.addWidget(self.c, stretch=5)
        self.box.addWidget(self.b, stretch=5)


class CardEditModel(QStackedWidget):
    def __init__(self):
        """
        визуальная модель карточки
        """
        super().__init__()
        self.setFixedSize(510, 510)


class CardEditView(QFrame):
    def __init__(self, main, name=None, config=None, cardModel=None, *args, **kwargs):
        """
        todo examples style
        :param main:
        """
        super().__init__(*args, **kwargs)
        self.__cardModel = cardModel
        self.setObjectName(name)
        self.config = config if config is not None else {}

        self.setFixedSize(700, 700)
        self.currentSide = "front"
        self.main = main
        self.box = QHBoxLayout(self)
        self.box.setSpacing(1)
        self.box.setContentsMargins(1, 1, 1, 1)
        self.dropListWidget = DropListWidget(self.cardModel.cardCfg.data["dropItemsTypeList"],
                                             self.main, "dropListWidget")

        self.box.addWidget(self.dropListWidget)
        self.box.addStretch(1)
        self.lbSide = LbSide(True, self)
        self.vcbox = QVBoxLayout()
        self.vcbox.setSpacing(50)
        self.vcbox.setContentsMargins(1, 1, 1, 1)
        self.cardView = CardEditModel()

        self.vcbox.addStretch(7)
        self.vcbox.addWidget(self.lbSide)
        self.vcbox.addWidget(self.cardView)
        self.vcbox.addStretch(10)

        # self.sides = dict(
        #     front=CardModelView(self.main, self.config, "front"),
        #     back=CardModelView(self.main, self.config, "back")
        # )
        # self.sides["front"].setFixedSize(510, 510)
        # self.sides["back"].setStyleSheet('background: #EFEFEF;')
        # self.sides["back"].setFixedSize(510, 510)
        # self.cardsStack.addWidget(self.sides["front"])
        # self.cardsStack.addWidget(self.sides["back"])
        # self.cardsStack.setCurrentWidget(self.sides[self.currentSide])

        self.box.addLayout(self.vcbox)
        self.box.addStretch(1)

    @property
    def cardModel(self):
        return self.__cardModel

    def setCardModel(self, cardModel):
        print()
        self.__cardModel = cardModel

    def changeSide(self, side):
        self.currentSide = side
        self.cardView.setCurrentWidget(self.sides[self.currentSide])


class LbSide(QLabel):
    def __init__(self, side, parent, *__args):
        super().__init__(*__args)
        self.parent = parent
        self.side = side
        self.textSide = {True: "front", False: "back"}
        self.setText(self.textSide[self.side])
        self.setFont(QFont("arial", 20))
        self.setAlignment(Qt.AlignCenter)
    #
    # def mousePressEvent(self, e):
    #     self.changeSide()
    #
    # def changeSide(self):
    #     self.side = not self.side
    #     self.setText(self.textSide[self.side])
    #     self.parent.changeSide(self.textSide[self.side])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(open('./etc/{0}.qss'.format('style'), "r").read())
    main = Widget()
    main.show()
    sys.exit(app.exec_())
