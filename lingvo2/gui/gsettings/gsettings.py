#!/usr/bin/env python3

from gui.custom.customwidgets import *
from gui.gsettings.gsettingsdict import GSettingsDict
from gui.gsettings.gsettingsgeometry import GSettingsGeometry


class GsettingsSection(QListWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(150)
        self.setSelectionRectVisible(False)
        self.setFrameStyle(QFrame.NoFrame)


class GsettingsStack(QStackedWidget):
    def __init__(self):
        super().__init__()


class Gsettings(QFrame):
    def __init__(self, main, cfg, objectName):
        super().__init__()
        self.setObjectName(objectName)
        self.main = main
        self.cfg = cfg
        self.box = BoxLayout(QBoxLayout.LeftToRight, self)
        self._sections = {}
        self.sections = GsettingsSection()
        self.sections.itemSelectionChanged.connect(self.chooseSection)
        self.settingsStacks = GsettingsStack()
        self.box.addWidget(self.sections)
        self.box.addWidget(self.settingsStacks)

        self._sections["gSettingsGeometry"] = GSettingsGeometry(self.main,
                                                                self.cfg,
                                                                    "графика",
                                                                    "gSettingsGeometry")
        self._sections["gSettingsDict"] = GSettingsDict(self.main, self.cfg,
                                                            "словари", "gSettingsDict")

        self.setSections(self._sections)

    def setSections(self, sectionsDict):
        for name, sectionFrame in sectionsDict.items():
            item = QListWidgetItem(sectionFrame.textName)
            self.sections.addItem(item)
            self.settingsStacks.addWidget(sectionFrame)


    def chooseSection(self):
        self.settingsStacks.setCurrentIndex(self.sections.currentIndex().row())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(open('./etc/{0}.qss'.format('style'), "r").read())
    main = Gsettings()
    main.show()
    sys.exit(app.exec_())
