
from gui.custom.abccard import AbcDropWidgetItem

class WidgetItem(AbcDropWidgetItem):
    def __init__(self, widget_tipe, text=None, soundBtnFlag=False, idO=None, *args, **kwargs):
        """
        этот виджет добавляем в контейнер AbcDropLayout
        :param widget_tipe:
        :param text:
        :param args:
        :param kwargs:
        """
        super().__init__(widget_tipe, text, idO, soundBtnFlag, *args, **kwargs)


    def __repr__(self):
        return "{}-{}".format(self.__class__.__name__, self.idO)