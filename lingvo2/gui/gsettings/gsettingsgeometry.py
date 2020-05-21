#!/usr/bin/env python3

from functools import partial
from gui.custom.customwidgets import *
from gui.gsettings.abc import AbcGSettingsFrame

from gui.custom import customwidgets

class ControlBtn(customwidgets.AbcControlBtn):
    def __init__(self, objectName, main, text="", *__args):
        super().__init__(objectName, main, text, *__args)

class ServiceBtn(QPushButton):
    def __init__(self, icon, *__args):
        super().__init__(*__args)
        self.setFixedSize(25, 25)
        self.setIcon(QIcon(icon))
        self.setFlat(True)








class GSettingsGeometry(AbcGSettingsFrame):
    def __init__(self, main, cfg, textName, obgectName, *args, **kwargs):
        super().__init__(main, cfg, textName, obgectName, *args, **kwargs)
        self.cfg = cfg
        self.main = main
        self.box = QVBoxLayout(self)
        self.options = {}

        viewCardWidth = AbcSpinBox()
        viewCardWidth.setMaximum(1500)
        viewCardWidth.setValue(cfg["ui"]["viewCardWidth"])
        viewCardWidth.lastValue = viewCardWidth.value()

        self.addOption("ширина карточки", viewCardWidth, "viewCardWidth")

        viewCardHeight = AbcSpinBox()
        viewCardHeight.setMaximum(1500)
        viewCardHeight.setValue(cfg["ui"]["viewCardHeight"])
        viewCardHeight.lastValue = viewCardHeight.value()
        self.addOption("высота карточки", viewCardHeight, "viewCardHeight")

        fullScreen = QCheckBox()
        fullScreen.setChecked(cfg["ui"]["fullScreen"])
        fullScreen.setValue = fullScreen.setChecked
        fullScreen.value = fullScreen.isChecked
        fullScreen.lastValue = fullScreen.isChecked()
        self.addOption("полный экран", fullScreen, "fullScreen")

        self.box.addStretch(10)


    def addOption(self, text, widget, objectName):
        self.options[objectName] = widget
        self.options[objectName].setObjectName(objectName)
        box = customwidgets.BoxLayout(QBoxLayout.LeftToRight, spacing=8)
        option = widget
        lastValue = option.lastValue
        redo = ServiceBtn(":/redo.png")
        redo.clicked.connect(partial(option.setValue, lastValue))
        box.addWidget(option)
        box.addWidget(redo)
        form = AbcFormFormlayout()
        form.addRow(AbcFormLabel(text), box)
        self.box.addLayout(form)

    def updateCfg(self):
        for option in self.options.values():
            v = option.value()
            self.cfg["ui"][option.objectName()] = v






if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(open('./etc/{0}.qss'.format('style'), "r").read())
    main = GSettingsGeometry()
    main.show()
    sys.exit(app.exec_())