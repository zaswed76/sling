import datetime
import random
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import paths

from gui.custom import customwidgets

class DropLabel(QLabel):
    def __init__(self, *__args):
        super().__init__(*__args)


class Section(QFrame):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.box = customwidgets.BoxLayout(QBoxLayout.TopToBottom, self)
        self.labels = {}


        shadow = QGraphicsDropShadowEffect(blurRadius=12, xOffset=3, yOffset=3)
        self.setGraphicsEffect(shadow)

    def getWidgets(self):
        w = []
        for i in range(self.box.count()):
            w.append(self.box.itemAt(i).widget())
        return w
    @property
    def typeTegs(self):
        return {"DropLabel": self.addLabel}

    def setContent(self, _contents):
        for w, ct in zip(self.getWidgets(), _contents):
            w.setText(ct)

    def setWidget(self, widget_type):
        self.typeTegs[widget_type]()

    def addLabel(self):
        name = "lb"+self.__getSuffix()
        self.labels[name] = DropLabel()
        self.box.addWidget(self.labels[name])

    def __getSuffix(self):
        n = str((datetime.datetime.now().strftime("%y%m%d%H%M%S")) + str(random.randint(0, 99999999999)))
        nl = [x for x in n]
        random.shuffle(nl)
        return "_" + "".join(nl)

class Top(Section):
    def __init__(self, parent, object_name, cfg, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)



class Center(Section):
    def __init__(self, parent, object_name, cfg, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)



class Bottom(Section):
    def __init__(self, parent, object_name, cfg, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

class CardView(QFrame):
    def __init__(self, main, cfg, object_name, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.cfg = cfg
        self.sections = {}
        self.box = customwidgets.BoxLayout(QBoxLayout.TopToBottom, self)
        self._initSections()




    def _initSections(self):
        self.sections["top"] = Top(self, "top", self.cfg)
        self.sections["center"] = Center(self, "center", self.cfg)
        self.sections["bottom"] = Bottom(self, "bottom", self.cfg)
        self.box.addWidget(self.sections["top"], stretch=5)
        self.box.addWidget(self.sections["center"], stretch=5)
        self.box.addWidget(self.sections["bottom"], stretch=5)



class ViewCardStack(QFrame):
    def __init__(self, main, cfg, object_name, name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.contentTeg = dict(Перевод="translation", Word="base", Транскрипция="cyrillicTranscription",
                               Пример="examples")
        self.setObjectName(object_name)
        self.config = cfg
        self.setObjectName(name)
        self.main = main
        self.hbox = customwidgets.BoxLayout(QBoxLayout.LeftToRight, self)
        self.hbox.setContentsMargins(14, 14, 14, 14)
        self.vWorkBox = customwidgets.BoxLayout(QBoxLayout.TopToBottom)
        self.hbox.addLayout(self.vWorkBox)

        self.cardsStack = QStackedWidget()
        self.vWorkBox.addWidget(self.cardsStack)

        self.sides = dict(
            front=CardView(self.main, self.config, "front"),
            back=CardView(self.main, self.config, "back")
        )
        self.sides["back"].setStyleSheet('background: #EFEFEF;')
        self.cardsStack.addWidget(self.sides["front"])
        self.cardsStack.addWidget(self.sides["back"])

    def setItemWord(self, item_word):
        if item_word is None:
            return
        _contents = []
        front = self.config["card"]["content"]["front"]
        for section, content in front.items():
            if content:
                sectionsWidget = self.sides["front"].sections[section]
                contents = [x.split("_") for x in content]
                for _content, widget_type in contents:
                    _contents.append(getattr(item_word, self.contentTeg[_content]))
                    sectionsWidget.setContent(_contents)

    def initCard(self):
        """
        добавить нужные виджеты в секции
        """
        front = self.config["card"]["content"]["front"]
        for section, content in front.items():
            if content:
                sectionsWidget = self.sides["front"].sections[section]
                contents = [x.split("_") for x in content]
                for _content, widget_type in contents:
                    sectionsWidget.setWidget(widget_type)

class CardItem:
    def __init__(self):
        pass






