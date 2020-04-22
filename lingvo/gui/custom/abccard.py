import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class DropLayout(QFrame):
    def __init__(self, objectName, *args, **kwargs):
        """
        виджет-контейнер в который можно перетащить другие виджеты
        :param objectName:
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        self.setObjectName(objectName)
        self.setAcceptDrops(True)
        self.box = None

    def setLayout(self, QLayout):
        self.box = QLayout

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        mime = e.mimeData()
        text = mime.text()
        e.accept()


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
        print("view", self.__cardModel)

    def setCardModel(self, cardModel):
        self.__cardModel = cardModel
        self.updateContent()

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
