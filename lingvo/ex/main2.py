import fileinput
import glob
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from tools.handler import qt_message_handler

qInstallMessageHandler(qt_message_handler)
import config
import paths
from core.cardModel import CardModel
from core.dictsequence import DictSeq
from core.dictsmodel import DictsModel
from core.soundloader import SoundLoader

from gui.centrallframe import CenterStackFrame
from gui.choosedicts.choosedict import ChooseDictStack
from gui.choosedicts.choosedict import *

from gui.editcard import editcard, editcardWidget, editdrop_listview
from gui.viewcard import viewcard

def warningMessage(parent, nameDict):
    message = """словарь - {} уже содержит каталог с аудиофайлами.
если проодолжить то ваши файлы могут быть удалены""".format(nameDict)
    msgBox = QMessageBox(QMessageBox.Warning, "QMessageBox.warning()",
            message, QMessageBox.NoButton, None)
    msgBox.addButton("продолжить", QMessageBox.AcceptRole)
    msgBox.addButton("отменить", QMessageBox.RejectRole)
    if msgBox.exec_() == QMessageBox.AcceptRole:
        return True
    else:
        return False






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
            QAction(QIcon(":/house.png"), "cardView", self))
        self.addAction(
            QAction(QIcon(":/dict.png"), "chooseDict", self))
        self.addAction(
            QAction(QIcon(":/edit.png"), "cardEditView", self))
        self.addAction(
            QAction(QIcon(":/profile.png"), "profile", self))

class ChooseDictStackController:
    def __init__(self, main, parent):
        self.parent = parent
        self.main = main

    def loadSoundsBtn(self):
        self.loadSoundsDialog = LoadSoundsDialog(self.main)
        self.loadSoundsDialog.show()

    def loadSoundWebBtn(self):
        workDict = {}
        checkList = self.main.chooseDict.checkedDicts()



        for dict_name, dict_data in self.main.dictSeq.scan.items():
            dirname = dict_data["dirname"]
            sounds = dict_data["sounds"]
            if dict_name in checkList:
                if sounds and not warningMessage(self, dict_name):
                    return
                workDict[dict_name] = dirname
        for dict_name, dict_path in  workDict.items():
            print(dict_name)
            print(self.main.dictSeq[dict_name].textBase)
            print(self.main.dictSeq[dict_name].textExamples)
            print("-------------------")







class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(790, 830)
        self.cfg = config.Config(paths.CONFIG)
        self._set_style_sheet(self.cfg["currentStyle"])

        self.dictSeq = DictSeq(paths.DICTIONARIES)

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
        self.chooseDict = ChooseDictStack(self, name="chooseDict",
                                          config=self.cfg)
        self.chooseDict.setFocusPolicy(Qt.NoFocus)
        self.controls["chooseDictStack"] = ChooseDictStackController(self,
                                                                     self.chooseDict)

        self.dictsModel = DictsModel(self.dictSeq)

        self.dictsModel.updateWorkData(self.cfg["choosedict"]['checkedDicts'])


        # работаем с карточками

        self.viewCard = viewcard.ViewCard(self.dictsModel)

        self.viewCard.setCardModel(self.cardModel)
        self.viewFrame = viewcard.ViewFrame(self.viewCard, "view")

        # редактируем карточки
        self.editDropList = editdrop_listview.DropListWidget(None, "editDropList")
        self.editDropList.setFocusPolicy(Qt.NoFocus)
        self.editDropList.setItems(config.Config(paths.CARD_CONFIG)["dropItemsTypeList"])
        self.viewEditCard = editcard.EditCard()

        self.viewEditCard.setCardModel(self.cardModel)
        self.viewCardEditWidget = editcardWidget.EditCardWidget(self.editDropList, self.viewEditCard, "cardEditView")

        self.stackWidgets["view"] = self.viewFrame
        self.stackWidgets["chooseDict"] = self.chooseDict
        self.stackWidgets["cardEditView"] = self.viewCardEditWidget

        self.centerStackFrame.setStackWidgets(self.stackWidgets)
        self.centerStackFrame.showStack(self._currentStackWidget)
        self.centerStackFrame.stack.currentChanged.connect(self.changeStackWidget)

        self.chooseDict.setCheckedItemsToNames(
            self.cfg["choosedict"]["checkedDicts"])
        self.setFocus(Qt.ActiveWindowFocusReason)
        self.changeStackWidget(0)

        self.newGame()

    def newGame(self):
        self.dictsModel.reset()
        self.viewCard.updateContent()


    def updateViews(self):
        self.viewCardEditWidget.updateContent()
        self.viewCard.updateWidgetComponent()


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
        elif self._currentStackWidget == "chooseDict":
            check = self.chooseDict.checkedDicts()
            self.dictsModel.updateWorkData(check)
            self.newGame()

        self._currentStackWidget = self.centerStackFrame.stack.widget(i).objectName()
        self.stackWidgets[self._currentStackWidget].setFocus(Qt.ActiveWindowFocusReason)




    def toolActions(self, act):
        getattr(self, "{}Action".format(act.text()))()

    def chooseDictAction(self):
        self.centerStackFrame.showStack("chooseDict")

    def cardEditViewAction(self):
        self.centerStackFrame.showStack("cardEditView")

    def cardViewAction(self):
        self.centerStackFrame.showStack("view")

    def profileAction(self):
        print("profile")

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
        if self._currentStackWidget == "view":
            self.viewKeyPressEvent(e)
        elif self._currentStackWidget == "cardEditView":
            self.editViewKeyPressEvent(e)

    def viewKeyPressEvent(self, e):
        if e.key() == Qt.Key_Right:
            self.viewCard.sideToName("front")
            self.viewCard.updateContent()
            # self.viewCard.t
        elif e.key() == Qt.Key_Left:
            print("<<<<<<<<<<<<")
        elif e.key() == Qt.Key_Space:
            self.viewCard.changeSide()

    def editViewKeyPressEvent(self, e):
        if e.key() == Qt.Key_Space:
            self.viewCardEditWidget.turnSideBtn.animateClick()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
    #
