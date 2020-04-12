
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
        self.setAlignment(Qt.AlignCenter)

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

        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        print("dragEnterEvent")
        e.accept()

    def dropEvent(self, e):
        print("dropEvent")
        e.accept()
