import datetime
import paths
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Widget(QPushButton):
    def __init__(self):
        super().__init__()



class DragLabel(QLabel):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setFont(QFont("Helvetica", 30))
        self.setAlignment(Qt.AlignLeft)

    def mouseMoveEvent(self, e):
        mimeData = QMimeData()
        mimeData.setText(self.text())
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        dropAction = drag.exec_(Qt.MoveAction)

class ControlLabelBtn(QPushButton):
    def __init__(self, icon, text,  parent, *__args):
        super().__init__(*__args)
        self.setParent(parent)
        self.setIcon(QIcon(icon))
        self.lbText = text
        self.setFixedSize(22,22)
        self.setFont(QFont("arial", 12))
        # self.setText("x")

class DropLabelControl(QFrame):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.box = QHBoxLayout(self)
        self.box.setSpacing(4)
        self.box.setContentsMargins(0, 0, 0, 0)

        self.delBtn = ControlLabelBtn("", self.parent().text(), self)
        self.delBtn.setObjectName("delBtn")
        self.delBtn.clicked.connect(self.parent().parent().delLabel)

        self.tuneBtn = ControlLabelBtn("", self.parent().text(), self)
        self.tuneBtn.setObjectName("tuneBtn")
        self.tuneBtn.clicked.connect(self.parent().parent().showTuneLabel)
        self.box.addWidget(self.delBtn)
        self.box.addWidget(self.tuneBtn)

class DropLabel(QLabel):
    def __init__(self, *__args):
        super().__init__(*__args)

        self.setAlignment(Qt.AlignCenter)
        self.installEventFilter(self)
        self.setStyleSheet("QLabel { color: #2D2D2D }")

        self.dropLabelControl = DropLabelControl(self)


        text, self.suffix = self.text().split("_")
        self.setText(text)
        self._tuneText()

    def _tuneText(self):
        if self.text() == "Пример":
            self.setText("this is an example in english")
            self.setFont(QFont("Helvetica", 14, italic=True))
            self.setStyleSheet("QLabel { color: #144676 }")
            self.setAlignment(Qt.AlignLeft)
            self.setContentsMargins(70, 10, 0, 0)

        elif self.text() == "Word":
            self.setFont(QFont("Helvetical", 56))
            self.setAlignment(Qt.AlignCenter)

        elif self.text() == "Транскрипция":
            self.setText("[Транскрипция]")
            self.setStyleSheet("QLabel { color: #6E6E6E }")
            self.setFont(QFont("Helvetica", 30))
            self.setAlignment(Qt.AlignCenter)

        elif self.text() == "Перевод":
            self.setFont(QFont("Helvetica", 56))
            self.setAlignment(Qt.AlignCenter)



    def eventFilter(self, obj, event):
        if event.type() == 11:  # Если мышь покинула область фиджета
            self.dropLabelControl.hide()  # выполнить  callback1()
        elif event.type() == 10:  # Если мышь над виджетом
            self.dropLabelControl.show()  # выполнить  callback2()
        return False

class DragFrame(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        # self.setScene(self.scene)
        # self.scene.addLine(QLineF(self.rect().topLeft(), self.rect().topRight()))
        # rcontent = self.contentsRect()
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # self.setSceneRect(0, 0, rcontent.width(), rcontent.height())
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizePolicy(sizePolicy)
        self.box = QVBoxLayout(self)
        self.setAcceptDrops(True)
        self.labels = {}
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        mime = e.mimeData()
        text = mime.text()
        # print(mime, "!!!")
        if self.box.count() < 4:
                suffix = datetime.datetime.now().strftime("_%y%m%d%H%M%S")
                text += suffix
                self.labels[text] = DropLabel(text, self)
                # self.labels[text].setFont(QFont("arial", 40))
                self.box.addWidget(self.labels[text])
        e.accept()

    def delLabel(self):
        lb = self.sender()
        key = lb.lbText
        self.box.removeWidget(self.labels[key])
        self.labels[key].deleteLater()

    def showTuneLabel(self):
        lb = self.sender()
        key = lb.lbText
        self.tuneLabel = TuneLabel(self)






class TuneLabel(QWidget):
    def __init__(self, p, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.win = uic.loadUi(paths.UIFORM / "tuneEditLabels.ui")
        self.win.bgBtn.clicked.connect(self.chooseBg)
        self.win.colorBtn.clicked.connect(self.chooseBg)
        self.win.fontNameBtn.clicked.connect(self.chooseBg)
        self.win.fontSizeBtn.clicked.connect(self.chooseBg)
        self.win.AlignLb.currentIndexChanged.connect(self.chooseBg)
        self.win.AlignLb.addItems(["слева", "по центру", "справа"])
        self.hbox = QHBoxLayout(self)
        self.hbox.addWidget(self.win)

        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlag(Qt.Tool)
        # self.resize(300, 500)
        self.show()

    def chooseBg(self):
        print(self.sender())