
from pathlib import Path
from shutil import copy2
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import paths
from gui.choosedicts.choosedict import *
from core.soundloader import SoundLoader


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


class ChooseDictStackController:
    def __init__(self, main, parent):
        self.parent = parent
        self.main = main


    def loadSoundsBtn(self):
        self.loadSoundsDialog = LoadSoundsDialog(self.main)
        self.loadSoundsDialog.show()

    def loadSoundWebBtn(self):
        loaderDict = {}
        exLoaderDict = {}
        workDict = {}
        checkList = self.main.chooseDict.checkedDicts()
        for dict_name, dict_data in self.main.dictSeq.scan.items():
            dirname = dict_data["dirname"]
            sounds = dict_data["sounds"]
            # print(sounds)

            if dict_name in checkList:
                if sounds and not warningMessage(self, dict_name):
                    continue
                else:

                    workDict[dict_name] = dirname
        for dict_name, dict_path in  workDict.items():
            # --------------------------------------------------
            pdict_path = Path(dict_path)
            Path(pdict_path / "sounds").mkdir(parents=True, exist_ok=True)
            targetDir = pdict_path / "sounds"


            wordList = self.main.dictSeq[dict_name].textBase

            exampleList = self.main.dictSeq[dict_name].textExample
            if any(exampleList):
                # todo добавить скачивание примеров
                Path(pdict_path / "examplesSounds").mkdir(parents=True, exist_ok=True)
                examplestargetDir = pdict_path / "examplesSounds"

                soundLoader =  SoundLoader(exampleList, examplestargetDir, None)
                soundLoader.setWindowTitle("загружаются файлы для словаря - {}".format(dict_name))
                nfiles = soundLoader.run()
                soundLoader.close()
                exLoaderDict[dict_name] = (nfiles, len(exampleList))

            soundLoader =  SoundLoader(wordList, targetDir, None)
            soundLoader.setWindowTitle("загружаются файлы для словаря - {}".format(dict_name))
            nfiles = soundLoader.run()
            soundLoader.close()
            loaderDict[dict_name] = (nfiles, len(wordList))

        self.main.updateDictModel()
        self.main.newGame()
        return self._fsum(loaderDict, exLoaderDict, dict_name)

    def _fsum(self, d1, d2, name):
        for _d1, _d2 in zip(d1.values(), d2.values()):
            return {name: [p1 + p2 for p1, p2 in zip(_d1, _d2)]}

    def addDict(self):
        fname = QFileDialog.getOpenFileName(None, 'Open file', '/home')[0]
        if fname:
            dataDir = paths.DATA
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


            #

