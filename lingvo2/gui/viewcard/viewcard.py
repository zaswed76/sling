
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

        self.setObjectName(objectName)

        self.box = QHBoxLayout(self)
        self.box.addWidget(viewCard)





class ViewCard(AbcViewCard):
    def __init__(self, dictsModel, main=None, *args, **kwargs):

        super().__init__(main, *args, **kwargs)
        self.main = main
        self.dictsModel = dictsModel

    def updateContent(self, wordItem):
        if not self.isComponent():
            return

        if wordItem is None:
            return
        for nameSide, side in self.sides.items():
            for layout in side.layouts:
                for component in layout.components:
                    widget = component
                    textType = component.text
                    text = wordItem.getTypeText(textType)
                    spoilerText = wordItem.getSpoiler()
                    image = wordItem.getImage()
                    if text is not None:
                        widget.setText(text)
                        widget.enabledIcon(True)
                        if textType == "spoilerExample":
                            widget.hideSpoiler()
                            if spoilerText:
                                widget.setSpoiletText(spoilerText)
                            else:
                                widget.setSpoiletText("")
                        elif textType == "image" and image:
                            widget.setPixmap(QPixmap(image))
                    else:
                        widget.clearText()
                        widget.enabledIcon(False)

    # def changeSide(self):
    #     return super().changeSide()

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

    def update2(self):

        for sideName, side in self.cardModel.sides.items():
            for index, dropLayoutModel in enumerate(side):
                self.addComponents(dropLayoutModel)

    def addComponents(self, dropLayoutModel):
        for comp in dropLayoutModel:
            text = comp.text
            widgetType = comp.qwidgetType
            idO = comp.idO
            comp.soundBtn = self.cardModel.soundBtnDefault
            qwidget = WidgetItem(widgetType, text=text, idO=idO,
                                 soundBtnFlag=comp.soundBtn, main=self.main)

            if widgetType == "ImageLabel":
                qwidget.setPixmap(QPixmap(":/photo_landscape_big.png"))
            if qwidget.soundBtn is not None:
                qwidget.soundBtn.clicked.connect(self.main.soundClick)
            qwidget.setObjectNameComponent(text)
            self.dropsLayouts[dropLayoutModel.name].addComponent(qwidget)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(open('./etc/{0}.qss'.format('style'), "r").read())
    main = ViewCard()
    main.show()
    sys.exit(app.exec_())