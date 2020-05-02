#!/usr/bin/env python3

import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from libs.Spoiler import Spoiler

def fun(spoiler):
    print("!!!!!!!!!!!!")
    if spoiler.isOpened():
        spoiler.close()
    else:
        spoiler.open()

class Main(QFrame):
    def __init__(self):
        super().__init__()
        self.spoilerLb = QLabel("это спойлер")
        self.spoilerLb.setAlignment(Qt.AlignCenter)
        self.spoilerLayout = QHBoxLayout()
        self.spoilerLayout.addWidget(self.spoilerLb)

        self.spoiler = Spoiler(Spoiler.Orientation.VERTICAL)
        self.spoiler.setContentLayout(self.spoilerLayout)

        self.setFixedSize(500, 500)
        self.box = QHBoxLayout(self)
        self.btn = QPushButton()
        self.btn.clicked.connect(lambda: fun(self.spoiler))
        self.btn.setFixedWidth(42)

        self.box.addWidget(self.btn)
        self.box.addWidget(self.spoiler)




if __name__ == '__main__':
    import paths
    app = QApplication(sys.argv)
    stylepath = paths.CSS / "base/spoiler.css"
    app.setStyleSheet(open(stylepath, "r").read())
    main = Main()
    main.show()
    sys.exit(app.exec_())