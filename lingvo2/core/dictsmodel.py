import itertools


class DictsModel:
    def __init__(self, dict_seq):
        """
        класс предоставляет api для работы со списком  объектов WordItem
        :param dict_seq: dictsmodel.DictSeq
        """


        self.dictSeq = dict_seq
        self._workData = {}
        self._workList = list()
        self._cursor = -1
        self.currentItem = None


    @property
    def workData(self):
        return self._workData

    @property
    def workList(self):
        return self._workList

    def updateWorkData(self, checkedDicts, dictSeq):
        self.reset()
        self._workData = {k:v for k, v in dictSeq.items() if k in checkedDicts}

        self._workList.clear()
        for d in self._workData.values():
            for it in d.values():
                self._workList.append(it)


    def nextItem(self):
        if self._cursor < len(self._workList)-1:
            self._cursor += 1
            self.currentItem = self._workList[self._cursor]
            return self.currentItem


    def prevItem(self):
        if self._cursor > 0:
            self._cursor -=1
            return self._workList[self._cursor]

    def reset(self):
        self._cursor = -1

if __name__ == '__main__':
    import paths
    from core.dictsequence import DictSeq
    dictSeq = DictSeq(paths.DATA)
    cardModel = DictsModel(dictSeq)