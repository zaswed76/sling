import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class AbcDropLabel(QLabel):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setAlignment(Qt.AlignCenter)
        self.installEventFilter(self)

class AbcBoxLayout(QBoxLayout):
    def __init__(self, QBoxLayout_Direction, parent=None, **kwargs):
        """

        :param direction: Q
        :param parent:
        :param kwargs:
        """

        super().__init__(QBoxLayout_Direction, parent)
        self.setDirection(QBoxLayout_Direction)
        self.setParent(parent)
        contentMargin = kwargs.get("content_margin", (0, 0, 0, 0))
        spacing = kwargs.get("spacing", 0)
        self.setContentsMargins(*contentMargin)
        self.setSpacing(spacing)

    def addWidgets(self, QWidgets_list, *args, **kwargs):
        for QWidget in QWidgets_list:
            self.addWidget(QWidget, *args, **kwargs)


class AbcVBoxLayout(QVBoxLayout):
    def __init__(self, parent):
        super().__init__(parent)
        self.setParent(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)





class AbcDropLayout(QFrame):
    def __init__(self, objectName, QBoxLayout_Direction,  cardModel, side, index , *args, **kwargs):
        """
        виджет-контейнер в который можно перетащить другие виджеты
        :param objectName:
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        self.index = index
        self.side = side
        self.cardModel = cardModel
        self.setObjectName(objectName)
        self.components = {}

        self.box = AbcBoxLayout(QBoxLayout_Direction, self)
        self.setToolTip(self.objectName())
        self.setAcceptDrops(True)

    def setContentLayout(self, QLayout):
        self.box = QLayout(self)

    def dragEnterEvent(self, e):
        pass
        e.accept()

    def dropEvent(self, e):
        pass
        mime = e.mimeData()
        text = mime.text()
        print(text)
        e.accept()

    def addComponent(self, component):
        self.components[id(component)] = component
        self.box.addWidget(self.components[id(component)])

    def removeComponent(self ,id):
        print(id)
        self.box.removeWidget(self.components[id])
        self.components[id].deleteLater()
        # print(component, "component")
        # for i in range(self.box.count()):
        #     print(self.box.takeAt(i), "1111")

class AbcSide(QFrame):
    def __init__(self, layout: QBoxLayout, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.box = layout

    def addWidget(self, widget):
        self.box.addWidget(widget)

    def setWidgets(self, widgets_list):
        for w in widgets_list:
            # print(w)
            self.addWidget(w)


class AbcViewCard(QStackedWidget):
    def __init__(self, *args, **kwargs):
        """
        визуальная модель карточки
        """

        super().__init__(*args, **kwargs)
        self.__currentSideIndex = 0
        self.sideNames = ('front', 'back')
        self.sides = {}

    def setSide(self, side_name, widget):
        self.sides[side_name] = widget
        self.addWidget(self.sides[side_name])

    def setSides(self, widgets_list):
        for name, widget in zip(self.sideNames, widgets_list):
            self.setSide(name, widget)

    def updateContent(self):
        pass
        # print("view", self.__cardModel)

    def setCardModel(self, cardModel):
        self.__cardModel = cardModel
        self.updateContent()

    @property
    def cardModel(self):
        return self.__cardModel

    @property
    def currentSideIndex(self):
        return self.__currentSideIndex

    @currentSideIndex.setter
    def currentSideIndex(self, index):
        if index:
            self.__currentSideIndex = 1
        else:
            self.__currentSideIndex = 0

    def changeSide(self):
        self.currentSideIndex = not self.currentSideIndex
        self.setCurrentIndex(self.currentSideIndex)




if __name__ == '__main__':

    def keyPressEvent(e):
        if e.key() == Qt.Key_Space:
            card.changeSide()


    app = QApplication(sys.argv)
    # app.setStyleSheet(open('./etc/{0}.qss'.format('style'), "r").read())
    main = QFrame()
    main.keyPressEvent = keyPressEvent
    box = QHBoxLayout(main)
    card = AbcViewCard()
    card.setSides([QLabel("front"), QLabel("back")])
    box.addWidget(card)
    main.show()
    sys.exit(app.exec_())
