import os
from pathlib import Path
from core.xlsxreader import xlsxRead
from collections import UserDict


class Reader:
    def __init__(self, path=None):
        self.data = []
        if path is not None:
            self.path = Path(path)
            self.load(self.path)


    def load(self, path):

        self.data.clear()
        self.path = Path(path)
        if self.path.suffix == ".txt":
            return self.readTxt(path)
        elif self.path.suffix == ".xlsx":
            return self.readXlsx(path)

    def readTxt(self, path):
        with open(path, "r") as f:
            for i in f.readlines():
                it = i.strip().split()
                if it:
                    self.data.append(it)
        return self.data

    def readXlsx(self, path):
        return xlsxRead(path)






def rglobs(folder, exts):
    lst = []

    ppath = Path(folder)

    for ext in exts:
        lst.extend([str(x) for x in ppath.rglob("*{}".format(ext))])
    rg = {Path(n).stem: n for n in lst}



    return rg


def scan(folder,
         dictexts=('.txt', '.xlsx'),
         imageexts=(".jpg", '.png'),
         soundexts=(".mp3",)):

    """

    :param folder:
    :param dictexts:
    :param imageexts:
    :param soundexts:
    :return: {'namedict' : {dict: str,
                            dirname: str,
                            images: [str, str],
                            sounds: [str, str]}}
    """
    dm = {}

    for root, directories, filenames in os.walk(folder):
        for filename in filenames:
            name, ext = os.path.splitext(filename)
            if ext in dictexts:
                dm[name] = {'dictpath': os.path.join(root, filename),
                            "dirname": root,
                            'images': rglobs(root, imageexts),
                            'sounds': rglobs(root, soundexts)
                            }

    return dm


if __name__ == '__main__':
    import paths
    import pprint
    slowar1 = r"E:\1_SYNS_ORIGINAL\0SYNC\python_projects\sling\lingvo2\data\slovar1\slovar1.txt"
    season = r"D:\user\projects\sling\lingvo2\data\seasons\seasons.xlsx"
    reader = Reader().load(season)
    pprint.pprint(reader)

    # datapath = paths.DATA



    # dext = (".txt", ".xlsx")
    # imext = (".png", ".jpg")

    # pprint.pprint(scan(datapath))
#