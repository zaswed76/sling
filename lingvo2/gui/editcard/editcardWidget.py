#!/usr/bin/env python3

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from functools import partial

class ChangeSideCardBtn(QPushButton):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setFont(QFont("arial", 20))


class EditCardWidget(QFrame):
    def __init__(self, editDropList, viewCard, objectName,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName(objectName)
        self.box_0 = QHBoxLayout(self)
        self.box_0.setContentsMargins(0, 0, 0, 0)
        self.box_0.setSpacing(0)
        self.box_0.addWidget(editDropList)
        self.box_0.addSpacing(20)

        self.box_right = QVBoxLayout()

        self.box_right.setContentsMargins(0, 0, 0, 0)
        self.box_right.setSpacing(0)
        self.turnSideBtn = ChangeSideCardBtn(viewCard.currentSideName)
        self.turnSideBtn.clicked.connect(partial(self.changeSide, viewCard))

        self.box_right.addWidget(self.turnSideBtn)
        self.box_right.addWidget(viewCard)


        self.box_0.addLayout(self.box_right)
        self.box_0.addStretch(1)



    def changeSide(self, viewCard):
        side = viewCard.changeSide()
        self.turnSideBtn.setText(side)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = EditCardWidget()
    main.show()
    sys.exit(app.exec_())