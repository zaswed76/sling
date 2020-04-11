import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import paths







class CenterFrame(QFrame):
    def __init__(self, main):
        super().__init__()
        self.stackWidgets = {}
        self.main = main
        self.hbox = QHBoxLayout(self)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.stack = QStackedWidget()
        self.hbox.addWidget(self.stack, alignment=Qt.AlignCenter)




    def setStackWidgets(self, stackWidgets):
        self.stackWidgets.update(stackWidgets)

    def initStack(self):
        for w in self.stackWidgets.values():
            self.stack.addWidget(w)


    def showStack(self, window):
        self.stack.setCurrentWidget(self.stackWidgets[window])