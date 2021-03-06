import paths
from core import scandicts
from collections.abc import MutableMapping

datadir = paths.DATA

class WordItem:
    def __init__(self, *args, **kwargs):
        self.textItems = args
        self.transcription = "none"
        self.cyrillicTranscription = "none"
        self.translation = "none"
        self.base = "none"
        self.example = "none"
        self.example2 = "none"
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
            self.example, self.example2 = ex
        elif ln == 5:
            self.base, self.cyrillicTranscription, self.translation, self.example, self.example2 = args
        elif ln == 6:
            self.base, self.cyrillicTranscription, self.translation, self.example, self.example2, self.transcription = args


    # def __repr__(self):
    #     return "{} {} cir:{} tr:{} {}".format(self.base,
    #                                self.translation,
    #                                self.cyrillicTranscription,
    #                                self.transcription,
    #                                self.examples)

    def __repr__(self):
        return "{}".format(self.base)




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
        self.__data = {}
        self.scan  = scandicts.scan(folder)
        self.init()

    @property
    def data(self):
        return self.__data

    def init(self):
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
            print(wordItem.base, wordItem.image, wordItem.sound, sep=":")



