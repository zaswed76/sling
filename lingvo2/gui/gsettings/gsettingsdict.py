#!/usr/bin/env python3


from gui.custom.customwidgets import *
from gui.gsettings.abc import AbcGSettingsFrame
from gui.custom import customwidgets

class GSettingsDict(AbcGSettingsFrame):
    def __init__(self, main, cfg, textName, obgectName, *args, **kwargs):
        super().__init__(main, cfg, textName, obgectName, *args, **kwargs)
        self.box = QHBoxLayout(self)

        self.main = main
        self.btn = customwidgets.AbcControlBtn("bumcaca", self.main)
        self.box.addWidget(self.btn)
