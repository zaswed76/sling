from gui.custom.abccard import *
from gui.custom.customwidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *











class DropLabel(AbcDropLabel):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setObjectName(self.text())








