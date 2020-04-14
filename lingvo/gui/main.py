import fileinput
import glob
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from gui.choosedict import ChooseDictStack
from gui.view import ViewStack
from gui.cardeditor import CardEditView

import paths
from core.dictsequence import DictSeq
from gui.centrallframe import CenterFrame


def fileInput(folder):
    files_list = glob.glob(folder + "/*.css")
    ls = []
    with fileinput.input(files=files_list) as f:
        for line in f:
            ls.append(line)
    return "".join(ls)



class ToolBar(QToolBar):
    def __init__(self, main, *__args):
        super().__init__(*__args)
        self.main = main
        self.setFixedHeight(42)
        self.addAction(QAction(QIcon(str(paths.ICONS / "dict.png")), "chooseDict", self))
        self.addAction(QAction(QIcon(str(paths.ICONS / "edit.png")), "cardEditView", self))

class ChooseDictStackController:
    def __init__(self, main, parent):
        self.parent = parent
        self.main = main

    def closeChooseDict(self):
        self.main.centerFrame.showStack("view")
        self.parent.parentMethod()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self._set_style_sheet("base")
        self.dictSeq = DictSeq(paths.DATA)

        self.centerFrame = CenterFrame(self)
        self.setCentralWidget(self.centerFrame)
        self.__setToolBar()
        self.stackWidgets = {}
        self.controls = {}

        self.chooseDictStack = ChooseDictStack(self)
        self.stackWidgets["chooseDict"] = self.chooseDictStack
        self.chooseDictStack.setObjectName("ChooseDictStack")
        self.controls["ChooseDictStack"] = ChooseDictStackController(self, self.chooseDictStack)

        self.viewStack = ViewStack(self)
        self.stackWidgets["view"] = self.viewStack

        self.cardEditView = CardEditView(self)

        self.stackWidgets["cardEditView"] = self.cardEditView

        self.centerFrame.setStackWidgets(self.stackWidgets)
        self.centerFrame.initStack()
        self.centerFrame.showStack("view")






    def connect(self):
        controll = self.sender()
        slot = controll.objectName()
        object = self.controls[controll.parent().objectName()]
        getattr(object, slot)()

    def __setToolBar(self):
        self.toolBar = ToolBar(self)
        self.addToolBar(Qt.TopToolBarArea, self.toolBar)
        self.toolBar.actionTriggered.connect(self.toolActions)

    def toolActions(self, act):
        getattr(self, "{}Action".format(act.text()))()

    def chooseDictAction(self):
        self.centerFrame.showStack("chooseDict")

    def cardEditViewAction(self):
        self.centerFrame.showStack("cardEditView")

    @property
    def dictList(self):
        return self.dictSeq.dictNames()

    def _set_style_sheet(self, sheetName):
        """
        :param sheetName: str имя стиля
        """
        styleSheet = fileInput(str(paths.CSS / sheetName))
        QApplication.instance().setStyleSheet(styleSheet)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())