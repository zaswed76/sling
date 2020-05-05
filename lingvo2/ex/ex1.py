

class LoadObject:
    def __init__(self, dictName, *args):
        self.dictName = dictName
        self._soundsType = []

    def setSoundType(self, type, soundList):
        setattr(self, type, soundList)
        self._soundsType.append(type)

    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def soundsList(self):
        return [getattr(self, x) for x in self._soundsType]

    def soundsDict(self):
        return {x: getattr(self, x) for x in self._soundsType}


class Loader:
    def __init__(self, *p_args):
        pass

if __name__ == '__main__':
    loadObject = LoadObject("name")
    # loadObject.setSoundType("SoundWord", [1, 2, 3])
    loadObject.setSoundType("SoundExamples", [4, 5, 6])

    print(loadObject.soundsList())
    print(loadObject.soundsDict())