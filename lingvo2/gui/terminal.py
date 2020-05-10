
#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

def terminalParser(textCommand):
    arg1 = None
    arg2 = None
    prs = textCommand.split(" ")
    command = prs.pop(0)
    if prs:
        arg1 = prs.pop(0)
    if prs:
        arg2 = prs.pop(0)
    return command, arg1, arg2





class TerminalLine(QLineEdit):
    def __init__(self, labelTerminal, controller):
        super().__init__()
        self.labelTerminal = labelTerminal
        self.controller = controller

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() == Qt.Key_Return:
            if self.hasFocus():
                repl = self.text()
                if repl:
                    command = terminalParser(repl)
                    self.labelTerminal.setText(str(command))
                    try:
                        getattr(self.controller, command[0])(*command[1:2])
                    except AttributeError:
                        self.labelTerminal.clear()
                        self.labelTerminal.setText(
                            "нет такой команды\nсправка - help")
                        self.clear()
                    else:
                        self.clear()
        else:
            super().keyPressEvent(qKeyEvent)

class TerminalLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)




class TeminalFrame(QFrame):
    def __init__(self, main, cfg, objectName, controller, *args, **kwargs):
        super().__init__(*args)
        self.box = QVBoxLayout(self)
        self.box.setContentsMargins(0, 0, 0, 0)
        self.box.setSpacing(0)
        self.terminalLabel = TerminalLabel()
        self.controller = controller
        self.controller.returnSignal.connect(self.terminalLabel.setText)


        self.TerminalLine = TerminalLine(self.terminalLabel, self.controller)

        self.box.addWidget(self.TerminalLine)
        self.box.addWidget(self.terminalLabel)
        self.cfg = cfg
        self._helloText = ""
        self.main = main
        self.controller = None
        self.setObjectName(objectName)

    def setController(self, controller):
        self.controller = controller

    def setHelloText(self, text):
        self._helloText = text
        self.setText(self._helloText)



class TerminalController(QObject):
    returnSignal = pyqtSignal(str)
    def __init__(self, main):
        super().__init__()
        self.main = main

    def open(self, *args):
        print("что то делаем")
        self.returnSignal.emit("результат")

    def help(self, *args):
        self.returnSignal.emit("справка по командам")





if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(open('./etc/{0}.qss'.format('style'), "r").read())
    main = TeminalFrame()
    main.show()
    sys.exit(app.exec_())