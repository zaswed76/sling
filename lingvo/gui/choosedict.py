import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import paths
from gui.custom.customwidgets import *

class DictItem(QStandardItem):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setCheckable(True)


class DictListModel(QStandardItemModel):
    def __init__(self):
        super().__init__()

class ChooseDictView(QListView):
    def __init__(self, main, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main = main
        self.dictListModel = DictListModel()
        self.setModel(self.dictListModel)
        self.updateDictList()

    def updateDictList(self):
        for i in self.main.dictList:
            self.dictListModel.appendRow(DictItem(i))







class ControlFrame(QFrame):
    def __init__(self, main, *args, **kwargs):
        super().__init__(*args, **kwargs)

class TextFrame(QFrame):
    def __init__(self, main, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ChooseDictStack(QFrame):
    def __init__(self, main, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(600, 600)
        self.main = main
        self.box = BoxLayout(QBoxLayout.LeftToRight, self)
        self.chooseDictFrame = ChooseDictView(self.main)
        self.controlFrame = ControlFrame(self.main)
        self.textFrame = TextFrame(self.main)
        self.box.addWidget(self.chooseDictFrame, stretch=10)
        self.box.addWidget(self.controlFrame, stretch=2)
        self.box.addWidget(self.textFrame, stretch=20)

        top_right = self.rect().topRight()
        n = top_right - QPoint(41, -2)
        print(n)
        self.closeChooseDictBtn = QPushButton("ok", self)
        self.closeChooseDictBtn.setObjectName("closeChooseDict")
        self.closeChooseDictBtn.clicked.connect(self.main.connect)
        self.closeChooseDictBtn.setFixedSize(40, 40)
        self.closeChooseDictBtn.move(n)

    def parentMethod(self):
        print("parentMethod")


