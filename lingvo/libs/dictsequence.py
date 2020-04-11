import paths
from libs import scandicts

datadir = paths.DATA

class Word:
    def __init__(self, base,
                 translation,
                 cyrillic_transcription,
                 transcription="", image=None, sound=None, index=0):
        self.index = index
        self.sound = sound
        self.image = image
        self.transcription = transcription
        self.cyrillicTranscription = cyrillic_transcription
        self.translation = translation
        self.base = base

    def __repr__(self):
        return "W:{}\nI:{}\nS:{}\n".format(self.base, self.image, self.sound)



class Dict:
    def __init__(self, name, dictpath,  dirname, images, sounds):
        self.__words = []
        self.dictpath = dictpath
        self.sounds = sounds
        self.images = images
        self.dirname = dirname
        self.name = name
        self.updateWordObjects()



    @property
    def words(self):
        return self.__words

    def updateWordObjects(self):
        for id, line in enumerate(scandicts.Reader().load(self.dictpath)):
            transcription = line[3] if len(line) > 3 else ""
            self.__words.append(Word(*line[0:3],
                                     transcription,
                                     image=self.images.get(line[0]),
                                     sound=self.sounds.get(line[0]),
                                     index=id))





    def __repr__(self):
        return "D:{}".format(self.__words)


class DictSeq:
    def __init__(self, folder):
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
    ds = DictSeq(paths.DATA)
    for d in ds.items():
        print(d)
        print("----")



