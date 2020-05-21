#!/usr/bin/env python3


from gui.custom.customwidgets import *
from gui.gsettings.abc import AbcGSettingsFrame

from gui.custom import customwidgets

class ControlBtn(customwidgets.AbcControlBtn):
    def __init__(self, objectName, main, text="", *__args):
        super().__init__(objectName, main, text, *__args)


class GSettingsGeometry(AbcGSettingsFrame):
    def __init__(self, main, cfg, textName, obgectName, *args, **kwargs):
        super().__init__(main, cfg, textName, obgectName, *args, **kwargs)
        self.main = main
        self.box = QVBoxLayout(self)
        self.btn = ControlBtn("tratata", self.main)
        self.box.addWidget(self.btn)






if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(open('./etc/{0}.qss'.format('style'), "r").read())
    main = GSettingsGeometry()
    main.show()
    sys.exit(app.exec_())