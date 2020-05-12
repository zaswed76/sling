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
        self.spoilerExample = Example()
        self.example2 = Example()
        self.index = kwargs.get("index", 0)
        self.sound = kwargs.get("sound")
        self.exampleSound = kwargs.get("exampleSound")

        self.image = kwargs.get("image")
        ln = len(args)
        if ln == 2:
            self.Word, self.translation = args
        elif ln == 3:
            self.Word, self.cyrillicTrans, self.translation = args
        elif ln == 4:
            self.Word, self.translation, *ex = args
            self.spoilerExample = Example(ex[0])
            self.example2 = Example(ex[1])
        elif ln == 5:
            self.Word, self.cyrillicTrans, self.translation, *ex = args
            self.spoilerExample = Example(ex[0])
            self.example2 = Example(ex[1])
        elif ln == 6:
            self.Word, self.cyrillicTrans, self.translation, *ex, self.transcription = args

            self.spoilerExample = Example(ex[0])
            self.example2 = Example(ex[1])

        if self.cyrillicTrans:
            self.cyrillicTrans = "[{}]".format(self.cyrillicTrans)

    def getImage(self):
        return self.image

    def getSpoiler(self):
        text = self.spoilerExample.spoiler
        return text

    def getTypeText(self, typeText):
        text = getattr(self, typeText)
        if typeText is not None:
            if typeText in ["spoilerExample", "example2"] and text is not None:
                text = text.text
        return text

    def __repr__(self):
        return "{}".format(self.Word)




class Dict(MutableMapping):
    def __init__(self, content, name, dictpath,  dirname, images, sounds, soundTypeList=None):
        self.content = content
        if soundTypeList is None:
            self.soundTypeList = []
        self.soundTypeList = soundTypeList
        self.__data = {}
        self.dictpath = dictpath
        self.sounds = sounds

        self.images = images
        self.dirname = dirname
        self.name = name
        self.updateWordObjects()


    def contents(self):
        cnt = dict(WordSound = 0, ExampleSound = 0, image = 0)
        for item in self.__data.values():
            if item.sound: cnt['WordSound']+= 1
            if item.exampleSound:  cnt['ExampleSound']+= 1
            if item.image: cnt['image'] += 1
        return cnt





    def itemListForTypeSound(self, typeSound):
        return getattr(self, "{}_List".format(typeSound))

    @property
    def Word_List(self):
        return [x.Word for x in self.__data.values() if x]

    @property
    def spoilerExample_List(self):
        return [x.spoilerExample.text for x in self.__data.values() if x.spoilerExample.text]

    @property
    def example2_List(self):
        return [x.example2.text for x in self.__data.values() if x.example2.text]

    @property
    def textItems(self):
        return [x.textItems for x in self.__data.values()]

    def updateWordObjects(self):
        for id, line in enumerate(self.content):
            ex = line[3:4]
            if ex:
                exname = ex[0].split("_")[0]
                exname = " ".join(exname.split(" ")[:8])
            else:
                exname = None
            soundWordName = "{}_Word".format(line[0])
            exampleSoundWordName = "{}_spoilerExample".format(exname)
            self.__data[line[0]] = WordItem(*line,
                                            image=self.images.get(line[0]),
                                            sound=self.sounds.get(soundWordName),
                                            exampleSound=self.sounds.get(exampleSoundWordName),
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
        self._soundTypeList = []


    def setSoundTypes(self, soundTypeList):
        self._soundTypeList.extend(soundTypeList)

    @property
    def soundTypeList(self):
        return self._soundTypeList

    def clear(self):
        self.__data.clear()

    @property
    def data(self):
        return self.__data

    def init(self):
        self.clear()
        self.scan = scandicts.scan(self.folder)
        for n, d in self.scan.items():
            content = scandicts.Reader().load(d["dictpath"])
            if content is None:
                return
            self.__data[n] = Dict(content, n, d["dictpath"],
                                  d["dirname"],
                                  d['images'],
                                  d['sounds'],
                                  soundTypeList=self.soundTypeList)



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
    print(ds)
    for name, slovar in ds.items():
        print("-----------")
        print(name)
        # for wordItem in slovar.values():
        #     print(wordItem.Word, wordItem.image, wordItem.sound, sep=":")



