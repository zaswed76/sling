#!/usr/bin/env python3

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *



class EditCardWidget(QFrame):
    def __init__(self, editDropList, viewCard, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.box_0 = QHBoxLayout(self)
        self.box_0.setContentsMargins(0, 0, 0, 0)
        self.box_0.setSpacing(0)
        self.box_0.addWidget(editDropList)
        self.box_0.addStretch(1)

        self.box_right = QVBoxLayout()

        self.box_right.setContentsMargins(0, 0, 0, 0)
        self.box_right.setSpacing(0)
        self.turnSideBtn = QPushButton("Turn")
        self.turnSideBtn.clicked.connect(viewCard.changeSide)

        self.box_right.addWidget(self.turnSideBtn)
        self.box_right.addWidget(viewCard)

        self.box_0.addLayout(self.box_right)
        self.box_0.addStretch(1)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = EditCardWidget()
    main.show()
    sys.exit(app.exec_())