from gui.custom.abccard import *


class ViewLayout(AbcDropLayout):

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
        self.box = AbcBoxLayout(QBoxLayout_Direction, self)

    def addComponent(self, qwidget):
        self.__components[qwidget.idO] = qwidget
        self.box.addWidget(self.__components[qwidget.idO])





