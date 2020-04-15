

class Card:
    def __init__(self, cfg):
        self.cfg = cfg
        self.front = []
        self.back = []
        self.sides = [self.front, self.front]
