import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

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
        self.main = main
        self.setFixedHeight(42)

        self.addAction(
            QAction(QIcon(":/arrow_right_green.png"), "cardView", self))
        self.addAction(
            QAction(QIcon(":/book_blue.png"), "chooseDict", self))
        self.addAction(
            QAction(QIcon(":/component_blue_edit.png"), "cardEditView", self))
        self.addAction(
            QAction(QIcon(":/profile.png"), "profile", self))
        self.addSeparator()
        self.addWidget(Spacer(stretch=1))
        self.addAction(
            QAction(QIcon(":/component_blue_replace.png"), "cardrefresh", self))
        self.addWidget(Spacer(spacing=26))

