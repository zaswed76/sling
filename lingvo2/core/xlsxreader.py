import pandas as pd

import paths
import numpy as np


def xlsxRead(xlsx_path):
        df = pd.read_excel(xlsx_path, header=None)
        df2 = df.fillna("")
        return _formatter(df2.values)

def _mfilter(lst):
    res = []
    for x in  lst:
        if not x or x.isspace():
            res.append(False)
        else:
            res.append(True)
    return any(res)

def _formatter(data):
    _data = [list(x[:5]) for x in data if any(x)]
    res = []
    for line in _data:
        line = [str(x) for x in line]
        if _mfilter(line):
            res.append(line)
    return res



if __name__ == '__main__':
    xlxsFile = paths.DATATESTDIR / "1251Test.xlsx"
    xlxsFile2 = paths.DATATESTDIR / "1251Test3col.xlsx"
    data = xlsxRead(xlxsFile2)

    for line in data:
        print(line)
    #
    # print("-----------------")
    #
    # for line in fdata:
    #     print(formatter(line))
