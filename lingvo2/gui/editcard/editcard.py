
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from gui.custom.dropcomponents import *
from gui.custom.dropitem import *


class EditCard(QStackedWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(600, 600)
        self.__currentSideIndex = 0
        self.sideNames = ('front', 'back')
        self.sides = {}
        self.dropsLayouts = {}
        self.sides["front"] = Side(AbcVBoxLayout, "front")
        self.sides["front"].setSpacing(1)
        self.sides["back"] = Side(AbcVBoxLayout, "back")
        self.sides["back"].setSpacing(1)
        self.setSides(self.sides.values())

    @property
    def cardModel(self):
        return self.__cardModel

    def setCardModel(self, cardModel):
        self.__cardModel = cardModel
        self.updateContent()

    def updateContent(self):
        for sideName, side in self.cardModel.sides.items():
            for index, dropLayoutModel in enumerate(side):
                self.dropsLayouts[dropLayoutModel.name] = DropLayout(dropLayoutModel.name,
                                                                     QBoxLayout.TopToBottom,
                                                                     self.cardModel,
                                                                     sideName,
                                                                     index)
                # контейнер на сторону
                self.sides[sideName].addWidget(self.dropsLayouts[dropLayoutModel.name])
                # компоненты в каждый контейнер если есть
                self.addComponents(dropLayoutModel)


    def addComponents(self, dropLayoutModel):
        for comp in dropLayoutModel:
            text = comp.text
            widgetType = comp.qwidgetType
            idO = comp.idO
            qwidget = DropWidgetItem(widgetType, text=text, idO=idO,  soundBtn=comp.soundBtn)
            self.dropsLayouts[dropLayoutModel.name].addComponent(qwidget)

    def setSide(self, side_name, widget):
        self.sides[side_name] = widget
        self.addWidget(self.sides[side_name])

    def setSides(self, widgets_list):
        for name, widget in zip(self.sideNames, widgets_list):
            self.setSide(name, widget)

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

    def __repr__(self):
        return "AbcViewCard"


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(open('./etc/{0}.qss'.format('style'), "r").read())
    main = EditCard()
    main.show()
    sys.exit(app.exec_())