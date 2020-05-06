



#!/usr/bin/env python3

import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *








class Widget(QLabel):
    def __init__(self):
        super().__init__()

        self.setWordWrap(True)

    @staticmethod
    def fontDiapason(key):
        return {-1 < key < 101: 16, 100 < key < 201: 14, 200 < key < 100000: 12}[1]

    def wrapText(self, text):
        size = Widget.fontDiapason(len(text))
        print(size)
        return """< p style = "font-size:{size}pt" > {text} < / p >""".format(text=text, size=size)

    def setText(self, p_str):
        super().setText(self.wrapText(p_str))



if __name__ == '__main__':
    s = """ rherthhhhhhhhhhhhhhhhhretttttttttttttttttttttttttttttfeatures in PyCharm along with how to get started with data science
    """
    app = QApplication(sys.argv)

    main = Widget()
    main.setText(s)

    main.show()
    sys.exit(app.exec_())