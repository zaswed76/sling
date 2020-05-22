from gtts import gTTS
from pathlib import Path
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from functools import partial


class SoundLoader(QThread):
    progressSignal = pyqtSignal(int)
    soundNameSignal = pyqtSignal(str)

    def __init__(self, typeSound, wordList, dirForSounds):
        super().__init__()
        self.typeSound = typeSound
        self.dirForSounds = dirForSounds
        self.wordList = wordList
        self.lenWordList = len(self.wordList)

    def run(self):
        for n, line in enumerate(self.wordList, start=1):
            line = " ".join(line.split(" ")[:])
            __line = " ".join(line.split(" ")[:8]) + "_" + self.typeSound
            tts = loadGtts(line)
            file_name = Path(self.dirForSounds) / "{}.mp3".format(__line)
            saveTTS(tts, file_name)
            self.progressSignal.emit(n)
            self.soundNameSignal.emit(line)


class ProgressLabel(QLabel):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setAlignment(Qt.AlignLeft)


class LoadSoundProgress(QProgressBar):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(12)


class SoundLoaderDialog(QDialog):
    finishedSignal = pyqtSignal(str)
    def __init__(self, Dict, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.setParent(parent)
        # self.setWindowModality(Qt.ApplicationModal)
        # self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.Dict = Dict
        self.nameDict = self.Dict.name
        self.setWindowTitle('загружаются файлы для словаря - "{}"'.format(self.nameDict))
        self.soundTypeList = Dict.soundTypeList
        # self.setParent(parent)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlag(Qt.Tool)
        self.resize(300, 50)
        self.box = QVBoxLayout(self)
        self.box.setSpacing(4)
        self.box.setContentsMargins(0, 0, 0, 0)
        self.label = ProgressLabel("{}:".format(self.nameDict))
        self.box.addWidget(self.label)
        self.show()



    def run(self):
        self.soundLoadThreads = {}
        self.progressBars = {}
        self.finished = []
        for typeSound in self.soundTypeList:
            typeSoundList = self.Dict.itemListForTypeSound(typeSound)
            if typeSoundList:
                targetSoundDir = Path(self.Dict.dirname) / "{}Sounds".format(typeSound)
                targetSoundDir.mkdir(parents=True, exist_ok=True)

                formLayout = QFormLayout()
                formLayout.setFormAlignment(Qt.AlignRight)
                self.progressBars[typeSound] = LoadSoundProgress()
                self.progressBars[typeSound].setRange(0, len(typeSoundList))
                lb = QLabel(typeSound)
                lb.setFont(QFont("helvetica", 10))
                lb.setIndent(25)

                lb.setMinimumWidth(150)
                formLayout.addRow(lb, self.progressBars[typeSound])
                self.box.addLayout(formLayout)

                r = self.soundLoadThreads[typeSound] = SoundLoader(typeSound, typeSoundList, targetSoundDir)
                print(r)
                self.soundLoadThreads[typeSound].finished.connect(partial(self.finishedThead, typeSound))
                # self.soundLoadThreads[typeSound].soundNameSignal.connect()
                self.soundLoadThreads[typeSound].progressSignal.connect(self.progressBars[typeSound].setValue)

                self.soundLoadThreads[typeSound].start()



    def finishedThead(self, typeSound):
        self.finished.append(typeSound)
        if len(self.finished) == len(self.soundLoadThreads):
            for t in self.soundLoadThreads.values():
                t.terminate()
                t.wait(1000)
            QThread.sleep(1)
            self.finishedSignal.emit(self.nameDict)


def loadGtts(line):
    return gTTS(line, lang='en')


def saveTTS(gtts, path):
    gtts.save(path)


if __name__ == '__main__':
    import paths

    datadir = paths.DICTIONARIES / "family"
    Path(datadir / "sounds").mkdir(parents=True, exist_ok=True)
    targetDir = datadir / "sounds"

    wordList = ["mother", "father"]
    SoundLoader("word", wordList, targetDir)
    SoundLoader.run()
