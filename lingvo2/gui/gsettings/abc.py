from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class AbcGSettingsFrame(QFrame):
    def __init__(self, main, cfg, textName, obgectName, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName(obgectName)
        self.textName = textName
        self.cfg = cfg
        self.main = main