import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import dropcomponents
from abccard import *

class SoundBtn(QPushButton):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setFlat(False)

class CloseDropLabelBtn(QPushButton):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setIcon(QIcon("./resources/icons/base/closeComponent.png"))

class TuneDropLabelBtn(QPushButton):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setIcon(QIcon("./resources/icons/base/icon_cog.png"))

class ControlsDropLabel(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.box = AbcBoxLayout(QBoxLayout.LeftToRight, parent=self)
        self.closeDropLabelBtn = CloseDropLabelBtn(self)
        self.tuneDropLabelBtn = TuneDropLabelBtn(self)
        self.box.addWidgets([self.closeDropLabelBtn, self.tuneDropLabelBtn])

class DropWidgetItem(QFrame):
    def __init__(self, widget_tipe, text=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.installEventFilter(self)
        self.box = QHBoxLayout(self)
        self.box.setContentsMargins(0, 0, 0, 0)
        self.box.setSpacing(0)
        self.component = getattr(dropcomponents, widget_tipe)()
        if text: self.component.setText(text)
        self.box.addWidget(self.component)
        self.soundBtn = SoundBtn(self.component)
        self.controlsDropLabel = ControlsDropLabel(self)
        self.controlsDropLabel.closeDropLabelBtn.clicked.connect(self.removeComponent)
        self.controlsDropLabel.tuneDropLabelBtn.clicked.connect(self.tuneComponent)
        self.controlsDropLabel.hide()

    def removeComponent(self):
        conteiner = self.sender().parent().parent().parent()
        widget = self.sender().parent().parent()
        idWidget = id(widget)
        print(conteiner, widget)
        # conteiner.removeComponent(idWidget)


    def tuneComponent(self):
        conteiner = self.sender().parent().parent().parent()
        widget = self.sender().parent().parent()
        idWidget = id(widget)
        print(conteiner, widget)
        # print(conteiner, idWidget, widget, sep=" - ")

    def resizeEvent(self, e):
        rect = self.component.rect()
        center = rect.center()
        right = rect.right()
        center.setX(right-75)
        center.setY(int(center.y()-25/2))
        self.soundBtn.move(center)

    def eventFilter(self, obj, event):
        if event.type() == 11:  # Если мышь покинула область фиджета
            self.controlsDropLabel.hide()  # выполнить  callback1()
        elif event.type() == 10:# Если мышь над виджетом
            self.controlsDropLabel.show()  # выполнить  callback2()
        return False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(open('./etc/{0}.qss'.format('style'), "r").read())
    main = DropWidgetItem("DropLabel", "Word")
    main.show()
    sys.exit(app.exec_())