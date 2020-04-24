from gui.custom.abccard import *
from gui.custom.customwidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class ControlsDropLabel(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.box = AbcBoxLayout(QBoxLayout.LeftToRight, parent=self)
        self.closeDropLabelBtn = CloseDropLabelBtn(self)
        self.tuneDropLabelBtn = TuneDropLabelBtn(self)
        self.box.addWidgets([self.closeDropLabelBtn, self.tuneDropLabelBtn])


class CloseDropLabelBtn(QPushButton):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setIcon(QIcon("./resources/icons/base/closeComponent.png"))

class TuneDropLabelBtn(QPushButton):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setIcon(QIcon("./resources/icons/base/icon_cog.png"))




class DropLabel(AbcDropLabel):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setObjectName(self.text())
        self.controlsDropLabel = ControlsDropLabel(self)
        self.controlsDropLabel.closeDropLabelBtn.clicked.connect(self.removeComponent)
        self.controlsDropLabel.tuneDropLabelBtn.clicked.connect(self.tuneComponent)
        self.controlsDropLabel.hide()
        self.installEventFilter(self)


    def eventFilter(self, obj, event):
        if event.type() == 11:  # Если мышь покинула область фиджета
            self.controlsDropLabel.hide()  # выполнить  callback1()
        elif event.type() == 10:# Если мышь над виджетом
            self.controlsDropLabel.show()  # выполнить  callback2()
        return False

    def removeComponent(self):
        conteiner = self.sender().parent().parent().parent()
        widget = self.sender().parent().parent()
        idWidget = id(widget)
        conteiner.removeComponent(idWidget)


    def tuneComponent(self):
        conteiner = self.sender().parent().parent().parent()
        widget = self.sender().parent().parent()
        idWidget = id(widget)
        print(conteiner, idWidget, widget, sep=" - ")