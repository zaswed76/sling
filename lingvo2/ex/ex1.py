



#!/usr/bin/env python3

import sys
import textwrap

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *








class Widget(QLabel):
    def __init__(self):
        super().__init__()
        self.setFixedSize(500, 300)
        # self.setWordWrap(True)
        self.setIndent(8)

    @staticmethod
    def fontDiapason(key):
        return {-1 < key < 101: 18, 100 < key < 201: 16, 200 < key < 100000: 14}[1]

    def wrapText(self, text):
        size = Widget.fontDiapason(len(text))
        content = "<br/>".join(textwrap.wrap(text, width=50))
        # return content
        return """< p style = "font-size:{size}pt" > {text} < / p >""".format(text=content, size=size)

    def setText(self, p_str):
        super().setText(self.wrapText(p_str))



if __name__ == '__main__':
    s = """ rherthhhhhhhhh hhhhhhhh retttttttt tttttttttttttt rtgheerrrrrrrrrrrrrrrrrrrrrrrrrrrrr tttttttfeatures in PyCharm along with how to get started with data science
    """
    app = QApplication(sys.argv)

    main = Widget()
    main.setText(s)

    main.show()
    sys.exit(app.exec_())