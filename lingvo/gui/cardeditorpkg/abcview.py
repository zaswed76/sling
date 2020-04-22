import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import paths
from gui.custom.drag import *
from gui.cardeditorpkg.droplistview import DropListWidget
from gui.cardeditorpkg.dropframe import DropFrame

class AbcViewCard(QStackedWidget):
    def __init__(self, *args, **kwargs):
        """
        визуальная модель карточки
        """

        super().__init__(*args, **kwargs)
        self.__currentSideIndex = 0
        # self.cardModel = cardModel
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

class ViewCard(AbcViewCard):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class EditCard(AbcViewCard):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Side(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize(500, 500)
        self.box = QHBoxLayout(self)


class Frame(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.viewCard = ViewCard(self)
        self.resize(500, 500)
        self.box = QHBoxLayout(self)
        self.box.addWidget(self.viewCard)
        self.setStyleSheet("background-color: lightgrey")
        self.front = Side()
        self.front.setStyleSheet("background-color: red")
        self.back = Side()
        self.back.setStyleSheet("background-color: cyan")
        self.viewCard.setSides([self.front, self.back])


    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Space:
            self.viewCard.changeSide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(open('./etc/{0}.qss'.format('style'), "r").read())
    main = Frame()
    main.show()
    sys.exit(app.exec_())