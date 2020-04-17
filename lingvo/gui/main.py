import fileinput
import glob
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from gui.choosedict import ChooseDictStack
from gui.viewcard import ViewCardStack
from gui.cardeditor import CardEditView

import paths
from core.dictsequence import DictSeq
from core.cardsmodel import CardsModel
from gui.centrallframe import CenterFrame
import config


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
        self.cfg = config.Config(paths.CONFIG)
        self._set_style_sheet("base")

        self.dictSeq = DictSeq(paths.DATA)

        self.centerFrame = CenterFrame(self)
        self.setCentralWidget(self.centerFrame)
        self.__setToolBar()
        self.stackWidgets = {}
        self.controls = {}
        self._currentStackWidget = self.cfg["ui"]["currentStackWidget"]

        self.chooseDictStack = ChooseDictStack(self, name="chooseDictStack")
        self.stackWidgets["chooseDict"] = self.chooseDictStack
        self.controls["chooseDictStack"] = ChooseDictStackController(self, self.chooseDictStack)

        self.viewCardStack = ViewCardStack(self, "viewStack", "viewCardStack")
        self.stackWidgets["view"] = self.viewCardStack

        self.cardEditView = CardEditView(self, config=self.cfg, name="cardEditView")

        self.stackWidgets["cardEditView"] = self.cardEditView

        self.centerFrame.setStackWidgets(self.stackWidgets)
        self.centerFrame.initStack()
        self.centerFrame.showStack(self._currentStackWidget)
        self.centerFrame.stack.currentChanged.connect(self.changeStackWidget)

        selectedDicts = self.chooseDictStack.selectedDicts()
        print(selectedDicts)
        self.cardModel = CardsModel(self.dictSeq)

    def connect(self):
        controll = self.sender()
        slot = controll.objectName()
        object = self.controls[controll.parent().objectName()]
        getattr(object, slot)()

    def __setToolBar(self):
        self.toolBar = ToolBar(self)
        self.addToolBar(Qt.TopToolBarArea, self.toolBar)
        self.toolBar.actionTriggered.connect(self.toolActions)

    def changeStackWidget(self, i):
        if self._currentStackWidget == "cardEditView":
            self.cfg.save()
        self._currentStackWidget = self.centerFrame.stack.widget(i).objectName()

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

    def closeEvent(self, *args, **kwargs):
        print("555")
        self.cfg.save()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
