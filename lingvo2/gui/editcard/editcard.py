
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from gui.custom.abccard import *

class DropLabel(AbcDropLabel):
    def __init__(self, *__args):
        super().__init__(*__args)



class DropLayout(AbcDropLayout):
    def __init__(self, objectName, *args, **kwargs):
        super().__init__(objectName, *args, **kwargs)
        self.setStyleSheet("background-color: white")



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
        self.setStyleSheet("background-color: lightgrey")
        self.drops = {}

        self.sides["front"] = Side(AbcVBoxLayout)
        self.sides["front"].setSpacing(1)
        self.sides["back"] = Side(AbcVBoxLayout)
        self.sides["back"].setSpacing(1)
        self.setSides(self.sides.values())

    def updateContent(self):
       for sideName, side in self.cardModel.sides.items():
           for dropBox in side:
               self.drops[dropBox.name] = DropLayout(dropBox.name, QBoxLayout.TopToBottom)
               self.sides[sideName].addWidget(self.drops[dropBox.name])
               for comp in dropBox:
                   self.drops[dropBox.name].addComponent(DropLabel(comp.text))




if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(open('./etc/{0}.qss'.format('style'), "r").read())
    main = EditCard()
    main.show()
    sys.exit(app.exec_())