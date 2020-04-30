import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from gui.custom.customwidgets import *


class LoadSoundsDialog(AbcDialog):
    def __init__(self):
        super().__init__()




class ControlBtn(QPushButton):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setCursor(QCursor(Qt.PointingHandCursor))


class ChooseDictControls(QFrame):
    def __init__(self, main, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.box = BoxLayout(QBoxLayout.TopToBottom, self)

        self.loadSoundsBtn = ControlBtn()
        self.setObjectName("chooseDictStack")
        self.loadSoundsBtn.clicked.connect(main.connect)
        self.loadSoundsBtn.setObjectName("loadSoundsBtn")

        self.box.addWidget(self.loadSoundsBtn)
        self.box.addStretch(10)