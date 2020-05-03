# !/usr/bin/env python3

import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import resources
from tools.handler import qt_message_handler

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
        self.visibleFlag = False
        self._stext = ""
        self.setAlignment(Qt.AlignTop | Qt.AlignLeft)

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

    # def resizeEvent(self, *args, **kwargs):
    #     rect = self.parent().rect()
    #     # self.setMinimumWidth(500)


class SpoilerBaseLabel(QLabel):
    clicked = pyqtSignal()
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setCursor(QCursor(Qt.PointingHandCursor))

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
        self.spoilerLabel.setParent(self)

        self.spBtn = spoilerBtn
        self.spBtn.setParent(self)
        self.spBtn.clicked.connect(self.runSpoiler)

    def resizeEvent(self, e):
        rect = self.baseLabel.rect()
        self.spBtn.move(rect.bottomLeft() + QPoint(self.indentlrftArrow, self.indenttopArrow))
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

