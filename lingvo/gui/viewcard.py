
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import paths
from gui.cardeditor import CardModelView
from gui.custom import customwidgets

class Section(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        shadow = QGraphicsDropShadowEffect(blurRadius=12, xOffset=3, yOffset=3)
        self.setGraphicsEffect(shadow)


class Top(Section):
    def __init__(self, parent, object_name, cfg, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)



class Center(Section):
    def __init__(self, parent, object_name, cfg, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)



class Bottom(Section):
    def __init__(self, parent, object_name, cfg, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

class CardView(CardModelView):
    def __init__(self, main, cfg, object_name):
        super().__init__(main, cfg, object_name)

    def _initSections(self):
        pass
        self.t = Top(self, "top", self.cfg)
        self.c = Center(self, "center", self.cfg)
        self.b = Bottom(self, "bottom", self.cfg)
        self.box.addWidget(self.t, stretch=5)
        self.box.addWidget(self.c, stretch=5)
        self.box.addWidget(self.b, stretch=5)



class ViewCardStack(QFrame):
    def __init__(self, main, cfg, object_name, name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
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


