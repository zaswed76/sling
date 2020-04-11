import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import paths
from gui.custom.customwidgets import *

class ChooseDictFrame(QFrame):
    def __init__(self, main, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ControlFrame(QFrame):
    def __init__(self, main, *args, **kwargs):
        super().__init__(*args, **kwargs)

class TextFrame(QFrame):
    def __init__(self, main, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ChooseDictStack(QFrame):
    def __init__(self, main, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(600, 600)
        self.main = main
        self.box = BoxLayout(QBoxLayout.LeftToRight, self)
        self.chooseDictFrame = ChooseDictFrame(self.main)
        self.controlFrame = ControlFrame(self.main)
        self.textFrame = TextFrame(self.main)
        self.box.addWidget(self.chooseDictFrame, stretch=10)
        self.box.addWidget(self.controlFrame, stretch=2)
        self.box.addWidget(self.textFrame, stretch=20)




