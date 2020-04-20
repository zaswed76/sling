import fileinput
import glob
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import config
import paths
from core.cardModel import CardModel
from core.dictsequence import DictSeq
from core.dictsmodel import DictsModel
from gui.cardeditorpkg.cardeditor import CardEditView
from gui.centrallframe import CenterStackFrame
from gui.choosedict import ChooseDictStack
from gui.viewcard import ViewCard


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
        self.addAction(
            QAction(QIcon(str(paths.ICONS / "dict.png")), "chooseDict", self))
        self.addAction(
            QAction(QIcon(str(paths.ICONS / "edit.png")), "cardEditView", self))


class ChooseDictStackController:
    def __init__(self, main, parent):
        self.parent = parent
        self.main = main

    def closeChooseDict(self):
        self.main.centerStackFrame.showStack("view")
        self.parent.parentMethod()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.cfg = config.Config(paths.CONFIG)

        self._set_style_sheet(self.cfg["currentStyle"])

        self.dictSeq = DictSeq(paths.DATA)
        # здесь хранятся все стеки (окна)
        self.centerStackFrame = CenterStackFrame(self)
        self.setCentralWidget(self.centerStackFrame)
        self.__setToolBar()
        self.stackWidgets = {}
        self.controls = {}
        self._currentStackWidget = self.cfg["ui"]["currentStackWidget"]

        self.cardCfg = config.Config(paths.CARD_CONFIG)
        self.cardModel = CardModel(self.cardCfg)

        # выбираем словарь
        self.chooseDictStack = ChooseDictStack(self, name="chooseDictStack",
                                               config=self.cfg)
        self.stackWidgets["chooseDict"] = self.chooseDictStack
        self.controls["chooseDictStack"] = ChooseDictStackController(self,
                                                                     self.chooseDictStack)
        # работаем с карточками
        self.viewCardStack = ViewCard(self, self.cfg, "viewStack", "viewCardStack")
        self.viewCardStack.setCardModel(self.cardModel)

        self.stackWidgets["view"] = self.viewCardStack
        # редактируем карточки
        self.cardEditView = CardEditView(self, config=self.cfg, name="cardEditView",
                                         cardModel=self.cardModel)

        self.stackWidgets["cardEditView"] = self.cardEditView

        self.centerStackFrame.setStackWidgets(self.stackWidgets)
        self.centerStackFrame.initStack()
        self.centerStackFrame.showStack(self._currentStackWidget)
        self.centerStackFrame.stack.currentChanged.connect(self.changeStackWidget)

        self.chooseDictStack.setCheckedItemsToNames(
            self.cfg["choosedict"]["checkedDicts"])

        self.dictsModel = DictsModel(self.dictSeq)
        self.dictsModel.updateWorkData(self.chooseDictStack.checkedDicts())
        # self.viewCardStack.initCard()

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
        self._currentStackWidget = self.centerStackFrame.stack.widget(i).objectName()
        self.dictsModel.updateWorkData(self.chooseDictStack.checkedDicts())
        # self.viewCardStack.initCard()

    def toolActions(self, act):
        getattr(self, "{}Action".format(act.text()))()

    def chooseDictAction(self):
        self.centerStackFrame.showStack("chooseDict")

    def cardEditViewAction(self):
        self.centerStackFrame.showStack("cardEditView")

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
        self.cfg.save()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Right:
            self.viewCardStack.setSideIndex(0)
            self.viewCardStack.setItemWord(self.dictsModel.nextItem())
        elif e.key() == Qt.Key_Left:
            pass
            # print(self.cardModel.prevItem())
        elif e.key() == Qt.Key_Space:
            self.viewCardStack.turnSide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
    #
