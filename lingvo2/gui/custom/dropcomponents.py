from gui.custom.abccard import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from gui.custom.dropitem import *
from gui.spoiler import gspoiler


class Side(AbcSide):
    def __init__(self, layout: QBoxLayout, objectName=None, *args, **kwarg):
        super().__init__(layout, objectName, *args, **kwarg)
        self.box = layout(self)


class DropLayout(AbcDropLayout):

    def __init__(self, objectName, QBoxLayout_Direction, cardModel, side, index, main=None, *args, **kwargs):
        """
        виджет-контейнер в который можно перетащить другие виджеты
        top center, bottom
        """

        super().__init__(objectName, QBoxLayout_Direction, cardModel, side, index, main=None, *args, **kwargs)
        self.main = main
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
        qwidget = DropWidgetItem(widgetType, text=text, idO=None, soundBtnFlag=self.cardModel.soundBtnDefault,
                                 main=self.main)
        self.cardModel.sides[sideName][self.index].appendDragItem(qwidget.idO, widgetType, text=text)
        self.addComponent(qwidget)
        e.accept()





    def __repr__(self):
        return "AbcDropLayout"




class DropLabel(AbcDropLabel):
    def __init__(self, main, *__args):

        super().__init__(main, *__args)
        self.main = main
        self.cfg = self.main.cfg


class SpoilerExampleLabel(QFrame):
    def __init__(self, main, *__args, **kwargs):

        super().__init__(*__args, **kwargs)
        self.main = main
        self.cfg =self.main.cfg
        self.box = QVBoxLayout(self)
        self.box.setContentsMargins(0, 0, 0, 0)
        self.box.setSpacing(0)
        cardSize = self.cfg["ui"]["viewCardSize"]
        btn = gspoiler.SpoilerBtn()
        base = gspoiler.SpoilerBaseLabel()
        base.setFixedSize(cardSize[0]/1.12, cardSize[1]/6.5)
        base.textWidth = cardSize[0]/10
        base.minFont = int(cardSize[0]/53)
        if base.minFont < 10: base.minFont = 10

        spoiler = gspoiler.SpoilerLabel()
        spoiler.setFixedSize(cardSize[0]/1.25, cardSize[1]/7.6)
        spoiler.textWidth = cardSize[0]/10
        spoiler.minFont = int(cardSize[0]/53)
        # spoiler.setStyleSheet('background-color: lightgrey;')

        self.spoilerWidget = gspoiler.SpoilerWidget(baseLabel=base, spoiLerLabel=spoiler, spoilerBtn=btn,
                                                    indenttopArrow=8, spoilertopIndent=3)

        self.spoilerWidget.setSpoilerText("спойлер")
        self.box.addWidget(self.spoilerWidget)

    def clear(self):
        self.spoilerWidget.clear()

    def setText(self, text):
        self.spoilerWidget.setText(text)

    def text(self):
        self.spoilerWidget.text()

    def hideSpoiler(self):
        self.spoilerWidget.hideSpoiler()


    def setSpoiletText(self, text):
        self.spoilerWidget.setSpoilerText(text)


