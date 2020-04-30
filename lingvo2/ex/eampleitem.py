

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






if __name__ == '__main__':

    s = "aaaaaaaaa_dddddddddddddddd\nsssssssssssss"




    ex = Example(s)
    print(ex.text)
    print(ex.spoiler)