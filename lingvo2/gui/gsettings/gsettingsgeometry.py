#!/usr/bin/env python3


from gui.custom.customwidgets import *
from gui.gsettings.abc import AbcGSettingsFrame


class GSettingsGeometry(AbcGSettingsFrame):
    def __init__(self, main, cfg, textName, obgectName, *args, **kwargs):
        super().__init__(main, cfg, textName, obgectName, *args, **kwargs)
        self.box = QHBoxLayout(self)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(open('./etc/{0}.qss'.format('style'), "r").read())
    main = GSettingsGeometry()
    main.show()
    sys.exit(app.exec_())