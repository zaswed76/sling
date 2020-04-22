from PyQt5.QtCore import *

import inspect as _insp
import random

ins = _insp.stack

from ex.modelex.picleconf import PConfig
_PATHCFG = "./cfg.pkl"

class NumList:
    def __init__(self):
        self._data = []

    def plus(self):
        self._data.append(random.randint(0, 9))

    def minus(self):
        self._data.pop()

    @property
    def data(self):
        return self._data



class Model(QObject):

    updateSignal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.contentCfg = PConfig(_PATHCFG)
        self._num = self.contentCfg.load()




    @property
    def reversenum(self):
        return "".join([str(x) for x in reversed(self._num.data)])

    @property
    def num(self):
        return "".join([str(x) for x in self._num.data])

    @pyqtSlot()
    def numplus(self):
        self._num.plus()
        self.updateSignal.emit()

    @pyqtSlot()
    def numminus(self):
        self._num.minus()
        self.updateSignal.emit()

    @pyqtSlot()
    def load(self):
        self._num = self.contentCfg.load()
        self.updateSignal.emit()

    @pyqtSlot()
    def save(self):
        self.contentCfg.save(self._num)

if __name__ == '__main__':
    pass
    obj = NumList()
    contentCfg = PConfig(_PATHCFG)
    contentCfg.save(obj)