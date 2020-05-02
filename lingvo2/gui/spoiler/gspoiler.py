
#!/usr/bin/env python3

import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from tools.handler import qt_message_handler
qInstallMessageHandler(qt_message_handler)



class Widget(QPushButton):
    def __init__(self):
        super().__init__()
        self.resize(500, 500)
        self.box = QHBoxLayout(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(open('./etc/{0}.qss'.format('style'), "r").read())
    main = Widget()
    main.show()
    sys.exit(app.exec_())