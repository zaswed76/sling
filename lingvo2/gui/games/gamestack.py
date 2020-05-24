# import sys
# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
# from PyQt5.QtCore import *
from gui.custom.customwidgets import *






class Games(QFrame):
    def __init__(self, main, objectName=None, config=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main = main
        self.cfg = config
        self.setObjectName(objectName)
        # self.resize(500, 500)
        # self.setFixedWidth(1200)
        self.box = BoxLayout(QBoxLayout.TopToBottom, self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(open('./etc/{0}.qss'.format('style'), "r").read())
    main = Games()
    main.show()
    sys.exit(app.exec_())