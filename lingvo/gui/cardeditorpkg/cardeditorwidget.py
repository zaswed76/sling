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
from gui.cardeditorpkg.dropframe import DropFrame



class Card(QStackedWidget):
    def __init__(self, cardModel):
        """
        визуальная модель карточки
        """
        super().__init__()
        self.__currentSideIndex = 0
        self.cardModel = cardModel
        self.setFixedSize(510, 510)
        self.sides = {}
        self.frontSide = DropFrame("frontSide")
        self.backSide = DropFrame("backSide")
        self.sides = {0: self.frontSide, 1: self.backSide}
        self.addWidget(self.frontSide)
        self.addWidget(self.backSide)
        self.setCurrentIndex(self.currentSideIndex)
        self.updateContent()

    def updateContent(self, *__args):
        print("")



    @property
    def currentSideIndex(self):
        return self.__currentSideIndex

    @currentSideIndex.setter
    def currentSideIndex(self, index):
        if index != 0:
            index = 1
        self.__currentSideIndex = index

    def changeSide(self):
        if self.__currentSideIndex == 0:
            self.__currentSideIndex = 1
        elif self.__currentSideIndex == 1:
            self.__currentSideIndex = 0
        self.setCurrentIndex(self.__currentSideIndex)



class CardEditView(QFrame):
    def __init__(self, main, name=None, config=None,*args, **kwargs):
        """
        todo examples style
        :param main:
        """

        super().__init__(*args, **kwargs)
        self.__cardModel = None
        self.setObjectName(name)
        self.config = config if config is not None else {}

        self.setFixedSize(700, 700)
        self.currentSide = "front"
        self.main = main
        self.box = QHBoxLayout(self)
        self.box.setSpacing(1)
        self.box.setContentsMargins(1, 1, 1, 1)
        self.dropListWidget = DropListWidget(self.main, "dropListWidget")

        self.box.addWidget(self.dropListWidget)
        self.box.addStretch(1)

        self.vcbox = QVBoxLayout()
        self.vcbox.setSpacing(50)
        self.vcbox.setContentsMargins(1, 1, 1, 1)
        # карточка
        self.card = Card(self.cardModel)
        self.changeSideCardBtn = ChangeSideCardBtn(self.card.frontSide.objectName(), self)
        self.changeSideCardBtn.clicked.connect(self.changeSideCard)

        self.vcbox.addStretch(7)
        self.vcbox.addWidget(self.changeSideCardBtn)
        self.vcbox.addWidget(self.card)
        self.vcbox.addStretch(10)
        self.box.addLayout(self.vcbox)
        self.box.addStretch(1)

    def updateContent(self):
        print("edit", self.cardModel)


    def setCardModel(self, cardModel):
        self.__cardModel = cardModel
        self.updateContent()


    def setDragList(self, dragList):
        self.dropListWidget.setItems(dragList)

    @property
    def cardModel(self):
        return self.__cardModel


    def changeSideCard(self):
        self.card.changeSide()
        self.changeSideCardBtn.setText(self.card.currentWidget().objectName())


class ChangeSideCardBtn(QPushButton):
    def __init__(self, *__args):

        super().__init__(*__args)
        self.setFont(QFont("arial", 20))




if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(open('./etc/{0}.qss'.format('style'), "r").read())
    main = Widget()
    main.show()
    sys.exit(app.exec_())
