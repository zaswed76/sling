import itertools


class CardsModel:
    def __init__(self, dict_seq, choose_dict):
        self.chooseDict = choose_dict
        self.checkedDicts = []
        self.dictSeq = dict_seq
        self._workData = {}
        self._workList = []

    @property
    def workData(self):
        return self._workData

    @property
    def workList(self):
        return self._workList

    def updateWorkData(self):
        self.checkedDicts = self.chooseDict.checkedDicts()
        self._workData = {k:v for k, v in self.dictSeq.items() if k in self.checkedDicts}
        self._workList.clear()
        self._workList = itertools.chain(*[list(x) for x in self._workData.values()])

    def nextItem(self):
        pass

if __name__ == '__main__':
    import paths
    from core.dictsequence import DictSeq
    dictSeq = DictSeq(paths.DATA)
    cardModel = CardsModel(dictSeq)