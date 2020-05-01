from gtts import gTTS
from pathlib import Path

def soundLoader(wordList, dirForSounds):
    for line in wordList:
        tts = loadGtts(line)
        file_name = Path(dirForSounds) / "{}.mp3".format(line)
        saveTTS(tts, file_name)


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
    soundLoader(wordList, targetDir)


