#!/usr/bin/env python3

import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *



class AbcDialog(QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlag(Qt.Tool)

class ToolTypeFrame(QFrame):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName(name)
        self.setToolTip("{}".format(self.__class__))


class BoxLayout(QBoxLayout):
    def __init__(self, direction, parent=None, **kwargs):
        super().__init__(direction, parent)
        self.setDirection(direction)
        self.setParent(parent)
        contentMargin = kwargs.get("content_margin", (0, 0, 0, 0))
        spacing = kwargs.get("spacing", 0)
        print(spacing, "WWWWWWWWWWWWWWWWWW")
        self.setContentsMargins(*contentMargin)
        self.setSpacing(spacing)






if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(open('./etc/{0}.qss'.format('style'), "r").read())
    main = ChangeSideCardBtn()
    main.show()
    sys.exit(app.exec_())