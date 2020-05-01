from gtts import gTTS
from pathlib import Path
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class ProgressLabel(QLabel):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setAlignment(Qt.AlignCenter)




class SoundLoader(QFrame):
    def __init__(self, wordList, dirForSounds, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wordList = wordList
        self.dirForSounds = dirForSounds
        self.setParent(parent)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlag(Qt.Tool)
        self.resize(300, 50)
        self.box = QVBoxLayout(self)
        self.box.setSpacing(0)
        self.box.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("background-color: lightgrey")
        self.loadSoundWebProgress = QProgressBar()
        self.loadSoundWebProgress.setRange(0, len(wordList))
        self.loadSoundWebProgress.setFixedHeight(12)
        self.loadSoundWebProgress.setTextVisible(False)
        self.label = ProgressLabel()
        self.box.addWidget(self.label)
        self.box.addWidget(self.loadSoundWebProgress)
        self.show()


        self.soundNames = []


    def run(self):
        for n, line in enumerate(self.wordList, start=1):
            qApp.processEvents()
            tts = loadGtts(line)
            file_name = Path(self.dirForSounds) / "{}.mp3".format(line)
            saveTTS(tts, file_name)
            self.soundNames.append(file_name)
            self.loadSoundWebProgress.setValue(n)
            self.label.setText(line + '.mp3')
        else:
            return len(self.soundNames)





def loadGtts(line):
    return gTTS(line, lang='en')

def saveTTS(gtts, path):
    gtts.save(path)


if __name__ == '__main__':
    import paths
    datadir = paths.DATA / "family"
    Path(datadir / "sounds").mkdir(parents=True, exist_ok=True)
    targetDir = datadir / "sounds"

    wordList = ["mother", "father"]
    SoundLoader(wordList, targetDir)


