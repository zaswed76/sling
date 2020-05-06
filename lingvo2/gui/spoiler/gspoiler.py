# !/usr/bin/env python3

import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import resources
from tools.handler import qt_message_handler
import textwrap
qInstallMessageHandler(qt_message_handler)

class SpoilerBtn(QPushButton):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setCheckable(True)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setFocusPolicy(Qt.NoFocus)

    # def keyPressEvent(self, QKeyEvent):
    #     self.

class SpoilerLabel(QLabel):
    def __init__(self, *__args):
        super().__init__(*__args)
        self._textWidth = 90
        self.minFont = 12
        self.visibleFlag = False
        self._stext = ""
        self.setAlignment(Qt.AlignTop | Qt.AlignLeft)

    def wrapText(self, text):
        size = SpoilerBaseLabel.fontDiapason(len(text))
        content = "<br/>".join(textwrap.wrap(text, width=self.textWidth))
        return """< p style = "font-size:{size}pt" > {text} < / p >""".format(text=content, size=size)

    @property
    def textWidth(self):
        return self._textWidth

    @textWidth.setter
    def textWidth(self, w):
        self._textWidth = w

    def clear(self):
        self._stext = ""
        self.setText(self._stext)

    def text(self):
        return self._stext

    def setSpoilerText(self, p_str):
        self._stext = p_str

    def changeVisible(self):
        self.visibleFlag = not self.visibleFlag

        if self.visibleFlag:
            self.setText(self._stext)
        else:
            self.setText("")

    def fontDiapason(self, key):
        small = self.minFont
        medium = self.minFont + 2
        big = self.minFont + 4
        return {-1 < key < 101: big, 100 < key < 201: medium, 200 < key < 100000: small}[1]

    def wrapText(self, text):
        size = self.fontDiapason(len(text))
        content = "<br/>".join(textwrap.wrap(text, width=self.textWidth))
        return """< p style = "font-size:{size}pt" > {text} < / p >""".format(text=content, size=size)

    def setText(self, p_str):
        super().setText(self.wrapText(p_str))


class SpoilerBaseLabel(QLabel):
    clicked = pyqtSignal()
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self._textWidth = 90
        self.minFont = 10


    @property
    def textWidth(self):
        return self._textWidth

    @textWidth.setter
    def textWidth(self, w):
        # print(w, "pppppppppppppp")
        self._textWidth = w


    def fontDiapason(self, key):
        small = self.minFont
        medium = self.minFont + 2
        big = self.minFont + 4
        return {-1 < key < 101: big, 100 < key < 201: medium, 200 < key < 100000: small}[1]

    def wrapText(self, text):

        size = self.fontDiapason(len(text))
        content = "<br/>".join(textwrap.wrap(text, width=self.textWidth))
        return """< p style = "font-size:{size}pt" > {text} < / p >""".format(text=content, size=size)

    def setText(self, p_str):
        super().setText(self.wrapText(p_str))

    def mousePressEvent(self, QMouseEvent):
        self.clicked.emit()



class SpoilerWidget(QFrame):
    def __init__(self, baseLabel=None, spoiLerLabel=None,
                 spoilerBtn=None,
                 spoilerLeftIndent=45, spoilertopIndent=1,
                 indenttopArrow=8, indentlrftArrow=10,):
        """
        :param baseLabel: базовая верхняя надпись inherit spoiler.BaseLabel
        :param spoiLerLabel: сполйлер inherit spoiler.SpoilerLabel
        :param spoilerLeftIndent: отступ спойлера от левого края
        :param spoilertopIndent: отступ спойлера от надписи
        :param indenttopArrow: отступ стрелки от верхней надписи
        """
        super().__init__()
        self.indentlrftArrow = indentlrftArrow
        self.spoilertopIndent = spoilertopIndent
        self.spoilerIndent = spoilerLeftIndent
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setSizePolicy(sizePolicy)
        self.indenttopArrow = indenttopArrow
        self.box = QVBoxLayout(self)
        self.box.setContentsMargins(0, 0, 0, 0)


        self.baseLabel = baseLabel

        self.baseLabel.setParent(self)

        self.baseLabel.clicked.connect(self.runSpoiler)
        self.box.addWidget(self.baseLabel , alignment=Qt.AlignLeft | Qt.AlignTop)

        self.spoilerLabel = spoiLerLabel
        # self.spoilerLabel = spoiLerLabel
        self.spoilerLabel.setParent(self)

        self.spBtn = spoilerBtn
        self.spBtn.setParent(self)
        self.spBtn.clicked.connect(self.runSpoiler)

    def resizeEvent(self, e):

        rect = self.baseLabel.rect()
        s = int(rect.width() / 5.5)
        # self.baseLabel.textWidth = s
        p = QPoint(self.indentlrftArrow, self.indenttopArrow)
        # print(rect, p, self.indenttopArrow)
        # print("-------------------")
        self.spBtn.move(rect.bottomLeft() + p)
        self.spoilerLabel.move(rect.bottomLeft() + QPoint(self.spoilerIndent, self.spoilertopIndent ))

    def setSpacing(self, p_int):
        self.box.setSpacing(p_int)

    def setSpoilerIndent(self, p_int):
        self.spoilerLabel.setIndent(p_int)

    def runSpoiler(self):
        self.spoilerLabel.changeVisible()
        self.spBtn.setChecked(self.spoilerLabel.visibleFlag)

    def hideSpoiler(self):
        self.spoilerLabel.setText("")
        self.spoilerLabel.visibleFlag = False
        self.spBtn.setChecked(False)

    def setText(self, text):
        self.baseLabel.setText(text)

    def setSpoilerText(self, text):
        self.spoilerLabel.setSpoilerText(text)

    def text(self):
        return self.baseLabel.text()

    def spoilerText(self):
        return self.spoilerLabel.text()

    def clear(self):

        self.baseLabel.clear()
        self.spoilerLabel.clear()






if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QFrame()
    main.resize(300, 200)
    box = QVBoxLayout(main)

    btn = SpoilerBtn()
    base = SpoilerBaseLabel()
    spoiler = SpoilerLabel()
    spoilerWidget = SpoilerWidget(baseLabel=base, spoiLerLabel=spoiler, spoilerBtn=btn, indenttopArrow=4)


    box.addWidget(spoilerWidget)

    spoilerWidget.setText("это пример")
    spoilerWidget.setSpoilerText("это спойлер")
    app.setStyleSheet(open("./spoiler.css", "r").read())
    main.show()
    sys.exit(app.exec_())

