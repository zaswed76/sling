import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

class ToolBtn(QToolButton):
    def __init__(self, parent, qicon, action, checkable=False):
        super().__init__()
        self.action = action
        self.setObjectName(action)
        self.parent = parent
        self.setIcon(qicon)

        self.setCheckable(checkable)

    def mousePressEvent(self, QMouseEvent):
        getattr(self.parent, self.action)()
        return super().mousePressEvent(QMouseEvent)




class Spacer(QFrame):
    def __init__(self, spacer=None, stretch=0, spacing=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.box = QHBoxLayout(self)
        self.box.setContentsMargins(0, 0, 0, 0)
        self.box.setSpacing(0)
        if spacer is not None: self.box.addSpacerItem(spacer)
        if stretch: self.box.addStretch(stretch)
        if spacing: self.box.addSpacing(spacing)

class ToolBar(QToolBar):
    def __init__(self, main, *__args):
        super().__init__(*__args)
        self.btns = {}
        self.main = main
        self.setFixedHeight(42)
        # self.addWidget(Spacer(spacing=42))
        self.addAction(
            QAction(QIcon(":/arrow_right_green.png"), "cardView", self))
        self.addAction(
            QAction(QIcon(":/book_blue.png"), "chooseDict", self))
        self.addAction(
            QAction(QIcon(":/component_blue_edit.png"), "cardEditView", self))
        # self.addAction(
            # QAction(QIcon(":/profile.png"), "profile", self))
        # self.addSeparator()
        # self.addWidget(Spacer(stretch=1))
        self.addAction(
            QAction(QIcon(":/gear.png"), "gsettings", self))
        self.addButton(QIcon(":/replace2.png"), "cardrefresh")
        self.addWidget(Spacer(stretch=1))
        self.addButton(QIcon(":/music_green_go.png"), "autoSoundGo", checkable=True)
        self.addWidget(Spacer(spacing=4))
        self.addButton(QIcon(":/music_green_rotate.png"), "autoSoundTurn", checkable=True)
        self.addSeparator()
        self.addAction(
            QAction(QIcon(":/windows.png"), "showScreen", self))

        self.addAction(
            QAction(QIcon(":/delete.png"), "closeWindow", self))

        # self.addWidget(Spacer(spacing=42))

    def addButton(self, Qicon, method, checkable=False):
        methodName = "{}Action".format(method)
        self.btns[method] = ToolBtn(self.main, Qicon, methodName, checkable)
        self.addWidget(self.btns[method])
        return self.btns[method]

    def setDisabledButton(self, btnName, p_bool):
        self.btns[btnName].setDisabled(p_bool)