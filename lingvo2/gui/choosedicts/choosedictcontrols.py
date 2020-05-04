import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from gui.custom.customwidgets import *

class ControlBtn(QPushButton):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setIconSize(QSize(36, 36))


class LoadSoundsDialog(AbcDialog):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.setObjectName("chooseDictStack")
        self.setFixedSize(300, 200)
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


    def loadSoundWeb(self):
        self.statusLabel.clear()
        loaderDict = self.main.connect()
        textLines = []
        for dct, res in  loaderDict.items():
            loads, all = res
            textLines.append('словарь "{}" - загружено {} из {}'.format(dct, loads, all))
        text = "\n".join(textLines)
        self.statusLabel.setText(text)






class ChooseDictControls(QFrame):
    def __init__(self, main, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setObjectName("chooseDictStack")
        self.box = BoxLayout(QBoxLayout.TopToBottom, self, spacing=6, content_margin=(0, 6, 0, 0))


        self.addDictBtn = ControlBtn()
        self.addDictBtn.setIcon(QIcon(":/notebook_add.png"))
        self.addDictBtn.clicked.connect(main.connect)
        self.addDictBtn.setObjectName("addDict")

        self.addSoundsBtn = ControlBtn()
        self.addSoundsBtn.setIcon(QIcon(":/music_blue_add.png"))
        self.addSoundsBtn.clicked.connect(main.connect)
        self.addSoundsBtn.setObjectName("loadSoundsBtn")

        self.box.addWidget(self.addDictBtn, alignment=Qt.AlignCenter)
        self.box.addWidget(self.addSoundsBtn, alignment=Qt.AlignCenter)
        self.box.addStretch(10)