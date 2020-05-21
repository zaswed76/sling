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
        self.main = main
        self.box = QVBoxLayout(self)


        width_option = AbcSpinBox()

        width_option.setMaximum(1500)
        width_option.setValue(cfg["ui"]["viewCardSize"][0])
        width_option.lastValue = width_option.value()
        self.addOption("ширина карточки", width_option)


    def addOption(self, name, widget):
        box = customwidgets.BoxLayout(QBoxLayout.LeftToRight, spacing=8)
        option = widget
        lastValue = option.lastValue
        redo = ServiceBtn(":/redo.png")
        redo.clicked.connect(partial(option.setValue, lastValue))
        box.addWidget(option)
        box.addWidget(redo)
        form = AbcFormFormlayout()
        form.addRow(AbcFormLabel(name), box)
        self.box.addLayout(form)






if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(open('./etc/{0}.qss'.format('style'), "r").read())
    main = GSettingsGeometry()
    main.show()
    sys.exit(app.exec_())