#!/usr/bin/env python3

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *



class Profiles(QFrame):
    def __init__(self, main, objectName=None, config=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cfg = config
        self.setObjectName(objectName)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(open('./etc/{0}.qss'.format('style'), "r").read())
    main = Profiles()
    main.show()
    sys.exit(app.exec_())