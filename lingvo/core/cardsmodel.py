
class CardsModel:
    def __init__(self, dict_seq):
        self.dictSeq = dict_seq
        # print(self.dictSeq)

if __name__ == '__main__':
    import paths
    from core.dictsequence import DictSeq
    dictSeq = DictSeq(paths.DATA)
    cardModel = CardsModel(dictSeq)