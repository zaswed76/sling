

#!/usr/bin/env python3

import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

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

from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QHBoxLayout, QListWidgetItem
from PyQt5.QtGui import QIcon
import sys


class Elements(QListWidget):
    def __init__(self):
        super().__init__()
        # self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setFixedSize(250, 500)
        self.l1 = QListWidgetItem("Word")
        self.l1.setFont(QFont("Arial", 24))
        self.l1.setTextAlignment(Qt.AlignCenter)
        self.l2 = QListWidgetItem("Перевод")

        self.l2.setFont(QFont("Arial", 24))
        self.l2.setTextAlignment(Qt.AlignCenter)

        self.l3 = QListWidgetItem("транскрипция")
        self.l4 = QListWidgetItem("пример")

        self.insertItem(0, self.l1)
        self.insertItem(1, self.l2)



class Editor(QListWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(500, 500)

class CardEdit(QFrame):
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.box = QHBoxLayout(self)
        self.elements = Elements()
        self.editor = Editor()
        self.box.addWidget(self.elements, stretch=1)
        self.box.addWidget(self.editor, stretch=4)






if __name__ == '__main__':
    App = QApplication(sys.argv)
    App.setStyleSheet(open(r"D:\user\projects\sling\lingvo\css\base\cardeditor.css", "r").read())
    window = CardEdit()
    window.show()
    sys.exit(App.exec_())



