
from PyQt5.QtGui import *

from gui.custom.abccard import AbcDropWidgetItem

class WidgetItem(AbcDropWidgetItem):
    def __init__(self, widget_tipe, text=None, soundBtnFlag=False, idO=None, main=None, *args, **kwargs):
        """
        этот виджет добавляем в контейнер AbcDropLayout
        :param widget_tipe:
        :param text:
        :param args:
        :param kwargs:
        """

        super().__init__(widget_tipe, text, idO, soundBtnFlag, main, *args, **kwargs)
        self.main = main
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if self.component.text() and event.type() == 11:  # Если мышь покинула область фиджета
            self.soundBtn.setIcon(QIcon(":/volume.png"))
        elif self.component.text() and event.type() == 10:# Если мышь над виджетом
            self.soundBtn.setIcon(QIcon(":/volumeHover.png"))
        return False

    def __repr__(self):
        return "{}-{}".format(self.__class__.__name__, self.idO)