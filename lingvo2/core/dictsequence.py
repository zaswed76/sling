import paths
from core import scandicts
from collections.abc import MutableMapping

datadir = paths.DATA

class Example:
    def __init__(self, example: str = None):
        self.example = example
        self.spoiler = None
        if example is None:
            self.text = None
        else:
            spl = self.example.split("_")[:2]
            lspl = len(spl)
            if lspl == 1:
                self.text = spl[0]
            elif lspl == 2:
                self.text, self.spoiler = spl
            if not self.text:
                self.text = None
            if not self.spoiler:
                self.spoiler = None



class WordItem:
    def __init__(self, *args, **kwargs):
        self.textItems = args
        self.transcription = None
        self.cyrillicTrans = None
        self.translation = None
        self.Word = None
        self.example = Example()
        self.example2 = Example()
        self.index = kwargs.get("index", 0)
        self.sound = kwargs.get("sound")
        self.image = kwargs.get("image")
        ln = len(args)
        if ln == 2:
            self.Word, self.translation = args
        elif ln == 3:
            self.Word, self.cyrillicTrans, self.translation = args
        elif ln == 4:
            self.Word, self.translation, *ex = args
            self.example = Example(ex[0])
            self.example2 = Example(ex[1])
        elif ln == 5:
            self.Word, self.cyrillicTrans, self.translation, *ex = args
            self.example = Example(ex[0])
            self.example2 = Example(ex[1])
        elif ln == 6:
            self.Word, self.cyrillicTrans, self.translation, *ex, self.transcription = args
            self.cyrillicTrans = "[{}]".format(self.cyrillicTrans)
            self.example = Example(ex[0])
            self.example2 = Example(ex[1])

    def getSpoiler(self):
        text = self.example.spoiler
        return text

    def getTypeText(self, typeText):
        text = getattr(self, typeText)
        if typeText is not None:
            if typeText == "example" and text is not None:
                text = text.text
        return text

    def __repr__(self):
        return "{}".format(self.Word)




class Dict(MutableMapping):
    def __init__(self, name, dictpath,  dirname, images, sounds):
        self.__data = {}
        self.dictpath = dictpath
        self.sounds = sounds
        self.images = images
        self.dirname = dirname
        self.name = name
        self.updateWordObjects()

    @property
    def textBase(self):
        return [x.Word for x in self.__data.values()]
    @property
    def textExample(self):
        return [x.example.text for x in self.__data.values()]

    @property
    def textItems(self):
        return [x.textItems for x in self.__data.values()]

    def updateWordObjects(self):
        for id, line in enumerate(scandicts.Reader().load(self.dictpath)):
            self.__data[line[0]] = WordItem(*line,
                                            image=self.images.get(line[0]),
                                            sound=self.sounds.get(line[0]),
                                            index=id
                                            )

    def __setitem__(self, key, value):
        self.__data[key] = value

    def __getitem__(self, key):
        return self.__data[key]

    def __len__(self):
        return len(self.__data)

    def __delitem__(self, key):
        del self.__data[key]

    def __iter__(self):
        return iter(self.__data)

    def __repr__(self):
        return "D:{}".format(self.__data)


class DictSeq(MutableMapping):
    def __init__(self, folder):
        """
        словарь словарей
        :param folder:
        """
        self.folder = folder
        self.__data = {}
        # self.scan  = scandicts.scan(folder)


    def clear(self):
        self.__data.clear()

    @property
    def data(self):
        return self.__data

    def init(self):
        self.clear()
        self.scan = scandicts.scan(self.folder)
        for n, d in self.scan.items():
            self.__data[n] = Dict(n, d["dictpath"],
                                  d["dirname"],
                                  d['images'],
                                  d['sounds'])

    def __setitem__(self, key, value):
        self.__data[key] = value

    def __getitem__(self, key):
        return self.__data[key]

    def __len__(self):
        return len(self.__data)

    def __delitem__(self, key):
        del self.__data[key]

    def __iter__(self):
        return iter(self.__data)

    def __repr__(self):
        return str(self.__data)

    def items(self):
        return self.__data.items()

    def dictNames(self):
        return list(self.__data.keys())



if __name__ == '__main__':
    import pprint
    ds = DictSeq(paths.DATA)
    for name, slovar in ds.items():
        print("-----------")
        print(name)
        for wordItem in slovar.values():
            print(wordItem.Word, wordItem.image, wordItem.sound, sep=":")



