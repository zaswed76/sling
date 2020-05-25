
from gui.viewcard import viewcard
from PyQt5.QtCore import QObject

class MainToolBarController(QObject):
    def __init__(self, main):
        super().__init__()
        self.main = main

    def gameStackAction(self):
        self.main.centerStackFrame.showStack("games")


    def videoAction(self):
        self.main.centerStackFrame.showStack("video")
        videoDict = self.main.currentDict().video
        if videoDict:
            videofile = list(videoDict.values())[0]
            self.main.video.setFile(videofile)
            self.main.video.play()

    def profilesAction(self):
        self.main.centerStackFrame.showStack("profiles")

    def showScreenAction(self):
        if self.main.isFullScreen():
            self.main.showNormal()
        else:
            self.main.showFullScreen()

    def closeWindowAction(self):
        self.main.close()

    def chooseDictAction(self):
        self.main.centerStackFrame.showStack("chooseDict")

    def autoSoundGoAction(self):
        checked = not self.main.toolBar.btns["autoSoundGo"].isChecked()
        self.main.cfg["core"]["autoSoundGo"] = checked

    def autoSoundTurnAction(self):
        checked = not self.main.toolBar.btns["autoSoundTurn"].isChecked()
        self.main.cfg["core"]["autoSoundTurn"] = checked

    def cardEditViewAction(self):
        self.main.centerStackFrame.showStack("cardEditView")

    def cardViewAction(self):
        if self.main.currentStackWidget == "cardEditView":
            self.cardrefreshAction()
        self.main.centerStackFrame.showStack("view")

    def gsettingsAction(self):
        self.main.centerStackFrame.showStack("gsettings")

    def cardrefreshAction(self):
        currentStack = self.main.currentStackWidget
        self.main.centerStackFrame.removeStackWidget("view", self.main.stackWidgets["view"])
        del self.main.stackWidgets["view"]
        self.main.viewCard = viewcard.ViewCard(self.main.dictsModel, main=self.main)
        self.main.viewCard.setFixedSize(self.main.cfg["ui"]["viewCardWidth"], self.main.cfg["ui"]["viewCardHeight"])
        self.main.viewCard.setCardModel(self.main.cardModel)
        self.main.viewFrame = viewcard.ViewFrame(self.main.viewCard, "view")
        self.main.stackWidgets["view"] = self.main.viewFrame
        self.main.centerStackFrame.insertWidget(0, "view", self.main.stackWidgets["view"])
        self.main.centerStackFrame.showStack(currentStack)
        self.main.newGame()
