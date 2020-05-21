
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from gui.custom.controller import AbcController




class GsettingsGeometryController(AbcController):
    def __init__(self, main, parent):
        super().__init__(main, parent)

    def tratata(self):
        print("tratata")


class GDictController(AbcController):
    def __init__(self, main, parent):
        super().__init__(main, parent)

    def bumcaca(self):
        print("GDictController - bumcaca")