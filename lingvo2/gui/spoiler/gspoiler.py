# !/usr/bin/env python3

import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import resources
from tools.handler import qt_message_handler

qInstallMessageHandler(qt_message_handler)

class QSpoilerBtn(QPushButton):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setCheckable(True)

class SpoilerLabel(QLabel):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.visibleFlag = False
        self._stext = ""


    def setSpoilerText(self, p_str):
        self._stext = p_str

    def changeVisible(self):
        self.visibleFlag = not self.visibleFlag

        if self.visibleFlag:
            self.setText(self._stext)
        else:
            self.setText("")


class BaseLabel(QLabel):
    clicked = pyqtSignal()
    def __init__(self, *__args):
        super().__init__(*__args)

    def mousePressEvent(self, QMouseEvent):
        self.clicked.emit()



class SpoilerWidget(QFrame):
    def __init__(self, baseLabel=None, spoiLerLabel=None, spacing=6, spoilerIndent=35, indentArrow=11):
        """

        :param baseLabel: базовая верхняя надпись inherit spoiler.BaseLabel
        :param spoiLerLabel: сполйлер inherit spoiler.SpoilerLabel
        :param spacing: int расстояние между базовой надписью и спойлером
        :param spoilerIndent: отступ спойлера от левого края
        :param indentArrow: отступ стрелки от верхней надписи
        """
        super().__init__()
        self.indentArrow = indentArrow
        self.box = QVBoxLayout(self)
        self.box.setContentsMargins(0, 0, 0, 0)
        self.box.setSpacing(spacing)

        self.baseLabel = BaseLabel() if baseLabel is None else baseLabel

        self.baseLabel.clicked.connect(self.runSpoiler)
        self.box.addWidget(self.baseLabel , alignment=Qt.AlignLeft | Qt.AlignTop)

        self.spoilerLabel = SpoilerLabel() if spoiLerLabel is None else spoiLerLabel

        self.box.addWidget(self.spoilerLabel, alignment=Qt.AlignLeft | Qt.AlignTop)
        self.box.addStretch(1)

        self.spBtn = QSpoilerBtn(self)
        self.spBtn.clicked.connect(self.runSpoiler)


        self.setSpoilerIndent(spoilerIndent)
        self.setStyleSheet(open("spoiler.css", "r").read())

    def resizeEvent(self, e):
        rect = self.baseLabel.rect()

        self.spBtn.move(rect.bottomLeft() - QPoint(0, -self.indentArrow))

    def setSpacing(self, p_int):
        self.box.setSpacing(p_int)

    def setSpoilerIndent(self, p_int):
        self.spoilerLabel.setIndent(p_int)

    def runSpoiler(self):
        self.spoilerLabel.changeVisible()

    def setText(self, text):
        self.baseLabel.setText(text)

    def setSpoilerText(self, text):
        self.spoilerLabel.setSpoilerText(text)







if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QFrame()
    box = QVBoxLayout(main)

    spoilerWidget = SpoilerWidget()

    box.addWidget(spoilerWidget)

    spoilerWidget.setText("это пример")
    spoilerWidget.setSpoilerText("это спойлер")
    main.show()
    sys.exit(app.exec_())
