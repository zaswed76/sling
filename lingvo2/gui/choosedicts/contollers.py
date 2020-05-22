import itertools
from pathlib import Path
from shutil import copy2
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import subprocess

import paths
from gui.choosedicts.choosedict import *
from core.soundloader import SoundLoaderDialog


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

class LoadDialogsFrame(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlag(Qt.Tool)

        self.base_box = QVBoxLayout(self)
        self.base_box.setSpacing(4)
        self.base_box.setContentsMargins(0, 0, 0, 0)
        self.setMinimumWidth(400)

    def addStratch(self, p_int):
        self.base_box.addStretch(p_int)

    def addWidget(self, widget):
        self.base_box.addWidget(widget)

    def closeEvent(self, QCloseEvent):
        ctrl = self.parent().main.chooseDictController
        if len(ctrl.finishedList) == len(ctrl.main.chooseDict.checkedDicts()):
            self.parent().main.updateDictModel()
            QCloseEvent.accept()
        else:
            QCloseEvent.ignore()




class ChooseDictStackController:
    def __init__(self, main, parent):
        self.parent = parent
        self.main = main

    def openDataFolder(self):
        print("openDataFolder")

        subprocess.Popen('explorer {}'.format(paths.DICTIONARIES))

    def loadSoundsBtn(self):
        self.loadSoundsDialog = LoadSoundsDialog(self.main)
        self.loadSoundsDialog.show()

    def loadSoundWebBtn(self):
        colors = ["#A7D8FB", "#B9FBB5"]
        gen = (x for x in itertools.cycle(colors))
        self.finishedList = []
        self.loadList = []
        loaderDict = {}
        checkList = self.main.chooseDict.checkedDicts()
        self.loadDialogsFrame = LoadDialogsFrame(self.loadSoundsDialog)
        self.loadDialogsFrame.show()
        self.loadDialogsFrame.addStratch(10)

        for n, (name, Dict) in enumerate(self.main.dictSeq.items()):
            if name in checkList:
                loaderDict[name] = SoundLoaderDialog(Dict, self.main)
                loaderDict[name].setStyleSheet('background: {};'.format(next(gen)))
                self.loadDialogsFrame.addWidget(loaderDict[name])
                loaderDict[name].finishedSignal.connect(self.finishedSignal)
                loaderDict[name].run()
        return loaderDict

    def addDictFolder(self):
        fdname = QFileDialog.getExistingDirectory(self.main, '/home')
        if fdname:
            dataDir = paths.DICTIONARIES
            pfname = Path(fdname)
            print(pfname)
            # name = pfname.stem

    def finishedSignal(self, p_name):
        self.finishedList.append(p_name)



    def _fsum(self, d1, d2, name):
        if not d1: d1 = {name: (0, 0)}
        if not d2: d2 = {name: (0, 0)}
        for _d1, _d2 in zip(d1.values(), d2.values()):

            return {name: [p1 + p2 for p1, p2 in zip(_d1, _d2)]}

    def addDict(self):
        fname = QFileDialog.getOpenFileName(None, 'Open file', '/home')[0]
        if fname:
            dataDir = paths.DICTIONARIES
            pfname = Path(fname)
            name = pfname.stem


            dict_folder = Path(dataDir / name)
            if not dict_folder.is_dir():
                dict_folder.mkdir(parents=True, exist_ok=True)
                copy2(fname, str(dict_folder / pfname.name))
                self.main.updateDictModel()
                self.main.chooseDict.updateViewList()
                self.main.newGame()
            else:
                msgBox = QMessageBox(QMessageBox.Warning, "warning!",
                                     "словарь с таким именем уже существует", QMessageBox.NoButton, None)
                msgBox.exec_()
                return




