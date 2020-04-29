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

    def updateDictList(self, dictList):
        for i in dictList:
            self.appendRow(DictItem(i))

class ChooseDictView(QListView):
    def __init__(self, main, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main = main




class ControlFrame(QFrame):
    def __init__(self, main, *args, **kwargs):
        super().__init__(*args, **kwargs)

class TextFrame(QTextEdit):
    def __init__(self, main, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setTextColor(QColor("grey"))
        self.setWordWrapMode(QTextOption.NoWrap)

class ChooseDictStack(QFrame):
    def __init__(self, main, name=None, config=None, *args, **kwargs):


        super().__init__(*args, **kwargs)
        self.cfg = config
        self.main = main
        self.setObjectName(name)
        self.box = BoxLayout(QBoxLayout.LeftToRight, self)
        self.box.setContentsMargins(0, 0, 0, 0)
        self.box.setSpacing(0)

        self.chooseDictFrame = ChooseDictView(self.main)
        self.dictListModel = DictListModel()
        self.chooseDictFrame.setModel(self.dictListModel)

        self.dictListModel.updateDictList(self.main.dictSeq)
        self.chooseDictFrame.clicked[QModelIndex].connect(self.itemDictChange)

        self.controlFrame = ControlFrame(self.main)
        self.textFrame = TextFrame(self.main)
        self.box.addWidget(self.chooseDictFrame, stretch=10)
        self.box.addWidget(self.controlFrame, stretch=2)
        self.box.addWidget(self.textFrame, stretch=20)

        top_right = self.rect().topRight()
        n = top_right - QPoint(41, -2)



    def parentMethod(self):
        print("parentMethod")


    def itemDictChange(self, index):
        self.cfg["choosedict"]["checkedDicts"] = self.checkedDicts()
        tlist = []
        item = self.dictListModel.itemFromIndex(index)

        for item in self.main.dictSeq[item.text()].textItems:
            print(item, "!!!!")

            tlist.append("   ".join(item) + "\n")
        text = "".join(tlist)
        self.textFrame.setPlainText(text)

    def dictsItems(self) -> list([str, str]):
        items = []
        for index in range(self.dictListModel.rowCount()):
            items.append(self.dictListModel.item(index).text())
        return items


    def setCheckedItemsToNames(self, args):
        for index in range(self.dictListModel.rowCount()):
            item = self.dictListModel.item(index)
            text = item.text()
            if text in args:
                item.setCheckState(Qt.Checked)

    def checkedDicts(self) -> list([str, str]):
        selected = []
        for index in range(self.dictListModel.rowCount()):
            item = self.dictListModel.item(index)
            if item.checkState():
                selected.append(item.text())
        return selected




