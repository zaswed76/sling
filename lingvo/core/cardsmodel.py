
class CardsModel:
    def __init__(self, dict_seq, choose_dict):
        self.chooseDict = choose_dict
        self.checkedDicts = []
        self.dictSeq = dict_seq
        self.__workData = {}

    @property
    def workData(self):
        return self.__workData

    def updateWorkData(self):
        self.checkedDicts = self.chooseDict.checkedDicts()
        self.__workData = {k:v for k, v in self.dictSeq.items() if k in self.checkedDicts}

if __name__ == '__main__':
    import paths
    from core.dictsequence import DictSeq
    dictSeq = DictSeq(paths.DATA)
    cardModel = CardsModel(dictSeq)