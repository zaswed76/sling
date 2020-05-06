import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from gui.custom import dropcomponents
from gui.custom.abccard import *


class DropWidgetItem(AbcDropWidgetItem):
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
        self.controlsDropLabel = ControlsDropLabel(self)
        self.controlsDropLabel.closeDropLabelBtn.clicked.connect(self.removeComponent)
        self.controlsDropLabel.tuneDropLabelBtn.clicked.connect(self.tuneComponent)
        self.controlsDropLabel.hide()

    def removeComponent(self):
        conteiner = self.sender().parent().parent().parent()
        widget = self.sender().parent().parent()
        idOWidget = widget.idO
        conteiner.cardModel.removeItemToIdO(conteiner.side, conteiner.index, idOWidget)
        conteiner.removeComponent(idOWidget)

    def tuneComponent(self):
        conteiner = self.sender().parent().parent().parent()
        widget = self.sender().parent().parent()
        idWidget = id(widget)
        self.tuneDropWidgetItemDialog = TuneDropWidgetItem()
        # self.tuneDropWidgetItemDialog.show()

    def resizeEvent(self, e):
        super(DropWidgetItem, self).resizeEvent(e)
        rect = self.component.rect()
        self.controlsDropLabel.move(rect.topLeft() + QPoint(5, 5))

    def eventFilter(self, obj, event):
        if event.type() == 11:  # Если мышь покинула область фиджета
            self.controlsDropLabel.hide()  # выполнить  callback1()
        elif event.type() == 10:# Если мышь над виджетом
            self.controlsDropLabel.show()  # выполнить  callback2()
        return False

    def __repr__(self):
        return "{}-{}".format(self.__class__.__name__, self.idO)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(open('./etc/{0}.qss'.format('style'), "r").read())
    main = DropWidgetItem("DropLabel", "Word")
    main.show()
    sys.exit(app.exec_())