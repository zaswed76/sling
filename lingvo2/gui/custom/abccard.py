import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from gui.custom import dropcomponents

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
        self.setCursor(QCursor(Qt.PointingHandCursor))

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
        self.box = AbcBoxLayout(QBoxLayout_Direction, None)

    def addComponent(self, qwidget):
        self.__components[qwidget.idO] = qwidget
        self.box.addWidget(self.__components[qwidget.idO])

    def removeComponent(self, idO):
        self.box.removeWidget(self.__components[idO])
        self.__components[idO].deleteLater()


    def removeComponents(self):
        for i in range(self.box.count()):
            item = self.box.itemAt(i)
            if item is not None:
                widget = item.widget()
                self.removeComponent(widget.idO)


    @property
    def components(self):
        lst = []
        for i in range(self.box.count()):
            lst.append(self.box.itemAt(i).widget())
        return lst

    def clear(self):
        for i in range(self.box.count()):
            self.box.takeAt(i)
        self.__components.clear()

class AbcDropLabel(QLabel):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setWordWrap(True)



    def __repr__(self):
        return "AbcDropLabel"

class AbcSide(QFrame):
    def __init__(self, layout: QBoxLayout, objectName=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName(objectName)
        self.box = layout(self)

    def _clear(self):
        for i in range(self.box.count()):
            item = self.box.itemAt(i)
            if item is not None:
                widget = item.widget()
                widget.removeComponents()



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
    def __init__(self, widget_tipe, text=None, idO=None, soundBtnFlag=False, main=None, *args, **kwargs):
        """
        этот виджет добавляем в контейнер AbcDropLayout
        :param widget_tipe:
        :param text:
        :param args:
        :param kwargs:
        """

        super().__init__(*args, **kwargs)
        self.main = main
        self.widgetType = widget_tipe
        self.text = text
        self.soundBtn = None

        self.box = QHBoxLayout(self)
        self.box.setContentsMargins(0, 0, 0, 0)
        self.box.setSpacing(0)

        if idO is None:
            self.idO = id(self)
        else:
            self.idO = idO

        self.component = getattr(dropcomponents, widget_tipe)()

        if text:
            self.component.setText(text)
        self.box.addWidget(self.component)

        if text in ["Word", "spoilerExample", "example2"]:
            self.soundBtn = SoundBtn(self.component)
            self.enabledIcon(soundBtnFlag)

    def setSpoiletText(self, text):
        print(text)
        try:
            self.component.setSpoiletText(text)
        except AttributeError:
            pass

    def hideSpoiler(self):
        try:
            self.component.hideSpoiler()
        except AttributeError:
            pass

    def setObjectNameComponent(self, objectName):
        self.component.setObjectName(objectName)

    def clearText(self):
        self.component.clear()

    def setText(self, text):
        self.component.setText(text)

    def enabledIcon(self, enabled):
        if self.soundBtn is None:
            return
        if enabled:
            self.soundBtn.setIcon(QIcon(":/volume.png"))
        else:
            self.soundBtn.setIcon(QIcon())

    def resizeEvent(self, e):
        rect = self.component.rect()
        center = rect.center()
        right = rect.right()
        mx = 45
        if self.widgetType == "SpoilerExampleLabel":
            mx +=40
        center.setX(right-mx)
        center.setY(int(center.y()-25/2))
        if self.soundBtn is not None:
            self.soundBtn.move(center)


    def __repr__(self):
        return "{}-{}".format(self.__class__.__name__, self.idO)

class AbcViewCard(QStackedWidget):
    def __init__(self, main=None, *args, **kwargs):
        """
        визуальная модель карточки
        """

        super().__init__()
        self.main = main
        self.__currentSideIndex = 1
        self.sideNames = ['front', 'back']
        self.sides = {}
        self.dropsLayouts = {}
        self.sides["front"] = AbcSide(AbcVBoxLayout, "front")
        self.sides["front"].setSpacing(0)
        self.sides["back"] = AbcSide(AbcVBoxLayout, "back")
        self.sides["back"].setSpacing(1)
        self.setSides(self.sides.values())
        self.changeSide()

    def clearComponents(self):
        for side in self.sides.values():
            for i in range(side.box.count()):
                item = side.box.itemAt(i)
                if item is not None:
                    widget = item.widget()
                    widget.removeComponents()



    def updateWidgetComponent(self):
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


    def isComponent(self):
        for nameSide, side in self.sides.items():
            for layout in side.layouts:
                for component in layout.components:
                    if component: return True
        else:
            return False


    def setSide(self, side_name, widget):
        self.sides[side_name] = widget
        self.addWidget(self.sides[side_name])

    def setSides(self, widgets_list):
        for name, widget in zip(self.sideNames, widgets_list):
            self.setSide(name, widget)

    def setCardModel(self, cardModel):
        self.__cardModel = cardModel
        self.updateWidgetComponent()

    @property
    def cardModel(self):
        return self.__cardModel

    @property
    def currentSideIndex(self):
        return self.__currentSideIndex

    @property
    def currentSideName(self):
        return self.sideNames[self.currentSideIndex]

    @currentSideIndex.setter
    def currentSideIndex(self, index):
        if index:
            self.__currentSideIndex = 1
        else:
            self.__currentSideIndex = 0

    def changeSide(self):
        x = 4 if self.currentSideIndex else -4
        shadow = QGraphicsDropShadowEffect(blurRadius=30, xOffset=x, yOffset=4)
        self.setGraphicsEffect(shadow)
        self.currentSideIndex = not self.currentSideIndex
        self.setCurrentIndex(self.currentSideIndex)
        return self.currentSideName

    def sideToName(self, name):
        self.setCurrentWidget(self.sides[name])
        self.currentSideIndex = self.sideNames.index(name)
        return self.currentSideName


    def __repr__(self):
        return "AbcViewCard"



if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(open('./etc/{0}.qss'.format('style'), "r").read())
    dropWidgetItem = AbcDropWidgetItem("AbcDropLabel", "word")
    dropWidgetItem.show()
    sys.exit(app.exec_())



