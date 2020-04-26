import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from tools.handler import qt_message_handler
qInstallMessageHandler(qt_message_handler)


class TuneDropWidgetItem(QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlag(Qt.Tool)

class SoundBtn(QPushButton):
    def __init__(self, *__args):
        super().__init__(*__args)

class CloseDropLabelBtn(QPushButton):
    def __init__(self, *__args):
        super().__init__(*__args)

class TuneDropLabelBtn(QPushButton):
    def __init__(self, *__args):
        super().__init__(*__args)

class ControlsDropLabel(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.box = AbcBoxLayout(QBoxLayout.LeftToRight, parent=self)
        self.closeDropLabelBtn = CloseDropLabelBtn(self)
        self.tuneDropLabelBtn = TuneDropLabelBtn(self)
        self.box.addWidgets([self.closeDropLabelBtn, self.tuneDropLabelBtn])

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
    def __init__(self, objectName, QBoxLayout_Direction, cardModel, side, index, *args, **kwargs):
        """
        виджет-контейнер в который можно перетащить другие виджеты
        top center, bottom
        :param objectName:
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        self.index = index
        self.side = side
        self.cardModel = cardModel
        self.setObjectName(objectName)
        self.__components = {}
        self.box = AbcBoxLayout(QBoxLayout_Direction)
        self.setToolTip(self.objectName())
        self.setAcceptDrops(True)

    def addComponent(self, qwidget):
        self.__components[id(qwidget)] = qwidget
        self.box.addWidget(self.__components[id(qwidget)])


class AbcDropLabel(QLabel):
    def __init__(self, *__args):
        super().__init__(*__args)

    def __repr__(self):
        return "AbcDropLabel"

class AbcSide(QFrame):
    def __init__(self, layout: QBoxLayout, objectName=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName(objectName)
        self.box = layout(self)

    def setSpacing(self, s):
        self.box.setSpacing(s)

    def addWidget(self, widget):
        self.box.addWidget(widget)

    def setWidgets(self, widgets_list):
        for w in widgets_list:
            self.addWidget(w)

    @property
    def layouts(self):
        lst = []
        for i in range(self.box.count()):
            lst.append(self.box.itemAt(i).widget())
        return lst

    def __repr__(self):
        return str(self.layouts)

class AbcDropWidgetItem(QFrame):
    def __init__(self, widget_tipe, text=None, idO=None, soundBtn=False, *args, **kwargs):
        """
        этот виджет добавляем в контейнер AbcDropLayout
        :param widget_tipe:
        :param text:
        :param args:
        :param kwargs:
        """

        super().__init__(*args, **kwargs)
        if idO is None:
            self.idO = id(self)
        else:
            self.idO = idO

        self.widgetType = widget_tipe
        self.text = text
        self.installEventFilter(self)
        self.box = QHBoxLayout(self)
        self.box.setContentsMargins(0, 0, 0, 0)
        self.box.setSpacing(0)
        self.resize(100, 100)

    # def enabledIcon(self, enabled):
    #     if enabled:
    #         self.soundBtn.setIcon(QIcon(":/volume.png"))
    #     else:
    #         self.soundBtn.setIcon(QIcon())

    # def resizeEvent(self, e):
    #     rect = self.component.rect()
    #     center = rect.center()
    #     right = rect.right()
    #     center.setX(right-175)
    #     center.setY(int(center.y()-25/2))
    #     self.soundBtn.move(center)
    #     self.controlsDropLabel.move(rect.topLeft() + QPoint(5, 5))

    # def eventFilter(self, obj, event):
    #     if event.type() == 11:  # Если мышь покинула область фиджета
    #         self.controlsDropLabel.hide()  # выполнить  callback1()
    #     elif event.type() == 10:# Если мышь над виджетом
    #         self.controlsDropLabel.show()  # выполнить  callback2()
    #     return False

    def __repr__(self):
        return "{}-{}".format(self.__class__.__name__, self.idO)

class AbcViewCard(QStackedWidget):
    def __init__(self, *args, **kwargs):
        """
        визуальная модель карточки
        """

        super().__init__(*args, **kwargs)
        self.__currentSideIndex = 0
        self.sideNames = ('front', 'back')
        self.sides = {}
        self.dropsLayouts = {}
        self.sides["front"] = AbcSide(AbcVBoxLayout, "front")
        self.sides["front"].setSpacing(1)
        self.sides["back"] = AbcSide(AbcVBoxLayout, "back")
        self.sides["back"].setSpacing(1)
        self.setSides(self.sides.values())

    def updateContent(self):
        for sideName, side in self.cardModel.sides.items():
            for index, dropLayoutModel in enumerate(side):
                self.dropsLayouts[dropLayoutModel.name] = AbcDropLayout(dropLayoutModel.name,
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
            qwidget = AbcDropWidgetItem(widgetType, text=text, idO=idO,  soundBtn=comp.soundBtn)
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
    dropWidgetItem = AbcDropWidgetItem("AbcDropLabel", "word")
    dropWidgetItem.show()
    sys.exit(app.exec_())


# if __name__ == '__main__':
#
#     def keyPressEvent(e):
#         if e.key() == Qt.Key_Space:
#             card.changeSide()
#
#
#     app = QApplication(sys.argv)
#     # app.setStyleSheet(open('./etc/{0}.qss'.format('style'), "r").read())
#     main = QFrame()
#     main.keyPressEvent = keyPressEvent
#     box = QHBoxLayout(main)
#     card = AbcViewCard()
#     card.setSides([QLabel("front"), QLabel("back")])
#     box.addWidget(card)
#     main.show()
#     sys.exit(app.exec_())
