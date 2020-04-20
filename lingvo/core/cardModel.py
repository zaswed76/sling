

class CardModel:
    def __init__(self, card_cfg):
        self.cardCfg = card_cfg
        self.front = []
        self.back = []
        self.sides = [self.front, self.front]
        print("init CardModel")
