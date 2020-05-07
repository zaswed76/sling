import sys
import textwrap
from tabulate import tabulate

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import paths
from gui.custom.customwidgets import *
from gui.choosedicts.choosedictcontrols import *

class DictItem(QStandardItem):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setCheckable(True)


class DictListModel(QStandardItemModel):
    def __init__(self):
        super().__init__()

    def updateDictList(self, dictList):
        for i in dictList:
            print(i, "5555")
            self.appendRow(DictItem(i))

class ChooseDictListView(QListView):
    def __init__(self, main, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main = main










class TextFrame(QTableWidget):
    def __init__(self, main, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main = main


    def updateTable(self, table):
        if not table:
            self.clear()
            for i in reversed(range(self.rowCount())):
                self.removeRow(i)
            return
        ncol = len(table[0])
        nrow = len(table)
        self.setColumnCount(ncol)
        self.setRowCount(nrow)



        for nrow, row in enumerate(table):
            for ncol, item in enumerate(row):
                widgetItem = QTableWidgetItem(item)
                widgetItem.setFont(QFont('helvetica', 12))

                self.setItem(nrow, ncol, widgetItem)

        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)




class ChooseDictStack(QFrame):
    def __init__(self, main, name=None, config=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cfg = config
        self.main = main
        self.setObjectName(name)
        self.box = BoxLayout(QBoxLayout.LeftToRight, self)
        self.box.setContentsMargins(0, 0, 0, 0)
        self.box.setSpacing(0)

        self.chooseDictListView = ChooseDictListView(self.main)
        self.dictListModel = DictListModel()
        self.chooseDictListView.setModel(self.dictListModel)

        self.updateViewList()
        self.chooseDictListView.clicked[QModelIndex].connect(self.itemDictChange)

        self.controlFrame = ChooseDictControls(self.main)
        self.textFrame = TextFrame(self.main)
        self.box.addWidget(self.chooseDictListView, stretch=10)
        self.box.addWidget(self.controlFrame, stretch=2)
        self.box.addWidget(self.textFrame, stretch=20)

        top_right = self.rect().topRight()
        n = top_right - QPoint(41, -2)


    def updateViewList(self):
        self.dictListModel.clear()
        self.dictListModel.updateDictList(self.main.dictSeq)


    def parentMethod(self):
        print("parentMethod")


    def itemDictChange(self, index):
        self.cfg["choosedict"]["checkedDicts"] = self.checkedDicts()
        tlist = []
        item = self.dictListModel.itemFromIndex(index)
        for item in self.main.dictSeq[item.text()].textItems:
            tlist.append(item)
        print(tlist)

        # tb = tabulate(tlist, tablefmt="github")
        # print(tb)

        self.textFrame.updateTable(tlist)

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




