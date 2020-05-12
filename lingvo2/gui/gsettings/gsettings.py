#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import paths
from gui.custom.customwidgets import *



class Gsettings(QFrame):
    def __init__(self, cfg, main, objectName):
        super().__init__()
        self.setObjectName(objectName)
        self.main = main
        self.cfg = cfg
        self.box = QHBoxLayout(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(open('./etc/{0}.qss'.format('style'), "r").read())
    main = Gsettings()
    main.show()
    sys.exit(app.exec_())