#!/usr/bin/env python3

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ex.modelex import model, userabc
from ex.modelex.model import NumList

def qt_message_handler(mode, context, message):
    if mode == QtInfoMsg:
        mode = 'INFO'
    elif mode == QtWarningMsg:
        mode = 'WARNING'
    elif mode == QtCriticalMsg:
        mode = 'CRITICAL'
    elif mode == QtFatalMsg:
        mode = 'FATAL'
    else:
        mode = 'DEBUG'
    print('qt_message_handler: line: %d, func: %s(), file: %s' % (
        context.line, context.function, context.file))
    print('  %s: %s\n' % (mode, message))


qInstallMessageHandler(qt_message_handler)

class ViewLeft(QLabel):
    def __init__(self, model, *__args):
        super().__init__(*__args)
        self.model = model
        self.updateContent()
        self.resize(500, 500)
        font = QFont('Helvetica', 24, QFont.Bold)
        self.setFont(font)
        self.setStyleSheet("color: black; background-color: white")

    def updateContent(self):
        self.setText(self.model.num)

class Viewright(QLabel):
    def __init__(self, model, *__args):
        super().__init__(*__args)


        self.model = model
        self.updateContent()

        self.resize(500, 500)
        font = QFont('Helvetica', 24, QFont.Bold)
        self.setFont(font)
        self.setStyleSheet("color: darkred; background-color: grey")
        self.setAlignment(Qt.AlignRight | Qt.AlignCenter)

    def updateContent(self):
        self.setText(self.model.reversenum)

class Main(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize(500, 500)
        self.box = QHBoxLayout(self)
        self.model = model.Model()
        self.model.updateSignal.connect(self.updateViews)

        self.leftView = ViewLeft(self.model)
        self.rightView = Viewright(self.model)

        self.box.addWidget(self.leftView, stretch=5)
        self.box.addWidget(self.rightView, stretch=5)
        vbox = QVBoxLayout()
        self.box.addLayout(vbox, stretch=2)
        self.plusBtn = QPushButton("+")

        self.minusBtn = QPushButton("-")
        self.loadBtn = QPushButton("load")
        self.saveBtn = QPushButton("save")

        self.plusBtn.clicked.connect(self.model.numplus)
        self.minusBtn.clicked.connect(self.model.numminus)
        self.loadBtn.clicked.connect(self.model.load)
        self.saveBtn.clicked.connect(self.model.save)

        vbox.addWidget(self.plusBtn)
        vbox.addWidget(self.minusBtn)
        vbox.addStretch(5)
        vbox.addWidget(self.loadBtn)
        vbox.addWidget(self.saveBtn)

    def updateViews(self):
        self.leftView.updateContent()
        self.rightView.updateContent()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())