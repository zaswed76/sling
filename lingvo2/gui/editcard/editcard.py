
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from gui.custom.abccard import *
from gui.custom import dropcomponents, dropitem









class DropLayout(AbcDropLayout):
    def __init__(self, objectName, QBoxLayout_Direction, cardModel, side, index ,*args, **kwargs):
        """
        виджет-контейнер в который можно перетащить другие виджеты
        top center, bottom
        """
        super().__init__(objectName, QBoxLayout_Direction, cardModel, side, *args, index , **kwargs)


    def dropEvent(self, e):
        sideName = self.parent().objectName()
        mime = e.mimeData()
        component = mime.text()
        text, widgetType = component.split("_")
        qwidget = dropitem.DropWidgetItem(widgetType, text, idO=None, sound=True)
        self.cardModel.sides[sideName][self.index].appendDragItem(qwidget.idO, widgetType, text=text)
        self.addComponent(qwidget)
        e.accept()

    def __repr__(self):
        return "AbcDropLayout"

class Side(AbcSide):
    def __init__(self, layout, *args, **kwargs):
        super().__init__(layout, *args, **kwargs)
        self.box = layout(self)


    def setSpacing(self, s):
        self.box.setSpacing(s)


class EditCard(AbcViewCard):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(600, 600)
        # self.setStyleSheet("background-color: lightgrey")
        self.dropsLayouts = {}

        self.sides["front"] = Side(AbcVBoxLayout, "front")
        self.sides["front"].setSpacing(1)
        self.sides["back"] = Side(AbcVBoxLayout, "back")
        self.sides["back"].setSpacing(1)
        self.setSides(self.sides.values())

    def updateContent(self):

        for sideName, side in self.cardModel.sides.items():
            for index, dropLayoutModel in enumerate(side):
                self.dropsLayouts[dropLayoutModel.name] = DropLayout(dropLayoutModel.name, QBoxLayout.TopToBottom, self.cardModel, sideName, index)
                # контейнер на сторону
                self.sides[sideName].addWidget(self.dropsLayouts[dropLayoutModel.name])
                # компоненты в каждый контейнер если есть
                self.addComponents(dropLayoutModel)
        # for l in self.sides["front"].layouts:
        #     print(l.components)





    def addComponents(self, dropLayoutModel):
        for comp in dropLayoutModel:
            text = comp.text
            widgetType = comp.qwidgetType
            idO = comp.idO
            qwidget = dropitem.DropWidgetItem(widgetType, text, idO=idO,  sound=True)
            self.dropsLayouts[dropLayoutModel.name].addComponent(qwidget)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(open('./etc/{0}.qss'.format('style'), "r").read())
    main = EditCard()
    main.show()
    sys.exit(app.exec_())