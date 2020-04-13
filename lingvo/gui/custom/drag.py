import datetime

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Widget(QPushButton):
    def __init__(self):
        super().__init__()



class DragLabel(QLabel):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setFont(QFont("arial", 30))
        self.setAlignment(Qt.AlignLeft)

    def mouseMoveEvent(self, e):
        mimeData = QMimeData()
        mimeData.setText(self.text())
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        dropAction = drag.exec_(Qt.MoveAction)

class DelBtn(QPushButton):
    def __init__(self, icon, text,  parent, *__args):
        super().__init__(*__args)
        self.setParent(parent)
        self.setIcon(QIcon(icon))
        self.lbText = text
        self.setFixedSize(25,25)
        self.setFont(QFont("arial", 12))
        self.setText("x")


class DropLabel(QLabel):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setFont(QFont("arial", 160))
        self.setAlignment(Qt.AlignCenter)
        self.installEventFilter(self)



        self.btn = DelBtn("", self.text(), self)
        self.btn.clicked.connect(self.parent().delLabel)
        text, self.suffix = self.text().split("_")
        self.setText(text)


    def eventFilter(self, obj, event):
        if event.type() == 11:  # Если мышь покинула область фиджета
            self.btn.hide()  # выполнить  callback1()
        elif event.type() == 10:  # Если мышь над виджетом
            self.btn.show()  # выполнить  callback2()


        return False

class DragFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.box = QVBoxLayout(self)
        self.setStyleSheet('background: grey;')
        self.setAcceptDrops(True)
        self.labels = {}
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        mime = e.mimeData()
        text = mime.text()
        if self.box.count() < 4:
                suffix = datetime.datetime.now().strftime("_%y%m%d%H%M%S")
                text += suffix
                self.labels[text] = DropLabel(text, self)
                self.labels[text].setFont(QFont("arial", 40))
                self.box.addWidget(self.labels[text])
        e.accept()

    def delLabel(self):
        lb = self.sender()
        key = lb.lbText
        self.box.removeWidget(self.labels[key])
        self.labels[key].deleteLater()
