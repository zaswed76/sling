# !/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import paths


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
        self.setFocusPolicy(Qt.StrongFocus)

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
        self.setTextInteractionFlags(
            Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)
        self.setIndent(4)


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
        self.lsdict = dict(dict="\n".join(self.main.dictSeq.dictNames()))

    def opendir(self, *args):
        if args:
            res = OpenPath(args[0]).open()

        self.returnSignal.emit(str(res))

    def help(self, *args):
        self.returnSignal.emit("справка по командам")

    def opendict(self, *args):
        if args:
            dct = self.main.dictSeq.get(" ".join(args))
            if dct:
                path = dct.dictpath
                os.startfile(path)
                self.returnSignal.emit(path)
            else:
                return "не удалось открыть словарь"
        else:
            return "не удалось открыть словарь"

    def ls(self, *args):
        if args:
            self.returnSignal.emit(self.lsdict[args[0]])


class OpenPath:
    Paths = {
        "data": paths.DICTIONARIES,
        "resources": paths.RESOURCES
    }

    def __init__(self, p_arg):
        self.p_arg = p_arg

    def open(self) -> str:
        if not self.p_arg:
            return "не удалось открыть путь"
        path = OpenPath.Paths.get(self.p_arg)
        if path:
            return self._open(path)
        else:
            path = Path(self.p_arg)
            if path.is_dir():
                return self._open(path)
            else:
                return "не удалось открыть путь"

    def _open(self, _p):
        subprocess.Popen('explorer {}'.format(_p))
        return _p


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(open('./etc/{0}.qss'.format('style'), "r").read())
    main = TeminalFrame()
    main.show()
    sys.exit(app.exec_())
