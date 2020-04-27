import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class DocFrame(QFrame):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.setFixedSize(200, 500)
        self.setStyleSheet('background: red;')

class Doc(QDockWidget):
    def __init__(self, *__args):
        super().__init__(*__args)
        # self.setFloating(True)

        # self.setDo



class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(500, 500)

        self.doc = Doc()
        self.listWidget = QListWidget()
        self.listWidget.setFixedSize(200, 500)
        self.listWidget.setStyleSheet('background: #ffffff;')
        self.listWidget.addItem('Google')
        self.listWidget.addItem('Facebook')
        self.listWidget.addItem('Microsoft')
        self.listWidget.addItem('Apple')
        self.doc.setWidget(self.listWidget)
        self.doc.show()
        # self.addDockWidget(Qt.LeftDockWidgetArea, self.doc)


    def moveEvent(self, e):
        pos = e.pos()
        fpos = pos - QPoint(224, 30)
        self.doc.move(fpos)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyleSheet(open('./etc/{0}.qss'.format('style'), "r").read())
    main = Main()
    main.show()
    sys.exit(app.exec_())


