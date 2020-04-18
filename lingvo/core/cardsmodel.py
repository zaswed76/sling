import itertools


class CardsModel:
    def __init__(self, dict_seq, choose_dict):
        self.chooseDict = choose_dict
        self.checkedDicts = []
        self.dictSeq = dict_seq
        self._workData = {}
        self._workList = list()
        self._cursor = -1


    @property
    def workData(self):
        return self._workData

    @property
    def workList(self):
        return self._workList

    def updateWorkData(self):
        self.reset()
        self.checkedDicts = self.chooseDict.checkedDicts()
        # print(self.checkedDicts)
        self._workData = {k:v for k, v in self.dictSeq.items() if k in self.checkedDicts}
        self._workList.clear()
        for d in self._workData.values():
            for it in d.values():
                # print(it, type(it))
                self._workList.append(it)
        # self._workList.extend(list(itertools.chain(*[list(x) for x in self._workData.values()])))

    def nextItem(self):
        if self._cursor < len(self._workList)-1:
            self._cursor += 1
            return self._workList[self._cursor]

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
    cardModel = CardsModel(dictSeq)