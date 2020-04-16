
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import paths

class ViewStack(QFrame):
    def __init__(self, main, name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName(name)
        self.main = main
        self.btnClose = QPushButton("view", self)
