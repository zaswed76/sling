
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from gui.custom.dropcomponents import *
from gui.custom.dropitem import *


class EditCard(AbcViewCard):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(600, 600)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Right:
            print(">>>>>>>")
        elif e.key() == Qt.Key_Left:
            print("<<<<<<<<<<<<")
        elif e.key() == Qt.Key_Space:
            self.changeSide()

    def updateWidgetComponent(self):
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
            # todo тут принудительно присвоили свойство soundBtn = self.cardModel.soundBtnDefault
            comp.soundBtn = self.cardModel.soundBtnDefault
            text = comp.text
            widgetType = comp.qwidgetType
            idO = comp.idO
            print(widgetType, text, "EEEEEEEEEEEEE")
            qwidget = DropWidgetItem(widgetType, text=text, idO=idO,  soundBtnFlag=comp.soundBtn)
            self.dropsLayouts[dropLayoutModel.name].addComponent(qwidget)

    def __repr__(self):
        return "AbcViewCard"


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(open('./etc/{0}.qss'.format('style'), "r").read())
    main = EditCard()
    main.show()
    sys.exit(app.exec_())