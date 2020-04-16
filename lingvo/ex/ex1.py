
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

a1 = ['cat1', 'per1']
a2 = ['cat2', '[cat2]', 'per2']
a3 = ['cat3', 'per3', 'ex13', 'ex23']
a4 = ['cat4', '[cat]4', 'per4', 'ex14', 'ex24']
a5 = ['cat4', '[cat]4', 'per4', 'ex14', 'ex24', "[ex34]"]

lst = [a1, a2, a3, a4, a5]

class WordItem:
    def __init__(self, *args, **kwargs):
        self.transcription = "none"
        self.cyrillicTranscription = "none"
        self.translation = "none"
        self.base = "none"
        self.examples = []
        self.index = kwargs.get("index", 0)
        self.sound = kwargs.get("sound")
        self.image = kwargs.get("image")
        ln = len(args)
        if ln == 2:
            self.base, self.translation = args
        elif ln == 3:
            self.base, self.cyrillicTranscription, self.translation = args
        elif ln == 4:
            self.base, self.translation, *ex = args
            self.examples.extend(ex)
        elif ln > 4:
            self.base, self.cyrillicTranscription, self.translation, *ex = args
            self.examples.extend(ex)
            if self.examples[-1].startswith("["):
                self.transcription = self.examples.pop()

    def __repr__(self):
        return "{} {} cir:{} tr:{} {}".format(self.base,
                                   self.translation,
                                   self.cyrillicTranscription,
                                   self.transcription,
                                   self.examples)


if __name__ == '__main__':
    import pprint
    s = {}
    for i in lst:
        s[i[0]]= WordItem(*i)
    pprint.pprint(s)