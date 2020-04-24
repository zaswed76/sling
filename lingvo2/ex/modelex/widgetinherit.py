#!/usr/bin/env python3

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ex.modelex import model, userabc




class Label(QLabel):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setAlignment(Qt.AlignCenter)
        font = QFont('Helvetica', 44, QFont.Bold)
        self.setFont(font)
        # self.setStyleSheet("background-color: cyan")

class Line(QLineEdit):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setFixedHeight(70)




if __name__ == '__main__':
    import paths
    app = QApplication(sys.argv)
    # app.setStyleSheet(open('./etc/{0}.qss'.format('style'), "r").read())
    main = DropWidgetItem(Label, "word")
    main.show()
    sys.exit(app.exec_())