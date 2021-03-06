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
from gui.terminal import TeminalFrame, TerminalController
from gui.gsettings import gsettings, gsettingsControllers
from gui.mainToolBarController import MainToolBarController
from gui.profiles import profiles, profilesController
from gui.games import gamestack, gamesController
from gui.video import video, videoController

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
        self.currentProfile = self.cfg["core"]["currentProfile"]
        self._size = self.cfg["ui"]["mainWindowSize"]
        self._initScreen()

        self.mainToolBarController = MainToolBarController(self)

        self.player = QtMultimedia.QMediaPlayer()
        self.start_time = time.time()

        self._set_style_sheet(self.cfg["currentStyle"])

        self.dictSeq = DictSeq(paths.DICTIONARIES)

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
        # self.chooseDict.setFocusPolicy(Qt.NoFocus)
        self.chooseDictController = ChooseDictStackController(self, self.chooseDict)
        self.controls["chooseDictStack"] = self.chooseDictController
        # работаем с карточками
        self.viewCard = viewcard.ViewCard(self.dictsModel, main=self)
        self.resizeCardView()
        self.viewCard.setCardModel(self.cardModel)
        self.viewFrame = viewcard.ViewFrame(self.viewCard, "view")  # 790, 830   790, 788
        # self.viewFrame.setFixedSize(self._size[0], self._size[1] - 42)  # 790, 830   790, 788

        # редактируем карточки
        self.editDropList = editdrop_listview.DropListWidget(None, "editDropList")
        self.editDropList.setFocusPolicy(Qt.NoFocus)
        self.editDropList.setItems(config.Config(paths.CARD_CONFIG)["dropItemsTypeList"])
        self.viewEditCard = editcard.EditCard(main=self)
        self.viewEditCard.setFixedSize(self.cfg["ui"]["viewCardWidth"], self.cfg["ui"]["viewCardHeight"])

        self.viewEditCard.setCardModel(self.cardModel)
        self.viewCardEditWidget = editcardWidget.EditCardWidget(self.editDropList, self.viewEditCard, "cardEditView")

        self.terminalController = TerminalController(self)
        self.terminal = TeminalFrame(self, self.cfg, "terminal", self.terminalController)

        self.gsettings = gsettings.Gsettings(self, self.cfg, "gsettings")
        self.gsetGeometryController = gsettingsControllers.GsettingsGeometryController(
            self, self.gsettings._sections["gSettingsGeometry"])
        self.controls["gSettingsGeometry"] = self.gsetGeometryController

        self.gDictController = gsettingsControllers.GDictController(
            self, self.gsettings._sections["gSettingsDict"])
        self.controls["gSettingsDict"] = self.gDictController

        self.profiles = profiles.Profiles(self, objectName="profiles", config=self.cfg)
        self.profilesController = profilesController.ProfilesController(self, self.profiles)
        self.controls["profiles"] = self.profilesController

        self.games = gamestack.Games(self, objectName="games", config=self.cfg)
        self.gamesController = gamesController.GamesController(self, self.games)
        self.controls["games"] = self.gamesController

        self.video = video.Video(self, objectName="video", config=self.cfg)
        self.videoController = videoController.VideoController(self, self.profiles)
        self.controls["video"] = self.videoController

        self.stackWidgets["view"] = self.viewFrame
        self.stackWidgets["chooseDict"] = self.chooseDict
        self.stackWidgets["cardEditView"] = self.viewCardEditWidget
        self.stackWidgets["terminal"] = self.terminal
        self.stackWidgets["gsettings"] = self.gsettings
        self.stackWidgets["profiles"] = self.profiles
        self.stackWidgets["games"] = self.games
        self.stackWidgets["video"] = self.video

        self.centerStackFrame.setStackWidgets(self.stackWidgets)

        self.centerStackFrame.showStack(self._currentStackWidget)
        self.centerStackFrame.stack.currentChanged.connect(self.changeStackWidget)

        self.chooseDict.setCheckedItemsToNames(
            self.cfg["choosedict"]["checkedDicts"])
        self.setFocus(Qt.ActiveWindowFocusReason)
        self.changeStackWidget(0)

        self.newGame()

    def sizeHint(self):
        w = self.cfg["ui"]["viewCardWidth"]
        h = self.cfg["ui"]["viewCardHeight"]
        return QSize(w, h)

    def currentDict(self):
        dictname = self.cfg["choosedict"]['checkedDicts'][0]
        currentDict = self.dictSeq[dictname]
        return currentDict

    def resizeCardView(self):
        self.viewCard.setFixedSize(self.cfg["ui"]["viewCardWidth"], self.cfg["ui"]["viewCardHeight"])

    def _initScreen(self):
        if self.cfg["ui"]["fullScreen"]:
            self.showFullScreen()
        else:
            self.showNormal()

    def updateDictModel(self):
        self.dictSeq.init()
        self.dictsModel.updateWorkData(self.cfg["choosedict"]['checkedDicts'], self.dictSeq)

    def soundClick(self):
        # todo может ли self.dictsModel.currentItem == None
        pathsound = None
        widgetType = self.sender().parent().parent().widgetType
        if widgetType == "SpoilerExampleLabel" and self.dictsModel.currentItem is not None:
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
        self.toolBar.btns["autoSoundGo"].setChecked(self.cfg["core"]["autoSoundGo"])
        self.toolBar.btns["autoSoundTurn"].setChecked(self.cfg["core"]["autoSoundTurn"])

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
        elif self._currentStackWidget == "gsettings":
            self.gsettings._sections["gSettingsGeometry"].updateCfg()
            self.resizeCardView()
            print(self.cfg["ui"]["viewCardWidth"], "!!!!!!!!!!!!!!")
            self.video.setSizeVideo(self.cfg["ui"]["viewCardWidth"] + 150,
                                             self.cfg["ui"]["viewCardHeight"])
            # todo update geometry
        elif self._currentStackWidget == "video":
            self.video.pause()

        self._currentStackWidget = self.centerStackFrame.stack.widget(i).objectName()

        # self.stackWidgets[self._currentStackWidget].setFocus(Qt.ActiveWindowFocusReason)

        if self.currentStackWidget == "view":
            self.toolBar.setDisabledButton("cardrefresh", False)
        else:
            self.toolBar.setDisabledButton("cardrefresh", True)



    def toolActions(self, act):
        getattr(self.mainToolBarController, "{}Action".format(act.text()))()

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
        modifiers = QApplication.keyboardModifiers()
        if modifiers == (Qt.ControlModifier | Qt.ShiftModifier):
            if e.key() == Qt.Key_T:
                self.openTerminal()
        elif e.key() == Qt.Key_F12:
            self.toolBar.setVisible(not self._visibleToolBarFlag)
        elif self._currentStackWidget == "view":
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
            if wordItem is not None:
                if wordItem.localVideo:
                    print(self.dictsModel.workData)
            self.viewCard.updateContent(wordItem)

            self.setFocus(Qt.ActiveWindowFocusReason)

            if self.cfg["core"]["autoSoundGo"]:
                pathsound = self.dictsModel.currentItem.sound
                if pathsound is not None:
                    self.playSound(pathsound)
            else:
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
            if (self.cfg["core"]["autoSoundTurn"] and self.viewCard.currentSideIndex == 1):
                pathsound = self.dictsModel.currentItem.sound
                if pathsound is not None:
                    self.playSound(pathsound)

    def editViewKeyPressEvent(self, e):
        if e.key() == Qt.Key_Space:
            self.viewCardEditWidget.turnSideBtn.animateClick()

    def mousePressEvent(self, e):
        rect = QRect(self.rect().topLeft(), QPoint(self._size[0], 41))
        x = e.pos().x()
        y = e.pos().y()
        if rect.contains(x, y) and not self._visibleToolBarFlag:
            self.toolBar.setVisible(True)

    def openTerminal(self):
        self._currentStackWidget = "terminal"
        self.centerStackFrame.showStack("terminal")

        focused_widget = qApp.focusWidget()
        focused_widget.clearFocus()
        self.terminal.setFocus()
        self.terminal.TerminalLine.setFocus()

        # self.terminal.setHelloText("{}\n>>> ".format(str(paths.ROOT)))
        # todo openTerminal


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
    #
