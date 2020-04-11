
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import paths

class ViewStack(QFrame):
    def __init__(self, main, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(600, 600)
        self.main = main
        self.btnClose = QPushButton("view", self)