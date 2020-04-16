import datetime
import random

from jinja2 import Template

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
    def __init__(self, icon, text, parent, type=None,  *__args):
        super().__init__(*__args)
        self.type = type
        self.setParent(parent)
        self.setIcon(QIcon(icon))
        self.itemName = text
        self.setFixedSize(22, 22)
        self.setFont(QFont("arial", 12))



class DropLabelControl(QFrame):
    def __init__(self, parent, type=None, *__args):
        super().__init__(*__args)
        self.setParent(parent)
        self.type = type
        self.box = QHBoxLayout(self)
        self.box.setSpacing(4)
        self.box.setContentsMargins(0, 0, 0, 0)
        self.delBtn = ControlLabelBtn("", self.parent().key, self, type=self.type)
        self.delBtn.setObjectName("delBtn")
        self.delBtn.clicked.connect(self.parent().parent().delLabel)

        self.tuneBtn = ControlLabelBtn("", self.parent().key, self)
        self.tuneBtn.setObjectName("tuneBtn")
        self.tuneBtn.clicked.connect(self.parent().parent().showTuneLabel)
        self.box.addWidget(self.delBtn)
        self.box.addWidget(self.tuneBtn)


class Style:
    Align = dict(left=Qt.AlignLeft, right=Qt.AlignRight, center=Qt.AlignCenter)

    def __init__(self, text=None, font_name="Tahoma", font_size=16, italic=False,
                 text_color="darkgrey", align="center", content_marging=(0, 0, 0, 0)):
        self.text = text
        self.contentMarging = content_marging
        self.align = self.Align[align]
        self.textColor = text_color
        self.italic = italic
        self.fontSize = font_size
        self.fontName = font_name

    @property
    def font(self):
        return QFont(self.fontName, self.fontSize, italic=self.italic)

class InputEdit(QTextEdit):

    def __init__(self, text, parent, *__args):
        super().__init__(*__args)
        self.key = text
        self.setPlainText("")
        self.setParent(parent)
        self.itemName, self.suffix = text.split("_")
        self.installEventFilter(self)
        self.dropLabelControl = DropLabelControl(self, type=self.__class__.__name__)

    @property
    def type(self):
        return self.__class__.__name__

    def eventFilter(self, obj, event):

        if event.type() == 11:  # Если мышь покинула область фиджета
            self.dropLabelControl.hide()  # выполнить  callback1()
        elif event.type() == 10:
            # Если мышь над виджетом
            self.dropLabelControl.show()  # выполнить  callback2()
        return False

class DropLabel(QLabel):
    def __init__(self, text, parent, *__args):
        super().__init__(*__args)
        self.setText(text)
        self.key = text
        self.setParent(parent)
        self.itemName, self.suffix = self.text().split("_")
        self.setAlignment(Qt.AlignCenter)
        self.installEventFilter(self)
        self.setStyleSheet("QLabel { color: #2D2D2D }")



        self.styleTypes = {
            "Пример": Style(text="this is an example in english", font_name="Helvetica", font_size=16,
                            text_color="#144676", italic=True),
            "Word": Style(text="Word", font_name="Helvetica", font_size=56, text_color="#262626"),
            "Транскрипция": Style(text="[транскрипция]",font_name="Helvetica", font_size=30, text_color="#3F3F3F"),
            "Перевод": Style(text="Перевод",font_name="Helvetica", font_size=56, text_color="#262626"),
            "input": Style(text="Input",font_name="Helvetica", font_size=56, text_color="#262626")
        }

        self.dropLabelControl = DropLabelControl(self, type=self.__class__.__name__)
        self._tuneText(self.itemName)

    @property
    def type(self):
        return self.__class__.__name__

    def setStyleContent(self, style):
        self.setText(style.text)
        self.setFont(QFont(style.font))
        self.setStyleSheet(Template("QLabel { color:{{tcolor}} }").render(tcolor=style.textColor))
        self.setAlignment(style.align)
        self.setContentsMargins(*style.contentMarging)

    def _tuneText(self, lbText):
        if lbText in self.styleTypes:
            self.setStyleContent(self.styleTypes[lbText])

    def eventFilter(self, obj, event):

        if event.type() == 11:  # Если мышь покинула область фиджета
            self.dropLabelControl.hide()  # выполнить  callback1()
        elif event.type() == 10:
            print("999999999999999")# Если мышь над виджетом
            self.dropLabelControl.show()  # выполнить  callback2()
        return False


class DragFrame(QFrame):

    def __init__(self, parent, object_name, cfg):
        super().__init__()
        self.WidgetTypes = {"DropLabel": self.addLabel, "InputEdit": self.addQLineEdit}
        self.cfg = cfg
        self.parent = parent
        self.setObjectName(object_name)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizePolicy(sizePolicy)
        self.box = QVBoxLayout(self)
        self.setAcceptDrops(True)
        self.labels = {}
        self.setAcceptDrops(True)
        shadow = QGraphicsDropShadowEffect(blurRadius=12, xOffset=3, yOffset=3)
        self.setGraphicsEffect(shadow)
        self.setContent(self.cfg)

    def dragEnterEvent(self, e):
        e.accept()

    def setContent(self, cfg):
        side = self.parent.objectName()
        layout = self.objectName()
        content = cfg["card"]["content"][side][layout]

        for item in content:
            text, type = item.split("_")
            if self.box.count() < 4:
                self.addQWidget(type, text)

    def addContentCfg(self, cfg, text, type):
        side = self.parent.objectName()
        layout = self.objectName()
        cfg["card"]["content"][side][layout].append("_".join((text, type)))

    def delContentCfg(self, cfg, text):
        side = self.parent.objectName()
        layout = self.objectName()
        cfg["card"]["content"][side][layout].remove(text)

    def dropEvent(self, e):
        mime = e.mimeData()
        text, type = mime.text().split("_")
        if self.box.count() < 4:
            self.addQWidget(type, text)
            self.addContentCfg(self.cfg, text, type)
        e.accept()

    def __getSuffix(self):
        n = str((datetime.datetime.now().strftime("%y%m%d%H%M%S")) + str(random.randint(0, 99999999999)))
        nl = [x for x in n]
        random.shuffle(nl)
        return "_" + "".join(nl)

    def addQWidget(self, type, text):
        self.WidgetTypes[type](text)


    def addLabel(self, text):
        text += self.__getSuffix()
        self.labels[text] = DropLabel(text, self)
        self.box.addWidget(self.labels[text])

    def addQLineEdit(self, text):
        text += self.__getSuffix()
        self.labels[text] = InputEdit(text, self)
        self.box.addWidget(self.labels[text], Qt.AlignCenter)



    def delLabel(self):
        item = self.sender()
        name = item.itemName
        print(name, "iiiiiiiiii")
        key = "_".join((name.split("_")[0], item.type))
        self.delContentCfg(self.cfg, key)
        self.box.removeWidget(self.labels[name])
        self.labels[name].deleteLater()

    def showTuneLabel(self):
        lb = self.sender()
        key = lb.itemName
        self.tuneLabel = CustomizeLabelDialog(self)


class CustomizeLabelDialog(QWidget):
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
        self.show()

    def chooseBg(self):
        print(self.sender())
