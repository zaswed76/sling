import fileinput
import glob
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import config
import paths
from core.cardModel import CardModel, PConfig, DropBox, DropItem, DragItemStyle
from core.dictsequence import DictSeq
from core.dictsmodel import DictsModel
from gui.custom.abccard import AbcViewCard
from gui.centrallframe import CenterStackFrame
from gui.choosedict import ChooseDictStack

from gui.editcard import editcard, editcardWidget, editdrop_listview
from gui.viewcard import viewcard



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
            QAction(QIcon(":/dict.png"), "chooseDict", self))
        self.addAction(
            QAction(QIcon(":/edit.png"), "cardEditView", self))


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
        self.setFixedSize(790, 830)
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

        # загружаем модель

        self.cardModel = CardModel(paths.PICKLE_CONFIG)
        self.cardModel.updateSignal.connect(self.updateViews)



        # выбираем словарь
        self.chooseDict = ChooseDictStack(self, name="chooseDictStack",
                                          config=self.cfg)
        self.controls["chooseDictStack"] = ChooseDictStackController(self,
                                                                     self.chooseDict)

        self.dictsModel = DictsModel(self.dictSeq)
        self.dictsModel.updateWorkData(self.chooseDict.checkedDicts())

        # работаем с карточками
        self.viewCard = viewcard.ViewCard()
        self.viewCard.setCardModel(self.cardModel)


        # редактируем карточки
        self.editDropList = editdrop_listview.DropListWidget(None, "editDropList")
        self.editDropList.setItems(config.Config(paths.CARD_CONFIG)["dropItemsTypeList"])
        self.viewEditCard = editcard.EditCard()
        self.viewEditCard.setCardModel(self.cardModel)
        # self.viewEditCard.setC
        self.viewCardEditWidget = editcardWidget.EditCardWidget(self.editDropList, self.viewEditCard)










        self.stackWidgets["view"] = self.viewCard
        self.stackWidgets["chooseDict"] = self.chooseDict
        self.stackWidgets["cardEditView"] = self.viewCardEditWidget

        self.centerStackFrame.setStackWidgets(self.stackWidgets)
        self.centerStackFrame.showStack(self._currentStackWidget)
        self.centerStackFrame.stack.currentChanged.connect(self.changeStackWidget)

        self.chooseDict.setCheckedItemsToNames(
            self.cfg["choosedict"]["checkedDicts"])



    def updateViews(self):
        self.viewCardEditWidget.updateContent()
        self.viewCard.updateContent()


    def getCardModel(self) -> CardModel:
        return self.cfgpObject.load()


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
        self.dictsModel.updateWorkData(self.chooseDict.checkedDicts())


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
        self.cardModel.saveContent()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Right:
            self.viewCard.setSideIndex(0)
            self.viewCard.setItemWord(self.dictsModel.nextItem())
        elif e.key() == Qt.Key_Left:
            pass
            # print(self.cardModel.prevItem())
        elif e.key() == Qt.Key_Space:
            self.viewCard.turnSide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
    #
