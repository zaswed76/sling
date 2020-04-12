import paths

import csv

class Examples:
    def __init__(self, examples):
        self.examples = examples




class Card:
    def __init__(self, base,
                 cyrillic_transcription,
                 translation,
                 ex1=None,
                 ex2=None,
                 transcription="", image=None, sound=None, index=0):
        self.index = index
        self.sound = sound
        self.image = image

        self.transcription = transcription
        self.cyrillicTranscription = cyrillic_transcription
        self.translation = translation
        self.base = base
        self.example1 = ex1
        self.example2 = ex2
        self.rexample1 = list(reversed(ex1))
        self.rexample2 = list(reversed(ex2))
        self.front = ["translation"]
        self.back = ["base", "cyrillicTranscription", "ex1", "ex2"]

        self.front2 = ["base"]
        self.back2 = ["translation", "cyrillicTranscription", "rex1", "rex2"]


path = r"D:\user\projects\sling\lingvo\data\slovar1\testDict.txt"

with open(path, newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=";")
    data = list(spamreader)
for line in data:
    print(line)
    print(line[:3])
    print(line[3:5])
    print(line[5:7])


