from gui.custom.abccard import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from gui.custom.dropitem import *


class Side(AbcSide):
    def __init__(self, layout: QBoxLayout, objectName=None, *args, **kwarg):
        super().__init__(layout, objectName, *args, **kwarg)
        self.box = layout(self)


class DropLayout(AbcDropLayout):

    def __init__(self, objectName, QBoxLayout_Direction, cardModel, side, index, *args, **kwargs):
        """
        виджет-контейнер в который можно перетащить другие виджеты
        top center, bottom
        """

        super().__init__(objectName, QBoxLayout_Direction, cardModel, side, index, *args, **kwargs)
        self.index = index
        self.side = side
        self.cardModel = cardModel
        self.setObjectName(objectName)
        self.__components = {}
        self.setAcceptDrops(True)
        self.box = AbcBoxLayout(QBoxLayout_Direction, self)


    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        sideName = self.parent().objectName()
        mime = e.mimeData()
        component = mime.text()
        text, widgetType = component.split("_")
        qwidget = DropWidgetItem(widgetType, text=text, idO=None, soundBtnFlag=self.cardModel.soundBtnDefault)
        self.cardModel.sides[sideName][self.index].appendDragItem(qwidget.idO, widgetType, text=text)
        self.addComponent(qwidget)
        e.accept()

    # def addComponent(self, qwidget):
    #     self.__components[qwidget.idO] = qwidget
    #     self.box.addWidget(self.__components[qwidget.idO])

    # def removeComponent(self, idO):
    #     self.box.removeWidget(self.__components[idO])
    #     self.__components[idO].deleteLater()



    def __repr__(self):
        return "AbcDropLayout"

    def __repr__(self):
        return "AbcDropLayout"


class DropLabel(AbcDropLabel):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setObjectName(self.text())
