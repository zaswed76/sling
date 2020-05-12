import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from gui.custom.customwidgets import *

class ControlBtn(QPushButton):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setIconSize(QSize(22, 22))


class LoadSoundsDialog(AbcDialog):
    def __init__(self, main):
        super().__init__()

        self.main = main
        self.setObjectName("chooseDictStack")
        self.resize(400, 200)
        self.box = BoxLayout(QBoxLayout.TopToBottom, self)
        self.box.setSpacing(4)
        self.loadSoundWebBtn = ControlBtn("загрузить файлы из интернета")
        self.loadSoundWebBtn.setObjectName("loadSoundWebBtn")
        self.loadSoundWebBtn.clicked.connect(self.loadSoundWeb)
        self.box.addWidget(self.loadSoundWebBtn)
        self.box.addStretch(10)

        self.statusLabel = QLabel()
        self.statusLabel.setObjectName("LoadSoundsDialog_statusLabel")

        self.box.addWidget(self.statusLabel)

    def closeEvent(self, *args, **kwargs):
        self.main.updateDictModel()
        self.main.chooseDict.updateViewList()



    def loadSoundWeb(self):
        self.statusLabel.clear()
        loaderDict = self.main.connect()
        # print(loaderDict)
        # textLines = []
        # for dct, res in  loaderDict.items():
        #     loads, all = res
        #     textLines.append('словарь "{}" - загружено {} из {}'.format(dct, loads, all))
        # text = "\n".join(textLines)
        # self.statusLabel.setText(text)






class ChooseDictControls(QFrame):
    def __init__(self, main, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main = main
        self.setObjectName("chooseDictStack")
        self.box = BoxLayout(QBoxLayout.TopToBottom, self, spacing=2, content_margin=(0, 2, 0, 0))



        self.addDictBtn = self.addBtn("addDict", ":/notebook_add.png")
        self.addDictDolderBtn = self.addBtn("addDictFolder", ":/book_blue_add.png")
        self.addSoundsBtn = self.addBtn("loadSoundsBtn", ":/music_blue_add.png")
        self.openDataFolder = self.addBtn("openDataFolder", ":/folder_window.png")


        self.box.addWidget(self.addDictBtn, alignment=Qt.AlignCenter)
        self.box.addWidget(self.addDictDolderBtn, alignment=Qt.AlignCenter)
        self.box.addWidget(self.addSoundsBtn, alignment=Qt.AlignCenter)
        self.box.addStretch(10)
        self.box.addWidget(self.openDataFolder, alignment=Qt.AlignCenter)

    def addBtn(self, methodName, icon=None):
        Btn = ControlBtn()
        if icon is not None:
            Btn.setIcon(QIcon(icon))
        else:
            Btn.setText(methodName[:5])
        Btn.clicked.connect(self.main.connect)
        Btn.setObjectName(methodName)
        return Btn