import time
import fileinput
import glob

from PyQt5 import QtMultimedia
from tools.handler import qt_message_handler


import config
from core.cardModel import CardModel
from core.dictsequence import DictSeq
from core.dictsmodel import DictsModel
from gui.centrallframe import CenterStackFrame
from gui.choosedicts.choosedict import *
from gui.choosedicts.contollers import ChooseDictStackController
from gui.editcard import editcard, editcardWidget, editdrop_listview
from gui.viewcard import viewcard
from gui.maintoolbar import ToolBar

qInstallMessageHandler(qt_message_handler)


def fileInput(folder):
    files_list = glob.glob(folder + "/*.css")
    ls = []
    with fileinput.input(files=files_list) as f:
        for line in f:
            ls.append(line)
    return "".join(ls)




class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.cfg = config.Config(paths.CONFIG)
        self.player = QtMultimedia.QMediaPlayer()
        self.start_time = time.time()
        self._size = self.cfg["ui"]["mainWindowSize"]
        self.setFixedSize(*self._size)
        self._set_style_sheet(self.cfg["currentStyle"])

        self.dictSeq = DictSeq(paths.DATA)

        self.dictSeq.setSoundTypes(self.cfg["choosedict"]["soundTypeList"])



        self.dictsModel = DictsModel(self.dictSeq)
        self.updateDictModel()

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
        self.chooseDict = ChooseDictStack(self, name="chooseDict", config=self.cfg)
        self.chooseDict.setFocusPolicy(Qt.NoFocus)
        self.chooseDictController = ChooseDictStackController(self, self.chooseDict)
        self.controls["chooseDictStack"] = self.chooseDictController
        # работаем с карточками
        self.viewCard = viewcard.ViewCard(self.dictsModel, main=self)
        self.viewCard.setFixedSize(*self.cfg["ui"]["viewCardSize"])
        self.viewCard.setCardModel(self.cardModel)
        self.viewFrame = viewcard.ViewFrame(self.viewCard, "view") # 790, 830   790, 788
        self.viewFrame.setFixedSize(self._size[0], self._size[1]-42) # 790, 830   790, 788

        # редактируем карточки
        self.editDropList = editdrop_listview.DropListWidget(None, "editDropList")
        self.editDropList.setFocusPolicy(Qt.NoFocus)
        self.editDropList.setItems(config.Config(paths.CARD_CONFIG)["dropItemsTypeList"])
        self.viewEditCard = editcard.EditCard(main=self)
        self.viewEditCard.setFixedSize(self._size[0]-190, self._size[1]-190)

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
        print(self.dictSeq["days of the week"]["monday"].image)



    def updateDictModel(self):
        self.dictSeq.init()
        self.dictsModel.updateWorkData(self.cfg["choosedict"]['checkedDicts'], self.dictSeq)



    def soundClick(self):
        # todo может ли self.dictsModel.currentItem == None
        pathsound = None
        widgetType = self.sender().parent().parent().widgetType
        if widgetType == "SpoilerExampleLabel"  and self.dictsModel.currentItem is not None:
            pathsound = self.dictsModel.currentItem.exampleSound
        elif widgetType == "DropLabel" and self.dictsModel.currentItem is not None:
            pathsound = self.dictsModel.currentItem.sound
        if pathsound is not None:
            self.playSound(pathsound)
            self.setFocus(Qt.ActiveWindowFocusReason)

    def playSound(self, filePath):
        if self.player.state() == QtMultimedia.QMediaPlayer.StoppedState:
            self.media = QUrl.fromLocalFile(filePath)
            self.content = QtMultimedia.QMediaContent(self.media)
            self.player = QtMultimedia.QMediaPlayer()
            self.player.setMedia(self.content)
            self.player.stateChanged.connect(self.mediaStatusSuond)
            self.player.play()
        else:
            self.player.setMedia(QtMultimedia.QMediaContent())
            self.player.stop()

    def positionSuond(self, i):
        pass
        # print(i, "!!!")

    def mediaStatusSuond(self, i):
        if self.player.state() == QtMultimedia.QMediaPlayer.StoppedState:
            self.player.setMedia(QtMultimedia.QMediaContent())
            self.player.stop()

    def newGame(self):
        self.dictsModel.reset()
        wordItem = self.dictsModel.nextItem()
        self.viewCard.updateContent(wordItem)
        self.player.setMedia(QtMultimedia.QMediaContent())
        self.player.stop()



    def updateViews(self):
        self.viewCardEditWidget.updateContent()
        self.viewCard.updateWidgetComponent()


    def getCardModel(self) -> CardModel:
        return self.cfgpObject.load()


    def connect(self):
        controll = self.sender()
        slot = controll.objectName()
        object = self.controls[controll.parent().objectName()]
        return getattr(object, slot)()

    def __setToolBar(self):
        self.toolBar = ToolBar(self)
        self._visibleToolBarFlag = True
        self.toolBar.visibilityChanged.connect(self.visibilityToolBar)
        self.addToolBar(Qt.TopToolBarArea, self.toolBar)
        self.toolBar.actionTriggered.connect(self.toolActions)

    def visibilityToolBar(self, p_bool):
        self._visibleToolBarFlag = p_bool


    def changeStackWidget(self, i):
        self.player.setMedia(QtMultimedia.QMediaContent())
        self.player.stop()
        if self._currentStackWidget == "cardEditView":
            self.cfg.save()
        elif self._currentStackWidget == "chooseDict":
            check = self.chooseDict.checkedDicts()
            self.dictsModel.updateWorkData(check, self.dictSeq)
            self.newGame()
        self._currentStackWidget = self.centerStackFrame.stack.widget(i).objectName()
        self.stackWidgets[self._currentStackWidget].setFocus(Qt.ActiveWindowFocusReason)
        if self.currentStackWidget == "view":
            self.toolBar.setDisabledButton("cardrefresh", False)
        else:
            self.toolBar.setDisabledButton("cardrefresh", True)




    def toolActions(self, act):
        getattr(self, "{}Action".format(act.text()))()

    def chooseDictAction(self):
        self.centerStackFrame.showStack("chooseDict")

    def cardEditViewAction(self):
        self.centerStackFrame.showStack("cardEditView")

    def cardViewAction(self):
        if self.currentStackWidget == "cardEditView":
            self.cardrefreshAction()
        self.centerStackFrame.showStack("view")



    def profileAction(self):
        pass
        # print("profile")

    def cardrefreshAction(self):
        currentStack = self.currentStackWidget
        self.centerStackFrame.removeStackWidget("view", self.stackWidgets["view"])
        del self.stackWidgets["view"]
        self.viewCard = viewcard.ViewCard(self.dictsModel, main=self)
        self.viewCard.setFixedSize(*self.cfg["ui"]["viewCardSize"])
        self.viewCard.setCardModel(self.cardModel)
        self.viewFrame = viewcard.ViewFrame(self.viewCard, "view")
        self.stackWidgets["view"] = self.viewFrame
        self.centerStackFrame.insertWidget(0, "view", self.stackWidgets["view"])
        self.centerStackFrame.showStack(currentStack)
        self.newGame()


    @property
    def currentStackWidget(self):
        return self._currentStackWidget


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
        if e.key() == Qt.Key_F12:
            self.toolBar.setVisible(not self._visibleToolBarFlag)
        if self._currentStackWidget == "view":
            self.viewKeyPressEvent(e)

        elif self._currentStackWidget == "cardEditView":
            self.editViewKeyPressEvent(e)
        self.centerStackFrame.setFocus()


    def wheelEvent(self, event):
        ang = event.angleDelta().y()
        if ang > 0:
            res = time.time() - self.start_time
            self.start_time = time.time()
            if res > 0.4:

                self.viewCard.sideToName("front")
                wordItem = self.dictsModel.nextItem()
                self.viewCard.updateContent(wordItem)
                self.setFocus(Qt.ActiveWindowFocusReason)
                self.player.setMedia(QtMultimedia.QMediaContent())
                self.player.stop()

    def viewKeyPressEvent(self, e):
        if e.key() == Qt.Key_Right:
            self.viewCard.sideToName("front")
            wordItem = self.dictsModel.nextItem()
            self.viewCard.updateContent(wordItem)
            self.setFocus(Qt.ActiveWindowFocusReason)
            self.player.setMedia(QtMultimedia.QMediaContent())
            self.player.stop()

        elif e.key() == Qt.Key_Left:
            self.viewCard.sideToName("front")
            wordItem = self.dictsModel.prevItem()
            self.viewCard.updateContent(wordItem)
            self.setFocus(Qt.ActiveWindowFocusReason)
            self.player.setMedia(QtMultimedia.QMediaContent())
            self.player.stop()
        elif e.key() == Qt.Key_Space:
            self.viewCard.changeSide()

    def editViewKeyPressEvent(self, e):
        if e.key() == Qt.Key_Space:
            self.viewCardEditWidget.turnSideBtn.animateClick()

    def mousePressEvent(self, e):
        rect = QRect(self.rect().topLeft(), QPoint(self._size[0], 41))
        x = e.pos().x()
        y = e.pos().y()
        if rect.contains(x, y) and not self._visibleToolBarFlag:
            self.toolBar.setVisible(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
    #
