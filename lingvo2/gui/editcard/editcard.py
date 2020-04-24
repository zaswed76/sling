
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from gui.custom.abccard import *
from gui.custom import dropcomponents









class DropLayout(AbcDropLayout):
    def __init__(self, objectName, QBoxLayout_Direction, cardModel, side, index ,*args, **kwargs):
        super().__init__(objectName, QBoxLayout_Direction, cardModel, side, *args, index , **kwargs)


    def dropEvent(self, e):
        pass
        mime = e.mimeData()
        component = mime.text()
        text, widgetType = component.split("_")
        self.cardModel.sides["front"][self.index].appendDragItem(widgetType, text=text)
        qwidget = getattr(dropcomponents, widgetType)
        self.addComponent(qwidget(text))

        e.accept()


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
        self.drops = {}

        self.sides["front"] = Side(AbcVBoxLayout)
        self.sides["front"].setSpacing(1)
        self.sides["back"] = Side(AbcVBoxLayout)
        self.sides["back"].setSpacing(1)
        self.setSides(self.sides.values())

    def updateContent(self):
       for sideName, side in self.cardModel.sides.items():
           for index, dropBox in enumerate(side):
                self.drops[dropBox.name] = DropLayout(dropBox.name, QBoxLayout.TopToBottom, self.cardModel, sideName, index)
                self.sides[sideName].addWidget(self.drops[dropBox.name])
                self.addComponent(dropBox)



    def addComponent(self, dropBox):
        for comp in dropBox:
            text = comp.text
            widgetType = comp.qwidgetType
            qwidget = getattr(dropcomponents, widgetType)(text)
            print(id(qwidget))
            self.drops[dropBox.name].addComponent(qwidget)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(open('./etc/{0}.qss'.format('style'), "r").read())
    main = EditCard()
    main.show()
    sys.exit(app.exec_())