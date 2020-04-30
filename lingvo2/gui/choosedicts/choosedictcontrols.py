import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from gui.custom.customwidgets import *

class ControlBtn(QPushButton):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setCursor(QCursor(Qt.PointingHandCursor))


class LoadSoundsDialog(AbcDialog):
    def __init__(self, main):
        super().__init__()
        self.setObjectName("chooseDictStack")
        self.setFixedSize(300, 200)
        self.box = BoxLayout(QBoxLayout.TopToBottom, self)
        self.box.setSpacing(4)

        self.loadSoundWebBtn = ControlBtn("загрузить файлы из интернета")
        self.loadSoundWebBtn.setObjectName("loadSoundWebBtn")
        self.loadSoundWebBtn.clicked.connect(main.connect)

        self.box.addWidget(self.loadSoundWebBtn)

        self.loadSoundWebProgress = QProgressBar()
        self.loadSoundWebProgress.setFixedHeight(4)
        self.box.addWidget(self.loadSoundWebProgress)



        self.box.addStretch(10)








class ChooseDictControls(QFrame):
    def __init__(self, main, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.box = BoxLayout(QBoxLayout.TopToBottom, self)
        self.loadSoundsBtn = ControlBtn()
        self.setObjectName("chooseDictStack")
        self.loadSoundsBtn.clicked.connect(main.connect)
        self.loadSoundsBtn.setObjectName("loadSoundsBtn")

        self.box.addWidget(self.loadSoundsBtn)
        self.box.addStretch(10)