
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from gui.custom.abccard import AbcViewCard
from gui.custom.dropcomponents import *
from gui.custom.dropitem import *
from gui.viewcard.widgetitem import WidgetItem
from gui.viewcard.components import ViewLayout

class ViewFrame(QFrame):
    def __init__(self, viewCard, objectName, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lst = [viewCard]
        self.setObjectName(objectName)
        self.setFixedSize(790, 788)
        self.box = QHBoxLayout(self)
        self.box.addWidget(viewCard)



class ViewCard(AbcViewCard):
    def __init__(self, dictsModel, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dictsModel = dictsModel
        self.setFixedSize(730, 730)


    def updateContent(self):
        for nameSide, side in self.sides.items():
            for layout in side.layouts:
                print(layout)


    def updateWidgetComponent(self):
        for sideName, side in self.cardModel.sides.items():
            for index, dropLayoutModel in enumerate(side):
                self.dropsLayouts[dropLayoutModel.name] = ViewLayout(dropLayoutModel.name,
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
            comp.soundBtn = self.cardModel.soundBtnDefault
            qwidget = WidgetItem(widgetType, text=text, idO=idO,  soundBtnFlag=comp.soundBtn)
            self.dropsLayouts[dropLayoutModel.name].addComponent(qwidget)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(open('./etc/{0}.qss'.format('style'), "r").read())
    main = ViewCard()
    main.show()
    sys.exit(app.exec_())